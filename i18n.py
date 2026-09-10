"""桌面应用的轻量级、无依赖本地化工具。

Worker 协议、命令参数、文件名和配置键保持不变。Worker 原始英文输出
仍用于进度解析；简体中文界面会在显示前翻译常见日志。
"""

import re

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
        "app.window_title": "Fishtest Worker 管理器 I18N ({version})",
        "button.install": "安装/重新安装 Worker",
        "button.update_msys2": "更新 MSYS2 环境",
        "button.settings": "设置",
        "button.uninstall": "卸载……",
        "button.new_version": "有新版本可用！",
        "button.new_version_tag": "有新版本可用：{version}",
        "button.start_worker": "启动 Worker",
        "button.stop_worker": "停止 Worker",
        "button.stopping_worker": "正在停止……",
        "button.delete_worker": "删除 Worker 文件夹",
        "button.uninstall_msys2": "卸载 MSYS2",
        "button.uninstall_disabled": "卸载",
        "status.initializing": "状态：正在初始化……",
        "status.idle": "状态：空闲 | 用户：{user} | 核心数：{cores}",
        "status.running": "状态：运行中 | 用户：{user} | 核心数：{cores}",
        "status.operation": "状态：{operation}……",
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
        "log.start_attempt": "正在尝试启动 Worker……",
        "log.exit_cleaned": "已清理遗留的 {file} 文件。",
        "log.exit_cleanup_failed": "无法清理遗留的 {file} 文件。Worker 可能无法正常启动：{error}",
        "log.worker_start_failed": "Worker 启动失败：{error}",
        "log.worker_not_running": "Worker 当前未运行。",
        "log.wrapper_dead": "Worker 包装进程已结束，正在尝试停止 Worker。",
        "log.stopping_gracefully": "正在正常停止 Worker……（正在创建 {file} 文件）",
        "log.exit_create_failed": "无法创建 {file} 文件：{error}。可以尝试右键强制停止。",
        "dialog.force_stop.title": "强制停止",
        "dialog.force_stop.message": "确定要强制停止 Worker 吗？当前游戏进度可能会丢失。",
        "log.force_stopping": "正在强制停止 Worker……",
        "log.taskkill_failed": "taskkill 失败（进程可能已经结束）：{error}",
        "log.terminate_failed": "内部 terminate() 调用失败（已忽略）：{error}",
        "log.worker_stopped": "Worker 进程已停止。",
        "log.process_failed": "进程以非零退出代码结束：{code}",
        "log.command_failed": "执行命令时出错：{error}",
        "command.removing_worker": "正在删除 Worker 文件夹……",
        "command.worker_not_found": "未找到 Worker 文件夹。",
        "command.uninstalling_msys2": "正在卸载 MSYS2……",
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


_STAT_LABELS = {
    "Concurrency": "并发数",
    "Threads": "线程数",
    "Hash": "哈希",
    "Depth": "深度",
    "Mean nodes": "平均节点数",
    "Mean time (ms)": "平均用时（毫秒）",
    "Mean nps": "平均 NPS",
    "Min nps": "最低 NPS",
    "Max nps": "最高 NPS",
    "Stdev (%)": "标准差（%）",
}

_RESULT_REASONS = {
    "Draw by insufficient mating material": "因子力不足判和",
    "Draw by 3-fold repetition": "因三次重复局面判和",
    "Draw by fifty moves rule": "因五十步规则判和",
    "Draw by stalemate": "因逼和判和",
    "Draw by adjudication": "经裁决判和",
    "Draw by agreement": "双方同意和棋",
    "Draw by timeout vs insufficient mating material": "超时但对面子力不足，判和",
    "White wins by adjudication": "白方经裁决获胜",
    "Black wins by adjudication": "黑方经裁决获胜",
    "White wins by checkmate": "白方将杀获胜",
    "Black wins by checkmate": "黑方将杀获胜",
    "White wins on time": "白方超时获胜",
    "Black wins on time": "黑方超时获胜",
    "White wins by resignation": "白方因对方认输获胜",
    "Black wins by resignation": "黑方因对方认输获胜",
    "White wins by illegal move": "白方因对方非法着法获胜",
    "Black wins by illegal move": "黑方因对方非法着法获胜",
    "White wins by disconnect": "白方因对方断线获胜",
    "Black wins by disconnect": "黑方因对方断线获胜",
}

