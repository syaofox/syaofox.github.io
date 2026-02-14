#!/bin/bash

# ZRAM 一键配置脚本
# 适用于 Linux Mint / Ubuntu 或其他基于 Debian 的系统

# --- 变量定义 ---
ZRAM_PERCENT=50      # ZRAM 大小占总内存的百分比
ZRAM_PRIORITY=100    # ZRAM 交换优先级（高于默认的 -2 或 -1）
ZRAM_ALGO="zstd"     # 压缩算法 (lz4 或 zstd)
ZRAM_CONFIG_FILE="/etc/default/zramswap"

# --- 颜色定义 ---
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查是否以 root 权限运行
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}错误: 请使用 sudo 运行此脚本。例如: sudo ./enable_zram.sh${NC}"
  exit 1
fi

echo -e "${YELLOW}--- ZRAM 自动配置程序启动 ---${NC}"

# 1. 更新软件包列表
echo -e "${GREEN}1. 正在更新软件包列表...${NC}"
apt update

# 2. 安装 zram-tools
echo -e "${GREEN}2. 正在安装 zram-tools...${NC}"
apt install zram-tools -y

# 3. 配置 ZRAM 参数
echo -e "${GREEN}3. 正在配置 ZRAM 参数...${NC}"
if [ -f "$ZRAM_CONFIG_FILE" ]; then
    # 备份现有配置
    cp "$ZRAM_CONFIG_FILE" "${ZRAM_CONFIG_FILE}.bak"
    echo "已备份现有配置文件到 ${ZRAM_CONFIG_FILE}.bak"
    
    # 使用 sed 命令设置或更新配置
    # 注意: 这些 sed 命令旨在处理 zram-tools 的标准配置文件格式
    
    # 设置 PERCENT
    sed -i "/^#*PERCENT=/c\PERCENT=$ZRAM_PERCENT" "$ZRAM_CONFIG_FILE"
    
    # 设置 PRIORITY
    sed -i "/^#*PRIORITY=/c\PRIORITY=$ZRAM_PRIORITY" "$ZRAM_CONFIG_FILE"
    
    # 设置 ALGO
    sed -i "/^#*ALGO=/c\ALGO=$ZRAM_ALGO" "$ZRAM_CONFIG_FILE"
    
    echo "ZRAM 配置已更新:"
    grep -E 'PERCENT|PRIORITY|ALGO' "$ZRAM_CONFIG_FILE"
else
    echo -e "${RED}警告: 找不到 $ZRAM_CONFIG_FILE。 ZRAM 配置文件不存在。${NC}"
    echo "请检查 zram-tools 是否正确安装。"
fi

# 4. 停止并启动 zramswap 服务以应用更改（仅在不重启的情况下使用）
echo -e "${GREEN}4. 正在重启 zramswap 服务以立即应用更改...${NC}"
systemctl restart zramswap.service

# 5. 检查 ZRAM 状态
echo -e "${GREEN}5. 检查当前的 Swap 状态（ZRAM 应已启动）：${NC}"
swapon --show

echo -e "\n${YELLOW}--- 配置完成 ---${NC}"
echo -e "ZRAM 已配置为占用 ${ZRAM_PERCENT}% 内存，优先级为 ${ZRAM_PRIORITY} (高于您的 swapfile)。"
echo -e "${RED}重要提示：为确保所有系统设置和启动服务完全生效，建议您重新启动计算机。${NC}"