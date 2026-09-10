# Fishtest Worker 图形管理器

这是一个面向 Windows 的图形界面工具，用于安装、配置和运行
[Fishtest](https://tests.stockfishchess.org/tests) Worker。

它会自动安装 MSYS2、下载 Fishtest Worker 文件、管理 Worker 配置，并在界面中实时显示日志和任务进度。
程序首次运行默认使用简体中文，也可以在“设置”窗口中切换为 English。

![app](https://github.com/user-attachments/assets/bc10707b-2349-430b-99a4-cd88761dd851)

## 系统要求

- Windows 10 或 Windows 11。
- 可用的互联网连接。
- 安装和更新 MSYS2 需要管理员权限。

## 使用方法

### 1. 下载

从 [Releases 页面](https://github.com/dav1312/fishtest-worker-gui/releases)下载
`fishtest-worker-gui.exe`。

请将程序放在一个新的空文件夹中，用于管理 Worker。例如：
`C:\Users\%username%\Downloads\FishtestWorker`。

### 2. 安装 Worker

1. 运行 `fishtest-worker-gui.exe`。
2. 点击“安装/重新安装 Worker”。
3. Windows 将显示用户账户控制（UAC）提示，请点击“是”。
4. 程序会自动将 MSYS2 安装到 `C:\msys64`，并在程序目录下的 `worker` 子文件夹中设置 Fishtest Worker 文件。
5. 等待安装完成。窗口底部的日志区域会显示实时进度，整个过程可能需要几分钟。

重新安装会删除并重新创建当前目录中的 `worker` 文件夹，因此其中已有的配置也会被替换。

### 3. 配置账号

1. 点击“设置”。
2. 填写 Fishtest 用户名、密码以及要使用的核心数（并发数）。
3. 如果需要访问 GitHub API，可选填 GitHub Personal Access Token。
4. 在“界面语言”中选择“简体中文”或“English”。
5. 点击“保存”。账号信息将保存至 `worker/fishtest.cfg`，语言设置保存在同一文件的 `[general]` 区域。

没有 Fishtest 账号？可以在设置窗口中点击注册链接，打开
<https://tests.stockfishchess.org/signup>。

### 4. 运行 Worker

- **启动**：点击“启动 Worker”。Worker 运行期间，其他控制按钮会被禁用，以避免操作冲突；日志区域会显示 Worker 输出。
- **正常停止**：点击“停止 Worker”。程序会创建 `fish.exit` 文件，让 Worker 完成当前任务后干净退出。这是推荐的停止方式。
- **强制停止**：如果 Worker 没有响应，可以右键点击红色的“停止 Worker”按钮，然后确认强制停止。此操作会立即终止 Worker 进程，正在进行的工作可能会丢失。

任务运行期间，界面会显示已完成的游戏数、总游戏数以及预计剩余时间。

### 5. 更新与卸载

- **更新 MSYS2**：点击“更新 MSYS2 环境”，运行底层环境的标准更新命令。此操作需要管理员权限。
- **卸载**：卸载分为两个阶段，先删除 Worker 文件，再卸载 MSYS2；两个阶段都需要管理员权限。
  1. **删除 Worker 文件夹**：按钮首先会变为“删除 Worker 文件夹”。确认后会删除本地 Worker 脚本和配置。
  2. **卸载 MSYS2**：删除 `worker` 文件夹后，同一个按钮会变为“卸载 MSYS2”。点击后会运行 MSYS2 卸载程序，并从系统中完整移除 `C:\msys64`。

## 从源代码构建

如果要从源代码构建程序，请按以下步骤操作：

1. 克隆本仓库。
2. 创建并激活 Python 虚拟环境。
3. 安装依赖：

   ```sh
   pip install -r requirements.txt
   ```

4. 使用 PyInstaller 构建可执行文件：

   ```sh
   pyinstaller --name "fishtest-worker-gui" --onefile --noconsole --add-data "assets;assets" main.py
   ```

   GitHub Actions 工作流会额外打包 CustomTkinter 文件，并使用 `assets/icon.ico` 设置程序图标。

5. 最终的 `.exe` 文件位于 `dist` 文件夹中。

## 本地化说明

- 界面文本由根目录的 `i18n.py` 统一管理。
- 默认语言为简体中文；用户选择的语言会写入 `worker/fishtest.cfg` 的 `[general] language`。
- 命令参数、文件名、配置节名和配置键保持原样。Worker 原始英文输出仍用于进度解析；简体中文界面会在显示前翻译常见日志。
- 如果要增加语言，只需在 `i18n.py` 的 `LANGUAGE_NAMES`、`LOG_LEVEL_NAMES` 和 `TRANSLATIONS` 中增加对应语言条目。

## 许可证

本项目采用 GNU General Public License v3.0。详情请参阅 [LICENSE](LICENSE)。
