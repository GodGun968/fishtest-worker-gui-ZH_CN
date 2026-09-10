import customtkinter as ctk
import tkinter.scrolledtext
import tkinter.messagebox
import subprocess
import threading
import os
import sys
import ctypes
import configparser
import webbrowser
import re
import time
import json
import urllib.request
from i18n import get_language, language_name, localized_level, set_language, supported_languages, t, translate_worker_output

# --- 常量 ---
APP_NAME = "Fishtest Worker Manager I18N"
APP_VERSION = "v0.0.1"
REPO_OWNER = "GodGun968"
REPO_NAME = "fishtest-worker-gui-I18N"

WORKER_DIR = os.path.abspath("worker")
CONFIG_FILE_NAME = "fishtest.cfg"
CONFIG_FILE = os.path.join(WORKER_DIR, CONFIG_FILE_NAME)
EXIT_FILE_NAME = "fish.exit"
MSYS2_PATH = "C:\\msys64"
USERNAME_DEFAULT = "your_username"

def get_asset_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和 PyInstaller 打包环境。"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, "assets", relative_path)

def windows_to_msys2_path(path):
    # 将 C:\Users\... 转换为 /c/Users/...
    drive, rest = os.path.splitdrive(os.path.abspath(path))
    drive_letter = drive.rstrip(":\\/").lower()
    rest = rest.replace("\\", "/").lstrip("/\\")
    return f"/{drive_letter}/{rest}"

class FishtestManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.worker_process = None
        self.is_long_operation_running = False
        self.config = configparser.ConfigParser()
        self.task_total_games = 0
        self.task_current_games = 0
        self.task_start_time = None
        self.latest_version_tag = None
        self.latest_release_url = ""

        # 简体中文是默认界面语言。在创建控件前读取已保存的语言，
        # 确保窗口首次显示时就使用正确的语言。
        self._load_language()
        self._setup_window()
        self._create_widgets()
        self._load_config()
        self.after(100, self._initial_environment_check)
        self.after(101, self._update_all_controls_state) # 延迟检查，确保窗口先完成绘制

        # 在后台检查更新
        self.after(2000, lambda: threading.Thread(target=self._check_latest_version_thread, daemon=True).start())

        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def _load_language(self):
        """在创建界面控件前加载界面语言。"""
        language_config = configparser.ConfigParser()
        language_config.read(CONFIG_FILE)
        set_language(language_config.get("general", "language", fallback="zh_CN"))

    def _setup_window(self):
        self.title(t("app.window_title", version=APP_VERSION))
        self.geometry("900x650")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.iconbitmap(get_asset_path("icon.ico"))

    def _create_widgets(self):
        # --- 顶部控制区域 ---
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        top_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.setup_button = ctk.CTkButton(top_frame, text=t("button.install"), command=lambda: self._run_with_elevation(self._run_full_setup, 'install'))
        self.setup_button.grid(row=0, column=0, padx=5, pady=10)

        self.update_button = ctk.CTkButton(top_frame, text=t("button.update_msys2"), command=lambda: self._run_with_elevation(self._update_msys2, 'update'))
        self.update_button.grid(row=0, column=1, padx=5, pady=10)

        self.settings_button = ctk.CTkButton(top_frame, text=t("button.settings"), command=self._open_settings_window)
        self.settings_button.grid(row=0, column=2, padx=5, pady=10)

        self.uninstall_button = ctk.CTkButton(top_frame, text=t("button.uninstall"), command=self._handle_uninstall_click, fg_color="#C00000", hover_color="#A00000")
        self.uninstall_button.grid(row=0, column=3, padx=5, pady=10)

        # --- 更新通知按钮（默认隐藏） ---
        self.new_version_button = ctk.CTkButton(top_frame, text=t("button.new_version"),
                                                command=self._open_release_page,
                                                fg_color="#229965", hover_color="#1F7A52", text_color="white")
        self.new_version_button.grid(row=1, column=0, columnspan=4, padx=5, pady=(0, 10), sticky="ew")
        self.new_version_button.grid_remove()

        # --- 主要操作区域 ---
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)

        self.worker_button = ctk.CTkButton(action_frame, text=t("button.start_worker"), command=self._toggle_worker, height=50, font=("Arial", 16, "bold"))
        self.worker_button.grid(row=0, column=0, padx=200, pady=5, sticky="ew")
        self.worker_button.bind("<Button-3>", self._force_stop_worker_event) # 右键强制停止

        self.status_label = ctk.CTkLabel(action_frame, text=t("status.initializing"), font=("Arial", 14))
        self.status_label.grid(row=1, column=0, pady=(5,0))

        # --- Worker 任务进度条 ---
        self.task_progress_label = ctk.CTkLabel(action_frame, text="", font=("Arial", 12))
        self.task_progress_label.grid(row=2, column=0, pady=(5,0), sticky="ew")

        self.task_progress_bar = ctk.CTkProgressBar(action_frame)
        self.task_progress_bar.grid(row=3, column=0, padx=50, pady=(5,10), sticky="ew")
        self.task_progress_bar.set(0)

        # Worker 启动前先隐藏
        self.task_progress_label.grid_remove()
        self.task_progress_bar.grid_remove()

        # --- 日志区域 ---
        log_frame = ctk.CTkFrame(self)
        log_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        self.log_text = tkinter.scrolledtext.ScrolledText(log_frame, wrap=ctk.WORD, state='disabled',
                                                          bg="#2B2B2B", fg="#DCE4EE", font=("Consolas", 10),
                                                          relief="flat", borderwidth=0)
        self.log_text.grid(row=0, column=0, sticky="nsew")

        # --- 日志颜色标签 ---
        self.log_text.tag_config("INFO", foreground="#4FC1FF")      # 浅蓝色
        self.log_text.tag_config("WARNING", foreground="#FFD700")   # 金黄色
        self.log_text.tag_config("ERROR", foreground="#FF453A")     # 红色
        self.log_text.tag_config("SUCCESS", foreground="#32D74B")   # 亮绿色
        self.log_text.tag_config("FATAL", foreground="#FF00FF")     # 洋红色
        self.log_text.tag_config("TIMESTAMP", foreground="#808080") # 灰色
        self.log_text.tag_config("WORKER", foreground="#DCE4EE")    # 普通文本
        self.log_text.tag_config("CMD", foreground="#B0B0B0")       # 较暗的命令行输出

    # --- 配置与状态管理 ---
    def _load_config(self):
        self.config.read(CONFIG_FILE)
        if 'login' not in self.config:
            self.config['login'] = {
                'username': USERNAME_DEFAULT, 'password': ''
            }
        if 'parameters' not in self.config:
            self.config['parameters'] = {
                'concurrency': '3'
            }
        user = self.config.get('login', 'username')
        cores = self.config.get('parameters', 'concurrency')
        self.status_label.configure(text=t("status.idle", user=user, cores=cores))

    def _refresh_ui_text(self):
        """语言切换后刷新主窗口文本。"""
        self.title(t("app.window_title", version=APP_VERSION))
        self.setup_button.configure(text=t("button.install"))
        self.update_button.configure(text=t("button.update_msys2"))
        self.settings_button.configure(text=t("button.settings"))
        notification_text = (
            t("button.new_version_tag", version=self.latest_version_tag)
            if self.latest_version_tag else t("button.new_version")
        )
        self.new_version_button.configure(text=notification_text)
        self._update_all_controls_state()

    def _save_config(self):
        try:
            with open(CONFIG_FILE, 'w') as configfile:
                self.config.write(configfile)
            self._load_config()
            self.add_log(t("log.settings_saved", file=CONFIG_FILE_NAME), level="SUCCESS")
            self._handle_github_token()
        except PermissionError:
            self.add_log(t("log.save_permission", file=CONFIG_FILE), level="ERROR")
        except Exception as e:
            self.add_log(t("log.save_io", error=e), level="ERROR")

    def _initial_environment_check(self):
        """记录初始环境状态，不改变界面控件。"""
        msys2_installed = os.path.exists(os.path.join(MSYS2_PATH, "msys2_shell.cmd"))
        worker_installed = os.path.exists(os.path.join(WORKER_DIR, "worker.py"))

        if not msys2_installed:
            self.add_log(t("log.msys2_missing"))
        elif not worker_installed:
            self.add_log(t("log.worker_missing"))
        else:
            self.add_log(t("log.setup_complete"), level="SUCCESS")
            user = self.config.get('login', 'username', fallback=USERNAME_DEFAULT)
            password = self.config.get('login', 'password', fallback='')
            if user == USERNAME_DEFAULT or not user or not password:
                self.add_log(t("log.settings_required"))
                self.after(500, self._open_settings_window)
            else:
                self.add_log(t("log.worker_ready"))

    def _update_all_controls_state(self):
        """根据应用状态统一设置所有控件的状态。"""
        is_worker_running = self.worker_process and self.worker_process.poll() is None

        # 情况 1：Worker 正在运行
        if is_worker_running:
            for button in [self.setup_button, self.update_button, self.settings_button, self.uninstall_button]:
                button.configure(state='disabled')
            self.worker_button.configure(text=t("button.stop_worker"), fg_color="#C00000", hover_color="#A00000", state="normal")
            user = self.config.get('login', 'username')
            cores = self.config.get('parameters', 'concurrency')
            self.status_label.configure(text=t("status.running", user=user, cores=cores))
            return

        # 情况 2：安装、更新或卸载等长时间操作正在运行
        if self.is_long_operation_running:
            for button in [self.setup_button, self.update_button, self.settings_button, self.uninstall_button, self.worker_button]:
                button.configure(state='disabled')
            return

        # 情况 3：应用空闲
        self._load_config()  # 同时刷新状态标签为“空闲”

        msys2_installed = os.path.exists(os.path.join(MSYS2_PATH, "msys2_shell.cmd"))
        worker_installed = os.path.exists(os.path.join(WORKER_DIR, "worker.py"))
        worker_dir_exists = os.path.exists(WORKER_DIR)
        msys2_uninstaller_exists = os.path.exists(os.path.join(MSYS2_PATH, "uninstall.exe"))

        self.setup_button.configure(state='normal')
        self.settings_button.configure(state='normal')
        self.update_button.configure(state='normal' if msys2_installed else 'disabled')
        self.worker_button.configure(state='normal' if worker_installed else 'disabled',
                                     text=t("button.start_worker"), fg_color="#1F6AA5", hover_color="#144870")

        if worker_dir_exists:
            self.uninstall_button.configure(text=t("button.delete_worker"), state='normal')
        elif msys2_uninstaller_exists:
            self.uninstall_button.configure(text=t("button.uninstall_msys2"), state='normal')
        else:
            self.uninstall_button.configure(text=t("button.uninstall_disabled"), state='disabled')

    # --- 更新检查逻辑 ---
    def _check_latest_version_thread(self):
        """在后台线程中检查 GitHub 的最新发布版本，包含预发行版。"""
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': APP_NAME})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 200:
                    return
                releases = json.loads(response.read().decode())
                latest = self._pick_latest_release(releases)
                if latest:
                    self._compare_versions(
                        latest.get("tag_name", ""),
                        latest.get("html_url", ""),
                    )
                else:
                    self.after(0, self.add_log, t("log.update_no_release"), "WARNING")
        except urllib.error.HTTPError as e:
            if e.code == 403:
                self.after(0, self.add_log, t("log.update_rate_limit"), "WARNING")
            else:
                self.after(0, self.add_log, t("log.update_http_failed", code=e.code), "WARNING")
        except Exception as e:
            self.after(0, self.add_log, t("log.update_network_failed", error=e), "WARNING")

    def _pick_latest_release(self, releases):
        """从 GitHub Releases 中选出最新版本，包含预发行版，排除草稿。"""
        if not isinstance(releases, list):
            return None
        candidates = []
        for release in releases:
            if not isinstance(release, dict) or release.get("draft"):
                continue
            tag = release.get("tag_name", "")
            if tag:
                candidates.append((self._parse_version(tag), tag, release))
        if not candidates:
            return None
        candidates.sort(key=lambda item: (item[0], item[1]))
        return candidates[-1][2]

    def _parse_version(self, v_str):
        try:
            numeric = v_str.lstrip("v").split("-", 1)[0]
            return tuple(int(part) for part in numeric.split(".") if part.isdigit())
        except ValueError:
            return (0, 0, 0)

    def _compare_versions(self, latest_tag, release_url=""):
        current = self._parse_version(APP_VERSION)
        latest = self._parse_version(latest_tag)

        if latest > current:
            self.after(0, lambda: self._show_update_notification(latest_tag, release_url))
        else:
            self.after(0, self.add_log, t("log.latest_version", version=APP_VERSION))

    def _show_update_notification(self, latest_tag, release_url=""):
        self.latest_version_tag = latest_tag
        self.latest_release_url = release_url
        self.new_version_button.configure(text=t("button.new_version_tag", version=latest_tag))
        self.new_version_button.grid()
        self.add_log(t("log.new_version", version=latest_tag))

    def _open_release_page(self):
        webbrowser.open(
            getattr(self, "latest_release_url", "")
            or f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases"
        )

    # --- 核心操作 ---
    def _run_with_elevation(self, action_func, action_arg_name):
        """检查管理员权限；没有权限时提权重启，有权限时直接执行操作。"""
        if self._is_admin():
            action_func()
        else:
            try:
                # 使用 sys.argv[0]，兼容 .py 文件和打包后的 .exe
                script_path = os.path.abspath(sys.argv[0])
                # 将脚本路径和操作参数传递给新的管理员进程
                params = f'"{script_path}" --run-as-admin={action_arg_name}'
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
                self.destroy()  # 关闭当前非管理员窗口
            except Exception as e:
                tkinter.messagebox.showerror(t("dialog.elevation_failed.title"), t("dialog.elevation_failed.message", error=e))

    def _run_full_setup(self):
        if not tkinter.messagebox.askyesno(t("dialog.install.title"), t("dialog.install.message")):
            return

        command = f'"{get_asset_path("00_install_winget_msys2_admin.cmd")}"'
        self._run_command_in_thread(
            command,
            start_message=t("log.install_start"),
            end_message=t("log.install_end"),
            on_complete=self._install_worker_files
        )

    def _install_worker_files(self):
        user = self.config.get('login', 'username')
        password = self.config.get('login', 'password')
        cores = self.config.get('parameters', 'concurrency')

        # 将安装脚本路径转换为 MSYS2 兼容格式
        msys2_script_path = windows_to_msys2_path(get_asset_path('gui_install_worker.sh'))
        # 脚本应从应用根目录运行，以创建“worker”子文件夹。
        app_run_dir = os.path.abspath(".")

        # 需要为 Shell 转义参数；脚本路径使用单引号，
        # 以便 Bash 正确处理 MSYS2 路径中的空格。
        worker_install_cmd = f"bash '{msys2_script_path}' '{user}' '{password}' '{cores}' '{get_language()}'"

        # 使用带引号的 Windows 路径配合 -where，比路径含空格时使用 -here 更安全。
        full_command = f'"{os.path.join(MSYS2_PATH, "msys2_shell.cmd")}" -defterm -ucrt64 -no-start -where "{app_run_dir}" -c "{worker_install_cmd}"'

        self._run_command_in_thread(
            full_command,
            start_message=t("log.worker_install_start"),
            end_message=t("log.worker_install_end"),
            on_complete=self._initial_environment_check
        )

    def _update_msys2(self):
        command = f'"{get_asset_path("04_update_msys2.cmd")}"'
        self._run_command_in_thread(
            command,
            start_message=t("log.msys2_update_start"),
            end_message=t("log.msys2_update_end")
        )

    def _handle_uninstall_click(self):
        worker_dir_exists = os.path.exists(WORKER_DIR)
        msys2_uninstaller_exists = os.path.exists(os.path.join(MSYS2_PATH, "uninstall.exe"))

        if worker_dir_exists:
            self._run_with_elevation(self._delete_worker_folder, 'delete_worker')
        elif msys2_uninstaller_exists:
            self._run_with_elevation(self._uninstall_msys2, 'uninstall_msys2')

    def _delete_worker_folder(self):
        if not tkinter.messagebox.askyesno(t("dialog.delete.title"),
                                           t("dialog.delete.message"),
                                           icon='warning'):
            return

        worker_dir_abs = os.path.abspath(WORKER_DIR)
        command = f'chcp 65001 >nul & if exist "{worker_dir_abs}" (echo {t("command.removing_worker")} & rd /s /q "{worker_dir_abs}") else (echo {t("command.worker_not_found")})'

        self._run_command_in_thread(
            command,
            start_message=t("log.delete_start"),
            end_message=t("log.delete_end")
        )

    def _uninstall_msys2(self):
        if not tkinter.messagebox.askyesno(t("dialog.uninstall.title"),
                                           t("dialog.uninstall.message"),
                                           icon='warning'):
            return

        msys2_uninstaller = os.path.join(MSYS2_PATH, "uninstall.exe")
        command = f'chcp 65001 >nul & if exist "{msys2_uninstaller}" (echo {t("command.uninstalling_msys2")} & start /wait "" "{msys2_uninstaller}" /S) else (echo {t("command.msys2_not_found")})'

        self._run_command_in_thread(
            command,
            start_message=t("log.uninstall_start"),
            end_message=t("log.uninstall_end")
        )

    def _handle_github_token(self):
        token = self.config.get('Fishtest', 'github_token', fallback='').strip()
        if token:
            try:
                # 在 Windows 中，文件名可以是 .netrc 或 _netrc
                netrc_path = os.path.join(os.path.expanduser("~"), "_netrc")
                netrc_content = f"machine api.github.com\nlogin {token}\npassword x-oauth-basic\n"
                with open(netrc_path, "w") as f:
                    f.write(netrc_content)
                self.add_log(t("log.github_token_saved", file=netrc_path))
            except Exception as e:
                self.add_log(t("log.github_token_failed", error=e), level="ERROR")

    # --- Worker 启动/停止逻辑 ---
    def _toggle_worker(self):
        # 检查对象是否存在，而不是依赖 Windows 对进程运行状态的判断。
        if self.worker_process is not None:
            self._stop_worker_gracefully()
        else:
            self._start_worker()

    def _start_worker(self):
        self.add_log(t("log.start_attempt"))

        # 启动进程前清理 fish.exit
        exit_file_path = os.path.join(WORKER_DIR, EXIT_FILE_NAME)
        if os.path.exists(exit_file_path):
            try:
                os.remove(exit_file_path)
                self.add_log(t("log.exit_cleaned", file=EXIT_FILE_NAME))
            except Exception as e:
                self.add_log(t("log.exit_cleanup_failed", file=EXIT_FILE_NAME, error=e), level="ERROR")

        # 重置进度状态并显示进度条
        self.task_total_games = 0
        self.task_current_games = 0
        self.task_start_time = None
        self.task_progress_bar.set(0)
        self.task_progress_label.configure(text="")
        self.task_progress_label.grid()
        self.task_progress_bar.grid()

        # worker.py 必须在 WORKER_DIR 中运行。
        # msys2_shell.cmd 的 -where 参数使用 Windows 路径。
        # 加引号以处理路径中的空格。
        worker_dir_win_path = os.path.abspath(WORKER_DIR)

        # 在 MSYS2 Shell 中执行的命令。
        # -where 已设置工作目录，因此不需要使用“cd”。
        worker_command = "env/bin/python3 worker.py"

        full_command = f'"{os.path.join(MSYS2_PATH, "msys2_shell.cmd")}" -defterm -ucrt64 -no-start -where "{worker_dir_win_path}" -c "{worker_command}"'

        threading.Thread(target=self._execute_worker_process, args=(full_command,), daemon=True).start()

    def _execute_worker_process(self, command):
        try:
            self.worker_process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding='utf-8', errors='replace', shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.after(0, self._update_all_controls_state) # 将界面更新为“运行中”状态
            # --- 逐行处理输出，以获取进度信息 ---
            for line in iter(self.worker_process.stdout.readline, ''):
                self.after(0, self._process_worker_output, line.strip())
            self.worker_process.stdout.close()
            self.worker_process.wait()
        except Exception as e:
            self.after(0, self.add_log, t("log.worker_start_failed", error=e), "FATAL")
        finally:
            self.after(0, self._on_worker_stopped)

    def _stop_worker_gracefully(self):
        # 只有对象确实为 None 时才直接返回。
        # 如果对象存在但已“僵死”，仍继续执行清理。
        if self.worker_process is None:
            return self.add_log(t("log.worker_not_running"))

        # 如果 poll() 返回值（即不为 None），说明包装进程已结束。
        # 但此时 self.worker_process 仍然不为 None，属于“僵死”状态。
        if self.worker_process.poll() is not None:
            self.add_log(t("log.wrapper_dead"), level="WARNING")

        self.add_log(t("log.stopping_gracefully", file=EXIT_FILE_NAME))
        self.worker_button.configure(text=t("button.stopping_worker"), state="disabled")
        try:
            with open(os.path.join(WORKER_DIR, EXIT_FILE_NAME), "w") as f: pass
        except Exception as e:
            self.add_log(t("log.exit_create_failed", file=EXIT_FILE_NAME, error=e), level="ERROR")
            # 创建文件失败时重新启用按钮
            self.worker_button.configure(text=t("button.stop_worker"), state="normal")

    def _force_stop_worker_event(self, event):
        # 检查对象是否存在，而不是依赖 Windows 对进程运行状态的判断。
        if self.worker_process is not None:
            if tkinter.messagebox.askyesno(t("dialog.force_stop.title"), t("dialog.force_stop.message")):
                self._stop_worker_forcefully()

    def _stop_worker_forcefully(self):
        # 只检查对象是否存在。
        # 即使包装进程静默结束，也可以据此完成清理。
        if self.worker_process is None:
            return self.add_log(t("log.worker_not_running"))

        self.add_log(t("log.force_stopping"))
        try:
            subprocess.run(f"taskkill /F /PID {self.worker_process.pid} /T", check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            # 如果进程已经结束（僵死状态），taskkill 会失败。
            self.add_log(t("log.taskkill_failed", error=e), level="WARNING")
            try:
                self.worker_process.terminate()
            except Exception as e:
                # 记录此错误以便排查；通常表示进程已经结束。
                self.add_log(t("log.terminate_failed", error=e), level="DEBUG")

        # 清理上一次“正常停止”尝试遗留的 fish.exit 文件（如有）
        exit_file_path = os.path.join(WORKER_DIR, EXIT_FILE_NAME)
        if os.path.exists(exit_file_path):
            try:
                os.remove(exit_file_path)
                self.add_log(t("log.exit_cleaned", file=EXIT_FILE_NAME))
            except Exception as e:
                self.add_log(t("log.exit_cleanup_failed", file=EXIT_FILE_NAME, error=e), level="ERROR")

    def _on_worker_stopped(self):
        self.add_log(t("log.worker_stopped"), level="SUCCESS")
        self.worker_process = None
        # --- Worker 停止后隐藏进度界面 ---
        self.task_progress_label.grid_remove()
        self.task_progress_bar.grid_remove()
        self._update_all_controls_state() # 将界面更新为“空闲”状态

    # --- Worker 进度跟踪 ---
    def _process_worker_output(self, line):
        """解析 Worker 标准输出中的一行，以更新任务进度。"""
        # 进度解析必须使用原始英文；显示时再翻译。
        self.add_log(translate_worker_output(line), level="WORKER")

        # 检测开始游戏数和总游戏数
        # 格式：Started game X of Y ...
        match_start = re.search(r"^Started game (\d+) of (\d+)", line)
        if match_start:
            game_num = int(match_start.group(1))
            total_games = int(match_start.group(2))

            self.task_total_games = total_games

            # 如果是第 1 局，重置计时器以计算预计剩余时间。
            # 如果从第 50 局恢复，则不重置计时器，否则预计时间会不准确。
            if game_num == 1:
                self.task_current_games = 0
                self.task_start_time = time.time()
                self._update_progress_display()

            return

        # 检测任务进度
        # 格式：Games: N, Wins: ...
        match_progress = re.search(r"^Games: (\d+), Wins:", line)
        if match_progress:
            self.task_current_games = int(match_progress.group(1))
            self._update_progress_display()

    # --- 包含预计剩余时间的显示逻辑 ---
    def _update_progress_display(self):
        """根据当前状态更新进度条和标签，包括预计剩余时间。"""
        if self.task_total_games > 0:
            progress = self.task_current_games / self.task_total_games
            self.task_progress_bar.set(progress)

            base_text = t("progress.task", current=self.task_current_games, total=self.task_total_games)
            eta_text = ""

            # 如果任务已开始且仍在进行，则计算预计剩余时间
            if self.task_start_time and self.task_current_games > 0 and self.task_current_games < self.task_total_games:
                elapsed_seconds = time.time() - self.task_start_time
                if elapsed_seconds > 1: # 避免除零和初始阶段数值波动
                    games_per_second = self.task_current_games / elapsed_seconds
                    remaining_games = self.task_total_games - self.task_current_games
                    remaining_seconds = remaining_games / games_per_second

                    if remaining_seconds < 60:
                        eta_text = t("progress.eta_seconds", value=int(remaining_seconds))
                    else:
                        remaining_minutes = remaining_seconds / 60
                        eta_text = t("progress.eta_minutes", value=int(remaining_minutes))

            elif self.task_current_games == self.task_total_games:
                eta_text = t("progress.finished")

            self.task_progress_label.configure(text=base_text + eta_text)
        else:
            # Worker 启动时已处理此情况，但这里保留兜底逻辑
            self.task_progress_bar.set(0)
            self.task_progress_label.configure(text="")

    # --- 线程与工具函数 ---
    def _run_command_in_thread(self, command, start_message="", end_message="", on_complete=None):
        def run():
            self.is_long_operation_running = True
            self.after(0, self._update_all_controls_state)
            self.after(0, self.status_label.configure, {"text": t("status.operation", operation=start_message.replace('---', '').strip())})
            if start_message: self.after(0, self.add_log, start_message)
            try:
                process = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding='utf-8', errors='replace', shell=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                for line in iter(process.stdout.readline, ''):
                    self.after(0, self.add_log, line.strip(), "CMD")
                rc = process.wait()
                if end_message: self.after(0, self.add_log, end_message)
                if rc == 0:
                    if on_complete: self.after(0, on_complete)
                else:
                    self.after(0, self.add_log, t("log.process_failed", code=rc), "ERROR")
            except Exception as e:
                self.after(0, self.add_log, t("log.command_failed", error=e), "FATAL")
            finally:
                self.is_long_operation_running = False
                self.after(0, self._update_all_controls_state)
        threading.Thread(target=run, daemon=True).start()

    def _open_settings_window(self):
        win = ctk.CTkToplevel(self)
        win.title(t("settings.title")); win.geometry("400x470"); win.transient(self); win.grab_set()

        ctk.CTkLabel(win, text=t("settings.username")).pack(pady=(10,0))
        user_entry = ctk.CTkEntry(win, width=250); user_entry.pack()

        ctk.CTkLabel(win, text=t("settings.password")).pack(pady=(10,0))
        pass_entry = ctk.CTkEntry(win, show="*", width=250); pass_entry.pack()

        ctk.CTkLabel(win, text=t("settings.concurrency")).pack(pady=(10,0))
        cores_entry = ctk.CTkEntry(win, width=250); cores_entry.pack()

        ctk.CTkLabel(win, text=t("settings.github_token")).pack(pady=(10,0))
        token_entry = ctk.CTkEntry(win, width=250); token_entry.pack()

        ctk.CTkLabel(win, text=t("settings.language")).pack(pady=(10,0))
        language_values = [language_name(language) for language in supported_languages()]
        language_menu = ctk.CTkComboBox(win, values=language_values, width=250)
        language_menu.pack()
        language_menu.set(language_name(get_language()))

        user_entry.insert(0, self.config.get('login', 'username'))
        pass_entry.insert(0, self.config.get('login', 'password'))
        cores_entry.insert(0, self.config.get('parameters', 'concurrency'))
        token_entry.insert(0, self.config.get('Fishtest', 'github_token', fallback=''))

        def save():
            self.config.set('login', 'username', user_entry.get())
            self.config.set('login', 'password', pass_entry.get())
            self.config.set('parameters', 'concurrency', cores_entry.get())
            if not self.config.has_section('Fishtest'):
                self.config.add_section('Fishtest')
            self.config.set('Fishtest', 'github_token', token_entry.get())
            selected_language = next(
                (language for language in supported_languages()
                 if language_name(language) == language_menu.get()),
                "zh_CN"
            )
            if not self.config.has_section('general'):
                self.config.add_section('general')
            self.config.set('general', 'language', selected_language)
            set_language(selected_language)
            self._save_config()
            self._refresh_ui_text()
            win.destroy()
        ctk.CTkButton(win, text=t("settings.save"), command=save).pack(pady=20)

        register_label = ctk.CTkLabel(win, text=t("settings.register"), fg_color="transparent", text_color="#33a2ff", cursor="hand2")
        register_label.pack(pady=(0, 0))
        register_label.bind("<Button-1>", lambda e: webbrowser.open("https://tests.stockfishchess.org/signup"))

    def add_log(self, message, level="INFO"):
        # 检查用户是否正在查看历史记录（已向上滚动）
        is_at_bottom = self.log_text.yview()[1] == 1.0

        self.log_text.configure(state='normal')

        timestamp = time.strftime("[%H:%M:%S]")

        # 确定标签并格式化日志级别
        level_str = level.upper()
        tag = level_str
        
        # 计算实际显示宽度（中文字符占 2 个宽度，英文/数字占 1 个）
        localized = localized_level(level)
        display_width = sum(2 if '\u4e00' <= c <= '\u9fff' else 1 for c in localized)
        padding = max(0, 7 - display_width)
        padded_level = f"[{localized}{' ' * padding}]"

        # 插入时间戳
        self.log_text.insert(ctk.END, timestamp + " ", "TIMESTAMP")

        # 插入日志级别
        self.log_text.insert(ctk.END, padded_level, tag)
        self.log_text.insert(ctk.END, " ")

        # 插入消息
        self.log_text.insert(ctk.END, message + '\n')

        self.log_text.configure(state='disabled')

        # 只有原本位于底部时才自动滚动到底部
        if is_at_bottom:
            self.log_text.yview(ctk.END)

    def _on_closing(self):
        if self.worker_process and self.worker_process.poll() is None:
            if tkinter.messagebox.askyesno(t("dialog.exit.title"), t("dialog.exit.message")):
                self._stop_worker_forcefully()
                self.destroy()
        else:
            self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = FishtestManagerApp()

    # 检查重新启动参数，以自动执行管理员操作
    run_action = None
    for arg in sys.argv:
        if arg.startswith('--run-as-admin='):
            run_action = arg.split('=', 1)[1]
            break

    if run_action:
        # 延迟执行操作，以便窗口先完成初始化
        if run_action == 'install':
            app.after(100, app._run_full_setup)
        elif run_action == 'update':
            app.after(100, app._update_msys2)
        elif run_action == 'delete_worker':
            app.after(100, app._delete_worker_folder)
        elif run_action == 'uninstall_msys2':
            app.after(100, app._uninstall_msys2)

    app.mainloop()
