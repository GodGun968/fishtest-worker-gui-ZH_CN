@echo off
chcp 65001 >nul
:: 更新 MSYS2
C:\msys64\msys2_shell.cmd -defterm -msys2 -here -c "pacman -Syuu --noconfirm"
