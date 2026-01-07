@echo off
chcp 65001 >nul
echo ====================================
echo   TrendRadar Web UI 启动脚本
echo ====================================
echo.

echo [1/3] 检查依赖...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Flask 未安装，正在安装依赖...
    pip install -r webui\requirements.txt
) else (
    echo ✓ 依赖已安装
)

echo.
echo [2/3] 启动 Web UI 服务...
cd webui
start cmd /k "python app.py"

echo.
echo [3/3] 完成!
echo.
echo ✅ Web UI 服务已启动
echo 🌐 访问地址: http://localhost:5000
echo 📝 停止服务: 关闭弹出的命令行窗口
echo.
pause