_WORKER_LINE_PATTERNS = (
    (r"^The prefix (.+) is too short\.$", "前缀 {0} 过短。"),
    (r"^Unable to parse expression for max_memory\.$", "无法解析 max_memory 表达式。"),
    (r"^Unable to parse expression for concurrency\.$", "无法解析 concurrency 表达式。"),
    (r"^concurrency must be at least 1\.$", "concurrency 至少为 1。"),
    (r"^You cannot have concurrency (.+) but at most:$", "concurrency 不能为 {0}，最多只能为："),
    (r"^Sleep interrupted\.\.\.$", "睡眠被中断……"),
    (r"^Exception computing sri hash of (.+):\s*(.+)$", "计算 {0} 的 sri 哈希时出错：{1}"),
    (r"^Writing sri hashes to (.+)\.$", "正在将 sri 哈希写入 {0}。"),
    (r"^Exception reading (.+):\s*(.+)$", "读取 {0} 时出错：{1}"),
    (r"^The file (.+) does not contain a dictionary\.$", "文件 {0} 不含字典。"),
    (r"^The value for (.+) is incorrect in (.+)\.$", "{1} 中 {0} 的值不正确。"),
    (r"^The file (.+) matches the worker files!$", "文件 {0} 与 Worker 文件匹配！"),
    (r"^The master sri file has a different version number\. Ignoring!$",
     "主 sri 文件版本号不同，已忽略！"),
    (r"^(.+) has been modified!$", "{0} 已被修改！"),
    (r"^This worker is tainted\.\.\.$", "此 Worker 已被修改……"),
    (r"^Running an unmodified worker\.\.\.$", "正在运行未修改的 Worker……"),
    (r"^Confirming (cached|supplied) credentials with (.+)\.$", "正在向 {1} 确认{0}凭据。"),
    (r"^Credentials ok!$", "凭据验证通过！"),
    (r"^Worker version (.+) connecting to (.+)\.$", "Worker 版本 {0} 正在连接 {1}。"),
    (r"^Obtaining version info for (.+)\.\.\.$", "正在获取 {0} 的版本信息……"),
    (r"^Found (fastchess .+)$", "已找到 {0}"),
    (r"^Running fastchess raised (.+): (.+)$", "运行 fastchess 引发 {0}：{1}"),
    (r"^Unable to run fastchess\. Return code: (.+)\. Error: (.+)$",
     "无法运行 fastchess。返回代码：{0}。错误：{1}"),
    (r"^Unable to find a suitable sha of length 7 or more in the fastchess version\.$",
     "在 fastchess 版本信息中找不到长度至少为 7 的合适 sha。"),
    (r"^fastchess sha (.+) required but the version shows (.+)\.$",
     "需要 fastchess sha {0}，但版本显示为 {1}。"),
    (r"^Removing fastchess raised (.+): (.+)$", "删除 fastchess 引发 {0}：{1}"),
    (r"^Building fastchess from sources\.\.\.$", "正在从源码构建 fastchess……"),
    (r"^Downloading (.+) failed: (.+)\. Trying the GitHub api\.$",
     "下载 {0} 失败：{1}。正在尝试 GitHub API。"),
    (r"^Downloading (.+)\.\.\.$", "正在下载 {0}……"),
    (r"^Downloading (.+)\.$", "正在下载 {0}。"),
    (r"^Using (.+) from global cache\.$", "正在使用全局缓存中的 {0}。"),
    (r"^Exception downloading, extracting or building fastchess:\s*(.+)$",
     "下载、解压或构建 fastchess 时出错：{0}"),
    (r"^Replacing the value '(.+)' of config option '(.+)' by '(.+)'\.$",
     "配置项“{1}”的值“{0}”已替换为“{2}”。"),
    (r"^The value '(.+)' of config option '(.+)' is not of type '(.+)'\.\s*Replacing it by the default value '(.+)'\.$",
     "配置项“{1}”的值“{0}”不是“{2}”类型。已替换为默认值“{3}”。"),
    (r"^The value '(.+)' of config option '(.+)' is not in (.+)\.\s*Replacing it by the default value '(.+)'\.$",
     "配置项“{1}”的值“{0}”不在 {2} 中。已替换为默认值“{3}”。"),
    (r"^Removing unknown config section '(.+)'\.$", "正在删除未知配置节“{0}”。"),
    (r"^Removing unknown config option '(.+)'\.$", "正在删除未知配置项“{0}”。"),
    (r"^Exception reading configfile (.+):\s*(.+)$", "读取配置文件 {0} 时出错：{1}"),
    (r"^Initializing configfile\.\.\.$", "正在初始化配置文件……"),
    (r"^Unknown system\.$", "未知系统。"),
    (r"^Exception checking HW info:\s*(.+)$", "检查硬件信息时出错：{0}"),
    (r"^Exception checking the CPU cores count:\s*(.+)$", "检查 CPU 核心数时出错：{0}"),
    (r"^No usable compilers found\.$", "未找到可用编译器。"),
    (r"^Unparsed command line arguments: (.+)$", "未解析的命令行参数：{0}"),
    (r"^Changing port to (\d+)\.$", "正在将端口改为 {0}。"),
    (r"^You need to reserve at least (.+) MiB to run the worker!$",
     "运行 Worker 至少需要预留 {0} MiB 内存！"),
    (r"^Changing concurrency to allow for running STC tests with the available memory\.$",
     "正在根据可用内存调整并发数，以便运行 STC 测试。"),
    (r"^The required memory to run with (\d+) concurrency is (.+)\.$",
     "以 {0} 并发运行所需内存为 {1}。"),
    (r"^The concurrency has been reduced to (\d+)\.$", "并发数已降至 {0}。"),
    (r"^Consider increasing max_memory if possible\.$", "如有可能，请考虑提高 max_memory。"),
    (r"^Default uuid_prefix: (.+)$", "默认 uuid_prefix：{0}"),
    (r"^Invalid or missing credentials\.$", "凭据无效或缺失。"),
    (r"^System memory determined to be: (.+)\.$", "系统内存检测为：{0}。"),
    (r"^Worker constraints: (.+)$", "Worker 约束：{0}"),
    (r"^Config file (.+) written\.$", "配置文件已写入 {0}。"),
    (r"^machine_id (.+) obtained from (.+)\.$", "machine_id {0} 取自 {1}。"),
    (r"^machine_id (.+) obtained via '(.+)'\.$", "machine_id {0} 通过“{1}”获得。"),
    (r"^Exception while reading the machine_id:\s*(.+)$", "读取 machine_id 时出错：{0}"),
    (r"^Unable to obtain the machine id\.$", "无法获取机器 ID。"),
    (r"^Exception fetching rate_limit \(invalid ~/.netrc\?\):\s*(.+)$",
     "获取 rate_limit 时出错（~/.netrc 可能无效）：{0}"),
    (r"^clang\+\+ poses as g\+\+\.$", "clang++ 伪装成 g++。"),
    (r"^No g\+\+ or g\+\+ is not executable\.$", "未找到 g++，或其不可执行。"),
    (r"^g\+\+ version query failed with return code (.+)\.$", "查询 g++ 版本失败，返回代码 {0}。"),
    (r"^Failed to parse g\+\+ version\.$", "解析 g++ 版本失败。"),
    (r"^Found g\+\+ version (.+)\. First usable version is (.+)\.$",
     "已找到 g++ 版本 {0}。最低可用版本为 {1}。"),
    (r"^No clang\+\+ or clang\+\+ is not executable\.$", "未找到 clang++，或其不可执行。"),
    (r"^clang\+\+ version query failed with return code (.+)\.$", "查询 clang++ 版本失败，返回代码 {0}。"),
    (r"^Failed to parse clang\+\+ version\.$", "解析 clang++ 版本失败。"),
    (r"^Found clang\+\+ version (.+)\. First usable version is (.+)\.$",
     "已找到 clang++ 版本 {0}。最低可用版本为 {1}。"),
    (r"^clang\+\+ is present but misconfigured: the command 'llvm-profdata' is missing\.$",
     "已找到 clang++，但配置不正确：缺少命令“llvm-profdata”。"),
    (r"^Found (.+) version (.+)\.$", "已找到 {0} 版本 {1}。"),
    (r"^Toolchain check\.\.\.$", "正在检查工具链……"),
    (r"^'(.+)' returned code: (.+) and error: (.+)$", "“{0}”返回代码：{1}，错误：{2}"),
    (r"^'(.+)' raised: (.+): (.+)$", "“{0}”引发 {1}：{2}"),
    (r"^Missing required tools: (.+)$", "缺少必需工具：{0}"),
    (r"^Worker arch determined to be: (.+)$", "Worker 架构检测为：{0}"),
    (r"^Exception obtaining worker arch:\s*(.+)$", "获取 Worker 架构时出错：{0}"),
    (r'^Unable to determine worker arch\. Setting it to "unknown"$',
     "无法确定 Worker 架构，已设为“unknown”。"),
    (r"^Start heartbeat\.$", "开始心跳。"),
    (r"^Send heartbeat for (.+)\.\.\.\s*\(received\)$", "正在为 {0} 发送心跳……（已收到）"),
    (r"^Send heartbeat for (.+)\.\.\.$", "正在为 {0} 发送心跳……"),
    (r"^Skipping heartbeat\.\.\.$", "正在跳过心跳……"),
    (r"^Exception calling heartbeat:\s*(.+)$", "调用心跳时出错：{0}"),
    (r"^\(received\)$", "（已收到）"),
    (r"^The server told us that no more games are needed for the current task\.$",
     "服务器告知当前任务不再需要更多对局。"),
    (r"^Heartbeat stopped\.$", "心跳已停止。"),
    (r"^Verify worker version\.\.\.$", "正在验证 Worker 版本……"),
    (r"^Updating worker version to (.+)\.$", "正在将 Worker 版本更新到 {0}。"),
    (r"^Exception while updating to version (.+):\s*(.+)$", "更新到版本 {0} 时出错：{1}"),
    (r"^Attempted update to worker version (.+) failed!$", "尝试更新到 Worker 版本 {0} 失败！"),
    (r"^Current time is (.+) UTC \(local offset: (.+)\)\.$", "当前时间为 {0} UTC（本地时差：{1}）。"),
    (r"^Remaining number of GitHub api calls = (\d+)\.$", "剩余 GitHub API 调用次数 = {0}。"),
    (r"^We have almost exhausted our GitHub api calls\.$", "GitHub API 调用次数即将用尽。"),
    (r"^The server will only give us tasks for tests we have seen before\.$",
     "服务器只会分配我们曾经见过的测试任务。"),
    (r"^Fetching task\.\.\.$", "正在获取任务……"),
    (r"^No tasks available at this time, waiting\.\.\.$", "当前没有可用任务，正在等待……"),
    (r"^Working on task (.+) from (.+)\.$", "正在处理来自 {1} 的任务 {0}。"),
    (r"^run: (.+) task: (.+) size: (.+) tc: (.+) concurrency: (.+) threads: (.+) \[ (.+) : (.+) \]$",
     "运行：{0} 任务：{1} 规模：{2} 时间控制：{3} 并发：{4} 线程：{5} [ {6} : {7} ]"),
    (r"^Running (.+) vs (.+)\.$", "正在运行 {0} 对阵 {1}。"),
    (r"^Exception running games:\s*(.+)$", "运行对局时出错：{0}"),
    (r"^Informing the server\.$", "正在通知服务器。"),
    (r"^Exception posting failed_task:\s*(.+)$", "提交 failed_task 时出错：{0}"),
    (r"^Uploading compressed PGN of (\d+) bytes\.$", "正在上传压缩 PGN，大小 {0} 字节。"),
    (r"^Task exited\.?$", "任务已退出。"),
    (r"^Checksum of file \((.+)\) does not match expected value \((.+)\)\.\s*Skipping upload\.$",
     "文件校验和（{0}）与期望值（{1}）不符。已跳过上传。"),
    (r"^Exception uploading PGN file:\s*(.+)$", "上传 PGN 文件时出错：{0}"),
    (r"^\*\*\* Another worker \(with PID=(.+)\) is already running in this directory\. \*\*\*$",
     "*** 此目录中已有另一个 Worker 正在运行（PID={0}）。***"),
    (r"^\*\*\* Unexpected exception: (.+) \*\*\*$", "*** 意外异常：{0} ***"),
    (r"^Worker started in (.+) with PID=(.+)\.$", "Worker 已在 {0} 启动，PID={1}。"),
    (r"^Error parsing options\. Config file not written\.$", "解析选项出错。未写入配置文件。"),
    (r"^Exception verifying worker version:\s*(.+)$", "验证 Worker 版本时出错：{0}"),
    (r"^Using (.+) (\d+\.\d+\.\d+)\.$", "使用 {0} {1}。"),
    (r"^UUID:\s*(.+)$", "UUID：{0}"),
    (r"^Stopped by 'fish\.exit' file\.$", "已因 fish.exit 文件停止。"),
    (r"^Exiting the worker since fleet==True and an error occurred\.$",
     "因 fleet==True 且发生错误，正在退出 Worker。"),
    (r"^Waiting (.+) seconds before retrying\.$", "将在 {0} 秒后重试。"),
    (r"^Removing fish\.exit file\.$", "正在删除 fish.exit 文件。"),
    (r"^Releasing the worker lock\.$", "正在释放 Worker 锁。"),
    (r"^Waiting for the heartbeat thread to finish\.\.\.$", "正在等待心跳线程结束……"),
    (r"^Moving logfile (.+) to (.+)\.$", "正在将日志文件 {0} 移动到 {1}。"),
    (r"^Exception moving log:\s*(.+)$", "移动日志时出错：{0}"),
    (r"^Failed to update the atime of (.+):\s*(.+)$", "更新 {0} 的访问时间失败：{1}"),
    (r"^Failed to preserve/delete the file (.+):\s*(.+)$", "保留或删除文件 {0} 失败：{1}"),
    (r"^Cleaning up old files: (\d+) old files removed\.\.\.$", "正在清理旧文件：已删除 {0} 个旧文件……"),
    (r"^Exception in requests\.get\(\):\s*(.+)$", "requests.get() 出错：{0}"),
    (r"^Exception in requests\.post\(\):\s*(.+)$", "requests.post() 出错：{0}"),
    (r"^Exception in send_api_post_request\(\):\s*(.+)$", "send_api_post_request() 出错：{0}"),
    (r"^Error from remote: (.+)$", "远程错误：{0}"),
    (r"^Info from remote: (.+)$", "远程信息：{0}"),
    (r"^Post request (.+) handled in (.+) \(server: (.+)\)\.$",
     "POST 请求 {0} 已处理，耗时 {1}（服务器：{2}）。"),
    (r"^Exception while posting to worker log:\s*(.+)$", "写入 Worker 日志时出错：{0}"),
    (r"^Obtaining EvalFile of (.+)\.\.\.$", "正在获取 {0} 的 EvalFile……"),
    (r"^Removing invalid (.+) from global cache\.$", "正在从全局缓存中删除无效的 {0}。"),
    (r"^Failed to fetch (.+) in attempt (\d+), trying in (.+) seconds\.$",
     "第 {1} 次获取 {0} 失败，将在 {2} 秒后重试。"),
    (r"^Warmup for bench\.\.\.$", "正在进行 bench 预热……"),
    (r"^\.\.\.done in (.+)\.$", "……已完成，耗时 {0}。"),
    (r"^Running bench\.\.\.$", "正在运行 bench……"),
    (r"^Statistics for (.+):$", "{0} 的统计信息："),
    (r"^Computing engine signature\.\.\.$", "正在计算引擎签名……"),
    (r"^Exception while executing make help:\s*(.+)$", "执行 make help 时出错：{0}"),
    (r"^Using native target architecture\.$", "正在使用本机目标架构。"),
    (r"^Available Makefile architecture targets: (.+)$", "可用 Makefile 架构目标：{0}"),
    (r"^Available g\+\+/cpu properties: (.+)$", "可用 g++/CPU 属性：{0}"),
    (r"^Determined the best architecture to be (.+)$", "确定的最佳架构为 {0}"),
    (r"^Removing invalid engine (.+)$", "正在删除无效引擎 {0}"),
    (r"^Build uses default net: (.+)$", "构建使用默认网络：{0}"),
    (r"^Killing (.+) with PID (.+)\.\.\.$", "正在终止 {0}（PID {1}）……"),
    (r"^Exception killing (.+) with PID (.+), possibly already terminated:\s*(.+)$",
     "终止 {0}（PID {1}）时出错，进程可能已经结束：{2}"),
    (r"^killed\.$", "已终止。"),
    (r"^CPU factor : (.+) - tc adjusted to (.+)$", "CPU 系数：{0}，时间控制已调整为 {1}"),
    (r"^TC limit (.+) End time: (.+)$", "时间控制上限 {0} 结束时间：{1}"),
    (r"^Indexing opening suite\.\.\.$", "正在为开局库建立索引……"),
    (r"^Started game (\d+) of (\d+) \((.+)\)$", "开始第 {0} / {1} 局（{2}）"),
    (r"^Finished game (\d+) \((.+)\): (.+) \{(.+)\}$", "完成第 {0} 局（{1}）：{2} {{{3}}}"),
    (r"^File (.+) has CRC32: (.+)$", "文件 {0} 的 CRC32：{1}"),
    (r"^Results of (.+) vs (.+) \((.+)\):$", "{0} 对阵 {1} 的结果（{2}）："),
    (r"^Elo: (.+), nElo: (.+)$", "Elo：{0}，nElo：{1}"),
    (r"^LOS: (.+), DrawRatio: (.+), PairsRatio: (.+)$", "LOS：{0}，和棋率：{1}，配对比：{2}"),
    (r"^Games: (\d+), Wins: (\d+), Losses: (\d+), Draws: (\d+), Points: (.+)$",
     "对局：{0}，胜：{1}，负：{2}，和：{3}，得分：{4}"),
    (r"^Ptnml\(0-2\): (.+), WL/DD Ratio: (.+)$", "Ptnml(0-2)：{0}，WL/DD 比：{1}"),
    (r"^Finished match cleanly\.$", "对局已干净结束。"),
    (r"^Exception calling update_task:\s*(.+)$", "调用 update_task 时出错：{0}"),
    (r"^Exception in send_sigint:\s*(.+)$", "发送 SIGINT 时出错：{0}"),
    (r"^Waiting for fastchess to finish\.\.\.$", "正在等待 fastchess 结束……"),
    (r"^timeout$", "超时"),
    (r"^done\.$", "完成。"),
    (r"^Exception starting fastchess:\s*(.+)$", "启动 fastchess 时出错：{0}"),
    (r"^Variable task sizes used\. Opening offset = (.+)\.$", "使用可变任务规模。开局偏移 = {0}。"),
    (r"^Book (.+) has sri (.+) whereas the server says it should be (.+)\.$",
     "开局库 {0} 的 sri 为 {1}，但服务器要求为 {2}。"),
    (r"^Exception computing sri of (.+):\s*(.+)$", "计算 {0} 的 sri 时出错：{1}"),
    (r"^Book (.+) does not exist\.\.\.$", "开局库 {0} 不存在……"),
    (r"^Using book (.+)\.\.\.$", "正在使用开局库 {0}……"),
    (r"^Failed to download (.+):\s*(.+)$", "下载 {0} 失败：{1}"),
    (r"^Failed to delete the folder (.+):\s*(.+)$", "删除文件夹 {0} 失败：{1}"),
    (r"^Failed to remove the old backup folder (.+):\s*(.+)$", "删除旧备份文件夹 {0} 失败：{1}"),
    (r"^start_dir: (.+)$", "起始目录：{0}"),
    (r"^Warning; Engine (.+) is not responsive$", "警告：引擎 {0} 无响应"),
    (r"^Warning; Engine (.+) didn't respond$", "警告：引擎 {0} 未响应"),
    (r"^Warning; No output from (.+)$", "警告：{0} 没有输出"),
    (r"^Warning; No bestmove found from (.+)$", "警告：{0} 未找到最佳着法"),
    (r"^Exception (.+) at (.+) WorkerVersion: (.+)$", "异常 {0}，位置 {1}，Worker 版本：{2}"),
)

