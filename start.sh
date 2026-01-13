#!/bin/bash

echo "正在启动视频播放器项目..."
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "错误: 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "警告: 未找到 Python，后台服务将无法启动"
    echo "只启动前端服务..."
    echo ""
    npm run dev &
    exit 0
fi

# 检查并安装依赖
if [ ! -d "node_modules" ]; then
    echo "正在安装前端依赖..."
    npm install
    echo ""
fi

# 创建视频目录
mkdir -p backend/videos

# 启动后台服务
echo "启动后台服务 (端口 8000)..."
cd backend
if command -v python3 &> /dev/null; then
    python3 main.py &
else
    python main.py &
fi
cd ..

# 等待一下
sleep 2

# 启动前端服务
echo "启动前端服务 (端口 5173)..."
npm run dev &

echo ""
echo "========================================"
echo "服务已启动！"
echo "前端: http://localhost:5173"
echo "后台: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo "========================================"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
wait
