@echo off
chcp 65001 >nul
:: 如果缺少 winget，则安装它
:: https://learn.microsoft.com/en-us/windows/package-manager/winget/
where winget >nul 2>nul || (
    echo 正在以静默模式安装 winget，这需要一些时间……
    powershell -Command "$progressPreference = 'silentlyContinue'; Write-Information '正在下载 WinGet 及其依赖项……'; Invoke-WebRequest -Uri https://aka.ms/getwinget -OutFile Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle; Invoke-WebRequest -Uri https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx -OutFile Microsoft.VCLibs.x64.14.00.Desktop.appx; Invoke-WebRequest -Uri https://github.com/microsoft/microsoft-ui-xaml/releases/download/v2.8.6/Microsoft.UI.Xaml.2.8.x64.appx -OutFile Microsoft.UI.Xaml.2.8.x64.appx; Add-AppxPackage Microsoft.VCLibs.x64.14.00.Desktop.appx; Add-AppxPackage Microsoft.UI.Xaml.2.8.x64.appx; Add-AppxPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle; Remove-Item Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle; Remove-Item Microsoft.VCLibs.x64.14.00.Desktop.appx; Remove-Item Microsoft.UI.Xaml.2.8.x64.appx"
)

:: 检查是否已经安装 MSYS2
if exist "C:\msys64\msys2_shell.cmd" (
    echo MSYS2 已经安装，跳过安装步骤。
) else (
    :: 安装 MSYS2
    winget install --id=MSYS2.MSYS2 --silent --accept-package-agreements --accept-source-agreements

    :: 更新 MSYS2
    C:\msys64\msys2_shell.cmd -defterm -msys2 -here -c "pacman -Syuu --noconfirm"
)