_WORKER_PHRASES = (
    ("Draw by insufficient mating material", "因子力不足判和"),
    ("Draw by 3-fold repetition", "因三次重复局面判和"),
    ("Draw by fifty moves rule", "因五十步规则判和"),
    ("Draw by stalemate", "因逼和判和"),
    ("White wins by adjudication", "白方经裁决获胜"),
    ("Black wins by adjudication", "黑方经裁决获胜"),
    ("White wins by checkmate", "白方将杀获胜"),
    ("Black wins by checkmate", "黑方将杀获胜"),
    ("White wins on time", "白方超时获胜"),
    ("Black wins on time", "黑方超时获胜"),
    ("White wins by resignation", "白方因对方认输获胜"),
    ("Black wins by resignation", "黑方因对方认输获胜"),
    ("White wins by illegal move", "白方因对方非法着法获胜"),
    ("Black wins by illegal move", "黑方因对方非法着法获胜"),
    ("White wins by disconnect", "白方因对方断线获胜"),
    ("Black wins by disconnect", "黑方因对方断线获胜"),
    ("Draw by adjudication", "经裁决判和"),
    ("Draw by agreement", "双方同意和棋"),
    ("'concurrency':", "'并发数':"),
    ("'max_memory':", "'最大内存':"),
    ("'min_threads':", "'最少线程':"),
)


