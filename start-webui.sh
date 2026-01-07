#!/bin/bash

echo "===================================="
echo "  TrendRadar Web UI 启动脚本"
echo "===================================="
echo ""

echo "[1/3] 检查依赖..."
if ! pip show flask &> /dev/null; then
    echo "⚠️  Flask 未安装，正在安装依赖..."
    pip install -r webui/requirements.txt
else
    echo "✓ 依赖已安装"
fi

echo ""
echo "[2/3] 启动 Web UI 服务..."
cd webui
python app.py &
WEBUI_PID=$!

echo ""
echo "[3/3] 完成!"
echo ""
echo "✅ Web UI 服务已启动 (PID: $WEBUI_PID)"
echo "🌐 访问地址: http://localhost:5000"
echo "📝 停止服务: kill $WEBUI_PID"
echo ""
