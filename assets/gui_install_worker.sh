#!/bin/bash
# 用于图形界面的非交互式 Fishtest Worker 安装脚本

# 图形界面传入的参数
if [ "$1" = "--encoded" ]; then
    decode_arg() {
        printf '%s' "$1" | base64 --decode
    }

    usr_name="$(decode_arg "$2")"
    usr_pwd="$(decode_arg "$3")"
    n_cores="$(decode_arg "$4")"
    ui_language="$(decode_arg "$5")"
    if [ -z "$usr_name" ] || [ -z "$ui_language" ]; then
        if [ "$ui_language" = "en_US" ]; then
            echo "Error: Failed to decode installation arguments."
        else
            echo "错误：无法解码图形界面传入的安装参数。"
        fi
        exit 2
    fi
else
    usr_name="$1"
    usr_pwd="$2"
    n_cores="$3"
    ui_language="${4:-zh_CN}"
fi

if [ "$ui_language" = "en_US" ]; then
    msg_start="--- Starting non-interactive worker installation ---"
    msg_username="Username: $usr_name"
    msg_invalid_cores="Invalid number of cores specified. Defaulting to 1 core."
    msg_cores="Cores: $n_cores"
    msg_update="--- Updating system and installing required packages ---"
    msg_clean="--- Cleaning package cache to save disk space ---"
    msg_remove="--- Removing old worker directory if it exists ---"
    msg_download="--- Downloading and extracting fishtest worker ---"
    msg_venv="--- Setting up Python virtual environment ---"
    msg_config="--- Generating fishtest.cfg ---"
    msg_config_ok="Successfully created fishtest.cfg"
    msg_config_error="Error: Failed to create fishtest.cfg"
    msg_finalize="--- Finalizing installation ---"
    msg_complete="--- Installation complete! ---"
else
    msg_start="--- 开始非交互式安装 Worker ---"
    msg_username="用户名：$usr_name"
    msg_invalid_cores="指定的核心数无效，将默认使用 1 个核心。"
    msg_cores="核心数：$n_cores"
    msg_update="--- 正在更新系统并安装必要的软件包 ---"
    msg_clean="--- 正在清理软件包缓存以节省磁盘空间 ---"
    msg_remove="--- 正在删除旧的 Worker 文件夹（如存在） ---"
    msg_download="--- 正在下载并解压 Fishtest Worker ---"
    msg_venv="--- 正在创建 Python 虚拟环境 ---"
    msg_config="--- 正在生成 fishtest.cfg ---"
    msg_config_ok="已成功创建 fishtest.cfg"
    msg_config_error="错误：创建 fishtest.cfg 失败"
    msg_finalize="--- 正在完成安装 ---"
    msg_complete="--- 安装完成！ ---"
fi

echo "$msg_start"
echo "$msg_username"

# n_cores 应为正整数。
# 重新安装时可能包含类似“2 ; = 2 cores”的字符串，
# 因此这里只提取其中的第一个整数。
n_cores=$(echo "$n_cores" | grep -oE '[0-9]+' | head -n 1)
# 如果 n_cores 为空或不是数字，则默认使用 1。
if ! [[ "$n_cores" =~ ^[0-9]+$ ]]; then
    echo "$msg_invalid_cores"
    n_cores=1
fi
if [ "$ui_language" = "en_US" ]; then
    msg_cores="Cores: $n_cores"
else
    msg_cores="核心数：$n_cores"
fi
echo "$msg_cores"

# 1. 更新系统并安装必要的软件包
echo "$msg_update"
pacman -Syuu --noconfirm
pacman -S --noconfirm --needed unzip make mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-python

echo "$msg_clean"
pacman -Scc --noconfirm

# 2. 删除旧的 Worker 文件夹，确保全新安装
echo "$msg_remove"
rm -rf worker

# 3. 下载并解压 Fishtest Worker
echo "$msg_download"
tmp_dir=___${RANDOM}
mkdir ${tmp_dir} && pushd ${tmp_dir} > /dev/null
wget https://github.com/official-stockfish/fishtest/archive/master.zip
unzip -q master.zip "fishtest-master/worker/**" # -q 表示安静模式
pushd fishtest-master/worker > /dev/null

# 4. 创建虚拟环境并安装依赖
echo "$msg_venv"
python3 -m venv "env"
env/bin/python3 -m pip install -q --upgrade pip setuptools wheel
env/bin/python3 -m pip install -q requests

# 5. 使用 Worker 自身的逻辑写入 fishtest.cfg
echo "$msg_config"
env/bin/python3 worker.py "$usr_name" "$usr_pwd" --concurrency "$n_cores" --only_config --no_validation
if [ $? -eq 0 ]; then
    echo "$msg_config_ok"
else
    echo "$msg_config_error"
    exit 1
fi

# 6. 创建 fishtest.cmd 启动脚本
cat << EOF > fishtest.cmd
@echo off
set "HERE=%~dp0"
set "PATH=C:\msys64\ucrt64\bin;C:\msys64\usr\bin;%PATH%"
cd /d "%HERE%"
env\\bin\\python3.exe worker.py
EOF

echo "$msg_finalize"
popd > /dev/null && popd > /dev/null
mv $tmp_dir/fishtest-master/worker .
rm -rf $tmp_dir

echo "$msg_complete"