_COMPILED_WORKER_LINE_PATTERNS = tuple(
    (re.compile(pattern), template, pattern)
    for pattern, template in _WORKER_LINE_PATTERNS
)
_STAT_PATTERN = re.compile(
    r"^(Concurrency|Threads|Hash|Depth|Mean nodes|Mean time \(ms\)|Mean nps|Min nps|Max nps|Stdev \(%\))(\s*:\s*)(.+)$"
)


def translate_worker_output(line):
    """将 Worker 日志翻译为当前界面语言；英文界面原样返回。

    进度解析必须使用原始英文行。本函数只用于显示。
    """
    if _current_language != "zh_CN" or not line:
        return line

    stripped = line.strip()
    if not stripped:
        return line

    stat = _STAT_PATTERN.match(stripped)
    if stat:
        return f"{_STAT_LABELS[stat.group(1)]}{stat.group(2)}{stat.group(3)}"

    for compiled, template, pattern in _COMPILED_WORKER_LINE_PATTERNS:
        match = compiled.match(stripped)
        if match:
            groups = list(match.groups())
            if pattern.startswith(r"^Confirming") and groups:
                groups[0] = "缓存的" if groups[0] == "cached" else "提供的"
            if pattern.startswith(r"^Finished game") and len(groups) >= 4:
                groups[3] = _RESULT_REASONS.get(groups[3], groups[3])
            if pattern.startswith(r"^Worker constraints") and groups:
                groups[0] = (
                    groups[0]
                    .replace("'concurrency':", "'并发数':")
                    .replace("'max_memory':", "'最大内存':")
                    .replace("'min_threads':", "'最少线程':")
                )
            return template.format(*groups)

    translated = stripped
    for english, chinese in _WORKER_PHRASES:
        translated = translated.replace(english, chinese)
    return translated
