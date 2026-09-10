# Fishtest Worker 图形界面

这是一个用户友好的图形界面，用于在 Windows 上设置和运行 [Fishtest](https://tests.stockfishchess.org/tests) worker。

它能够自动安装 MSYS2 和 Fishtest worker 脚本，管理相关配置，并实时显示日志信息。

![应用界面](https://github.com/user-attachments/assets/bc10707b-2349-430b-99a4-cd88761dd851)

## 前置条件

- Windows 10 或 Windows 11。
- 可用的互联网连接。

## 使用方法

### 1. 下载

从 [Releases 页面](https://github.com/dav1312/fishtest-worker-gui/releases)下载 `fishtest-worker-gui.exe` 文件。

将可执行文件放入一个新的空文件夹中。这个文件夹将用于管理你的 worker，例如：

```text
C:\Users\%username%\Downloads\FishtestWorker
```

### 2. 安装

1. 运行 `fishtest-worker-gui.exe`。
2. 点击 **安装/重新安装 Worker** 按钮。
3. Windows 用户账户控制（UAC）提示框会出现，并请求管理员权限。点击 **是**。
4. 程序会自动下载并安装 MSYS2 到：

   ```text
   C:\msys64
   ```

   随后，程序会在一个新的 `worker` 子文件夹中设置 Fishtest worker 文件。
5. 等待整个过程完成。你可以在窗口底部的日志查看器中监控进度。该过程可能需要几分钟。

### 3. 配置

1. 点击 **设置** 按钮。
2. 在新窗口中输入你的 Fishtest **用户名**、**密码**，以及希望使用的 **核心数**（并发数）。
3. 点击 **保存**。你的信息将保存到：

   ```text
   worker/fishtest.cfg
   ```

### 4. 运行 Worker

- **启动：** 点击较大的 **启动 Worker** 按钮。其他所有控件都会被禁用，以防止发生冲突。此时，日志查看器会显示 Fishtest worker 的输出信息。

- **正常停止：** 点击 **停止 Worker** 按钮。程序会创建一个 `fish.exit` 文件，通知 worker 完成当前任务后再干净地关闭。这是推荐的停止方式。

- **强制停止：** 如果 worker 没有响应，请**右键点击**红色的 **停止 Worker** 按钮。程序会要求你确认。确认后，worker 进程会立即终止，正在进行的工作可能会丢失。

### 5. 维护与卸载

- **更新 MSYS2：** 点击 **更新 MSYS2 环境** 按钮，运行底层环境的标准更新命令。此操作需要管理员权限。

- **卸载：** 卸载过程分为两个阶段：首先删除 worker 文件，然后卸载 MSYS2。这两个步骤都需要管理员权限。

  1. **删除 Worker 文件夹：** 点击卸载按钮后，程序首先会询问是否删除本地的 `worker` 文件夹。删除后，你的 worker 脚本和配置文件也会一并移除。

  2. **卸载 MSYS2：** `worker` 文件夹删除后，同一个按钮的文字会变为 **卸载 MSYS2**。点击该按钮后，程序会运行 MSYS2 卸载程序，并将 MSYS2 从系统中完全删除：

     ```text
     C:\msys64
     ```

## 从源代码构建

如果你希望从源代码构建此应用程序，请按照以下步骤操作：

1. 克隆代码仓库。
2. 创建并激活 Python 虚拟环境。
3. 安装所需的软件包：

   ```sh
   pip install -r requirements.txt
   ```

4. 使用 PyInstaller 构建可执行文件：

   ```sh
   pyinstaller --name "fishtest-worker-gui" --onefile --noconsole --add-data "assets;assets" main.py
   ```

5. 最终生成的 `.exe` 文件将位于 `dist` 文件夹中。

## 许可证

本项目采用 GNU General Public License v3.0授权。详情请参阅 [LICENSE](LICENSE) 文件。
