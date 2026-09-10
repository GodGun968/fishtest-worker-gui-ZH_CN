"""桌面应用的轻量级、无依赖本地化工具。

Worker 本身及其调用的命令行工具拥有自己的输出格式。本模块只翻译
图形界面生成的文本，因此 Worker 协议、命令参数、文件名和配置键保持不变。
"""

LANGUAGE_NAMES = {
    "zh_CN": "简体中文",
    "en_US": "English",
}

LOG_LEVEL_NAMES = {
    "zh_CN": {
        "INFO": "信息",
        "WARNING": "警告",
        "ERROR": "错误",
        "SUCCESS": "成功",
        "FATAL": "致命",
        "DEBUG": "调试",
        "WORKER": "Worker",
        "CMD": "命令",
    },
    "en_US": {},
}

TRANSLATIONS = {
    "zh_CN": {
        "app.window_title": "Fishtest Worker 管理器 i18n版 ({version})",
        "button.install": "安装/重新安装 Worker",
        "button.update_msys2": "更新 MSYS2 环境",
        "button.settings": "设置",
        "button.uninstall": "卸载...",
        "button.new_version": "有新版本可用！",
        "button.new_version_tag": "有新版本可用：{version}",
        "button.start_worker": "启动 Worker",
        "button.stop_worker": "停止 Worker",
        "button.stopping_worker": "正在停止...",
        "button.delete_worker": "删除 Worker 文件夹",
        "button.uninstall_msys2": "卸载 MSYS2",
        "button.uninstall_disabled": "卸载",
        "status.initializing": "状态：正在初始化...",
        "status.idle": "状态：空闲 | 用户：{user} | 核心数：{cores}",
        "status.running": "状态：运行中 | 用户：{user} | 核心数：{cores}",
        "status.operation": "状态：{operation}...",
        "progress.task": "任务进度：{current} / {total}",
        "progress.eta_seconds": "（预计剩余：{value} 秒）",
        "progress.eta_minutes": "（预计剩余：{value} 分钟）",
        "progress.finished": "（已完成）",
        "log.settings_saved": "设置已保存至 {file}。",
        "log.save_permission": "设置保存失败：没有权限写入 {file}。",
        "log.save_io": "设置保存失败：发生意外的输入/输出错误：{error}",
        "log.msys2_missing": "未找到 MSYS2。请运行“安装/重新安装 Worker”。",
        "log.worker_missing": "已找到 MSYS2，但缺少 Worker 文件。请运行“安装/重新安装 Worker”完成设置。",
        "log.setup_complete": "环境已完整设置。",
        "log.settings_required": "启动 Worker 前，请打开“设置”并填写 Fishtest 用户名和密码，然后点击“启动 Worker”。",
        "log.worker_ready": "现在可以点击“启动 Worker”运行任务。",
        "log.update_rate_limit": "已跳过应用更新检查（GitHub API 已达到速率限制）。",
        "log.update_http_failed": "应用更新检查失败（HTTP {code}）。",
        "log.update_network_failed": "应用更新检查失败。启动 Worker 前请检查网络连接。（{error}）",
        "log.latest_version": "当前已是最新版本（{version}）。",
        "log.new_version": "管理器有新版本可用（{version}）。",
        "dialog.elevation_failed.title": "提权失败",
        "dialog.elevation_failed.message": "无法以管理员权限重新启动程序：{error}",
        "dialog.install.title": "确认安装",
        "dialog.install.message": "此操作将安装 MSYS2 环境并下载 Fishtest Worker 文件。\n可能需要几分钟。\n\n注意：当前目录中的“worker”文件夹（如有）将被删除并替换。\n\n是否继续？",
        "log.install_start": "--- 开始安装 MSYS2 ---",
        "log.install_end": "--- MSYS2 安装完成 ---",
        "log.worker_install_start": "--- 开始安装 Worker 文件和依赖 ---",
        "log.worker_install_end": "--- Worker 安装完成 ---",
        "log.msys2_update_start": "--- 开始更新 MSYS2 环境 ---",
        "log.msys2_update_end": "--- MSYS2 更新完成 ---",
        "dialog.delete.title": "确认删除",
        "dialog.delete.message": "警告：此操作具有破坏性。\n\n此操作将永久删除“worker”文件夹及其全部内容，包括配置文件。\n\n确定要继续吗？",
        "log.delete_start": "--- 开始删除 Worker 文件夹 ---",
        "log.delete_end": "--- Worker 文件夹已删除 ---",
        "dialog.uninstall.title": "确认卸载",
        "dialog.uninstall.message": "警告：此操作具有破坏性。\n\n此操作将运行 MSYS2 卸载程序并删除整个 MSYS2 环境。\n\n确定要继续吗？",
        "log.uninstall_start": "--- 开始卸载 MSYS2 ---",
        "log.uninstall_end": "--- MSYS2 卸载完成 ---",
        "log.github_token_saved": "已为 GitHub API 身份验证创建/更新“{file}”。",
        "log.github_token_failed": "创建 _netrc 文件失败：{error}",
        "log.start_attempt": "正在尝试启动 Worker...",
        "log.exit_cleaned": "已清理遗留的 {file} 文件。",
        "log.exit_cleanup_failed": "无法清理遗留的 {file} 文件。Worker 可能无法正常启动：{error}",
        "log.worker_start_failed": "Worker 启动失败：{error}",
        "log.worker_not_running": "Worker 当前未运行。",
        "log.wrapper_dead": "Worker 包装进程已结束，正在尝试停止 Worker。",
        "log.stopping_gracefully": "正在正常停止 Worker...（正在创建 {file} 文件）",
        "log.exit_create_failed": "无法创建 {file} 文件：{error}。可以尝试右键强制停止。",
        "dialog.force_stop.title": "强制停止",
        "dialog.force_stop.message": "确定要强制停止 Worker 吗？当前游戏进度可能会丢失。",
        "log.force_stopping": "正在强制停止 Worker...",
        "log.taskkill_failed": "taskkill 失败（进程可能已经结束）：{error}",
        "log.terminate_failed": "内部 terminate() 调用失败（已忽略）：{error}",
        "log.worker_stopped": "Worker 进程已停止。",
        "log.process_failed": "进程以非零退出代码结束：{code}",
        "log.command_failed": "执行命令时出错：{error}",
        "command.removing_worker": "正在删除 Worker 文件夹...",
        "command.worker_not_found": "未找到 Worker 文件夹。",
        "command.uninstalling_msys2": "正在卸载 MSYS2...",
        "command.msys2_not_found": "未找到 MSYS2。",
        "settings.title": "设置",
        "settings.username": "Fishtest 用户名：",
        "settings.password": "Fishtest 密码：",
        "settings.concurrency": "并发数（核心数）：",
        "settings.github_token": "GitHub Personal Access Token（可选）：",
        "settings.language": "界面语言：",
        "settings.language_zh_CN": "简体中文",
        "settings.language_en_US": "English",
        "settings.save": "保存",
        "settings.register": "还没有账号？点击此处注册！",
        "dialog.exit.title": "退出",
        "dialog.exit.message": "Worker 仍在运行。要强制停止并退出吗？",
    },
    "en_US": {
        "app.window_title": "Fishtest Worker Manager ({version})",
        "button.install": "Install/Re-Install Worker",
        "button.update_msys2": "Update MSYS2 Environment",
        "button.settings": "Settings",
        "button.uninstall": "Uninstall...",
        "button.new_version": "New Version Available!",
        "button.new_version_tag": "New Version Available: {version}",
        "button.start_worker": "START WORKER",
        "button.stop_worker": "STOP WORKER",
        "button.stopping_worker": "STOPPING...",
        "button.delete_worker": "Delete Worker Folder",
        "button.uninstall_msys2": "Uninstall MSYS2",
        "button.uninstall_disabled": "Uninstall",
        "status.initializing": "Status: Initializing...",
        "status.idle": "Status: Idle | User: {user} | Cores: {cores}",
        "status.running": "Status: Running | User: {user} | Cores: {cores}",
        "status.operation": "Status: {operation}...",
        "progress.task": "Task Progress: {current} / {total}",
        "progress.eta_seconds": " (ETA: {value}s)",
        "progress.eta_minutes": " (ETA: {value}m)",
        "progress.finished": " (Finished)",
        "log.settings_saved": "Settings saved to {file}.",
        "log.save_permission": "Failed to save settings. Permission denied writing to {file}.",
        "log.save_io": "Failed to save settings due to an unexpected IO error: {error}",
        "log.msys2_missing": "MSYS2 not found. Please run 'Install/Re-Install Worker'.",
        "log.worker_missing": "MSYS2 found, but worker files are missing. Run 'Install/Re-Install Worker' to set them up.",
        "log.setup_complete": "Full environment setup is complete.",
        "log.settings_required": "Before starting the worker, open 'Settings' and enter your Fishtest username and password. Then, click 'START WORKER'.",
        "log.worker_ready": "You may now start the worker by clicking 'START WORKER'.",
        "log.update_rate_limit": "App update check skipped (GitHub API rate limit exceeded).",
        "log.update_http_failed": "App update check failed (HTTP {code}).",
        "log.update_network_failed": "App update check failed. Check your internet connection before running the worker. ({error})",
        "log.latest_version": "You are using the latest version of the app ({version}).",
        "log.new_version": "A new version of the Manager is available ({version}).",
        "dialog.elevation_failed.title": "Elevation Failed",
        "dialog.elevation_failed.message": "Could not re-launch with admin rights: {error}",
        "dialog.install.title": "Confirm Installation",
        "dialog.install.message": "This will install the MSYS2 environment and download the fishtest worker files.\nThis may take several minutes.\n\nNote: Any existing 'worker' folder in this directory will be deleted and replaced.\n\nContinue?",
        "log.install_start": "--- Starting MSYS2 Installation ---",
        "log.install_end": "--- MSYS2 Installation finished ---",
        "log.worker_install_start": "--- Installing worker files and dependencies ---",
        "log.worker_install_end": "--- Worker installation finished ---",
        "log.msys2_update_start": "--- Updating MSYS2 environment ---",
        "log.msys2_update_end": "--- MSYS2 Update finished ---",
        "dialog.delete.title": "Confirm Deletion",
        "dialog.delete.message": "WARNING: This is a destructive action.\n\nThis will permanently delete the 'worker' folder and all its contents, including your configuration file.\n\nAre you sure you want to continue?",
        "log.delete_start": "--- Deleting worker folder ---",
        "log.delete_end": "--- Worker folder deleted ---",
        "dialog.uninstall.title": "Confirm Uninstallation",
        "dialog.uninstall.message": "WARNING: This is a destructive action.\n\nThis will run the MSYS2 uninstaller and remove the entire MSYS2 environment.\n\nAre you sure you want to continue?",
        "log.uninstall_start": "--- Starting MSYS2 Uninstallation ---",
        "log.uninstall_end": "--- MSYS2 Uninstallation finished ---",
        "log.github_token_saved": "Created/Updated '{file}' for GitHub API authentication.",
        "log.github_token_failed": "Failed to create _netrc file: {error}",
        "log.start_attempt": "Attempting to start the worker...",
        "log.exit_cleaned": "Cleaned up leftover {file} file.",
        "log.exit_cleanup_failed": "Could not clean up leftover {file} file. The worker may not start correctly: {error}",
        "log.worker_start_failed": "Worker failed to start: {error}",
        "log.worker_not_running": "Worker is not running.",
        "log.wrapper_dead": "Wrapper process is dead. Attempting to stop the worker.",
        "log.stopping_gracefully": "Stopping worker gracefully... (creating {file} file)",
        "log.exit_create_failed": "Could not create {file} file: {error}. Consider a force stop (right-click).",
        "dialog.force_stop.title": "Force Stop",
        "dialog.force_stop.message": "Are you sure you want to force stop the worker? Current game progress may be lost.",
        "log.force_stopping": "Force stopping worker...",
        "log.taskkill_failed": "taskkill failed (process might be dead): {error}",
        "log.terminate_failed": "Internal terminate() failed (ignoring): {error}",
        "log.worker_stopped": "Worker process has stopped.",
        "log.process_failed": "Process finished with non-zero exit code: {code}",
        "log.command_failed": "Error executing command: {error}",
        "command.removing_worker": "Removing Worker folder...",
        "command.worker_not_found": "Worker folder not found.",
        "command.uninstalling_msys2": "Uninstalling MSYS2...",
        "command.msys2_not_found": "MSYS2 not found.",
        "settings.title": "Settings",
        "settings.username": "Fishtest Username:",
        "settings.password": "Fishtest Password:",
        "settings.concurrency": "Concurrency (Cores):",
        "settings.github_token": "GitHub Personal Access Token (Optional):",
        "settings.language": "Interface language:",
        "settings.language_zh_CN": "简体中文",
        "settings.language_en_US": "English",
        "settings.save": "Save",
        "settings.register": "Don't have an account? Register here!",
        "dialog.exit.title": "Exit",
        "dialog.exit.message": "The worker is still running. Do you want to force stop it and exit?",
    },
}

_current_language = "zh_CN"


def supported_languages():
    return tuple(TRANSLATIONS.keys())


def get_language():
    return _current_language


def set_language(language):
    """选择支持的语言，并返回实际选中的语言。"""
    global _current_language
    if language not in TRANSLATIONS:
        language = "zh_CN"
    _current_language = language
    return _current_language


def language_name(language):
    return LANGUAGE_NAMES.get(language, language)


def localized_level(level):
    level = level.upper()
    return LOG_LEVEL_NAMES.get(_current_language, {}).get(level, level)


def t(key, **kwargs):
    """返回本地化字符串；缺少翻译键时回退到英文。"""
    text = TRANSLATIONS.get(_current_language, {}).get(key)
    if text is None:
        text = TRANSLATIONS["en_US"].get(key, key)
    return text.format(**kwargs) if kwargs else text
