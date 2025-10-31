#!/bin/bash
# 安全 runfile 安装（自动停止/恢复 GUI）

RUNFILE="$1"
TARGET="$2"

[[ -z "$RUNFILE" || -z "$TARGET" ]] && {
    echo "用法: $0 cuda_13.0.1_530.30.02_linux.run /usr/local/cuda-13.0"
    exit 1
}

# 1. 停止 GUI
echo "停止图形界面..."
sudo systemctl isolate multi-user.target

# 2. 安装
echo "开始安装 $RUNFILE → $TARGET"
sudo sh "$RUNFILE" --toolkit --toolkitpath="$TARGET" --no-opengl-libs --override

# 3. 恢复 GUI
echo "恢复图形界面..."
sudo systemctl start graphical.target

echo "安装完成！请重启验证：nvidia-smi"
