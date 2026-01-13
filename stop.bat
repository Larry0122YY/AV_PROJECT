@echo off
echo 正在停止所有服务...
echo.

REM 停止 Node.js 进程（前端）
taskkill /F /IM node.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [√] 前端服务已停止
) else (
    echo [!] 未找到运行中的前端服务
)

REM 停止 Python 进程（后台）
taskkill /F /IM python.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [√] 后台服务已停止
) else (
    echo [!] 未找到运行中的后台服务
)

echo.
echo 所有服务已停止
pause
