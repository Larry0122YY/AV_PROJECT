@echo off
echo 正在启动视频播放器项目...
echo.

REM 检查 Node.js 是否安装
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未找到 Node.js，请先安装 Node.js
    pause
    exit /b 1
)

REM 检查 Python 是否安装
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 警告: 未找到 Python，后台服务将无法启动
    echo 只启动前端服务...
    echo.
    start "前端服务" cmd /k "cd /d %~dp0 && npm run dev"
    pause
    exit /b 0
)

REM 检查是否已安装依赖
if not exist "node_modules" (
    echo 正在安装前端依赖...
    call npm install
    echo.
)

if not exist "backend\videos" (
    mkdir backend\videos
)

REM 启动后台服务（新窗口）
echo 启动后台服务 (端口 8000)...
start "后台服务" cmd /k "cd /d %~dp0backend && python main.py"

REM 等待一下让后台先启动
timeout /t 2 /nobreak >nul

REM 启动前端服务（新窗口）
echo 启动前端服务 (端口 5173)...
start "前端服务" cmd /k "cd /d %~dp0 && npm run dev"

echo.
echo ========================================
echo 服务已启动！
echo 前端: http://localhost:5173
echo 后台: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo ========================================
echo.
echo 按任意键关闭此窗口（服务将继续运行）...
pause >nul
