# TrendRadar Web UI

## 📖 功能介绍

提供可视化的配置管理界面,支持以下功能:

- ✅ **通知渠道配置**: 管理飞书、钉钉、企业微信、Telegram、Server酱等多个通知渠道
- ✅ **RSS 订阅管理**: 添加/编辑/禁用 RSS 订阅源
- ✅ **新闻平台配置**: 选择要监控的新闻平台
- ✅ **关键词管理**: 在线编辑监控关键词
- ✅ **基础设置**: 报告模式、显示模式等

## 🚀 快速启动

### 方式一: 本地启动

```bash
# 1. 安装依赖
cd webui
pip install -r requirements.txt

# 2. 启动服务
python app.py

# 3. 访问界面
浏览器打开: http://localhost:5000
```

### 方式二: Docker 启动

```bash
# 在项目根目录
docker compose up -d

# 访问 Web UI
浏览器打开: http://localhost:5000
```

## 🔧 配置说明

### 环境变量

- `WEBUI_PORT`: Web UI 端口 (默认: 5000)
- `WEBUI_AUTH`: 是否启用认证 (默认: false)
- `WEBUI_USERNAME`: 管理员用户名
- `WEBUI_PASSWORD`: 管理员密码

### 安全建议

⚠️ **生产环境部署注意事项**:

1. **启用身份认证**: 设置 `WEBUI_AUTH=true` 并配置用户名密码
2. **限制访问**: 使用防火墙限制只能从内网访问
3. **使用 HTTPS**: 配置 SSL 证书,避免配置信息在传输中泄露
4. **定期备份**: 定期备份配置文件

## 📋 开发路线图

- [x] 基础 CRUD API
- [x] 前端界面设计
- [ ] 通知渠道测试功能
- [ ] 配置热重载
- [ ] 身份认证
- [ ] 配置版本管理
- [ ] 配置导入导出
- [ ] 实时日志查看

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!
