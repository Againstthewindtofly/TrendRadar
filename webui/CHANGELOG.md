# WebUI 更新日志

## 2026-01-07 - 配置管理增强

### 新增功能

#### 1. Docker 环境支持 ✅
- 修复了 Docker 容器内配置文件路径问题
- 自动检测运行环境（本地/Docker）并使用正确的路径

#### 2. 环境变量支持 ✅
- **读取配置时**自动合并环境变量和文件配置
- **保存配置时**不会覆盖由环境变量控制的配置
- 新增 `/api/config/env-status` 端点，用于查询哪些配置来自环境变量
- 为来自环境变量的配置添加 `_from_env` 标记

#### 3. 新增配置 API 端点 ✅

##### 应用配置 (app)
- `GET/POST /api/config/app`
- 配置时区、版本更新提示等

##### 报告配置 (report)
- `GET/POST /api/config/report`
- 配置报告模式（daily/current/incremental）
- 配置显示模式（keyword/platform）
- 配置排名阈值、排序方式等

##### 推送时间窗口 (push_window)
- `GET/POST /api/config/push-window`
- 配置推送时间范围
- 配置是否窗口内只推送一次

##### 存储配置 (storage)
- `GET/POST /api/config/storage`
- 配置存储后端（local/remote/auto）
- 配置数据格式（sqlite/txt/html）
- 配置本地存储路径和保留天数
- 配置远程存储（S3兼容）
- 配置数据拉取

##### 高级配置 (advanced)
- `GET/POST /api/config/advanced`
- 配置爬虫设置（请求间隔、代理等）
- 配置 RSS 设置（超时、代理等）
- 配置排序权重
- 配置消息批次大小和发送间隔
- 配置多账号限制

### 配置覆盖优先级

```
环境变量 > 配置文件
```

**读取时：**
- 如果设置了环境变量，显示环境变量的值
- 否则显示配置文件中的值

**保存时：**
- 只保存到配置文件
- 不会覆盖环境变量控制的配置项

### 使用示例

#### 场景 1: 混合使用环境变量和配置文件

**环境变量：**
```bash
FEISHU_WEBHOOK_URL=https://env-webhook.com
```

**配置文件：**
```yaml
notification:
  channels:
    feishu:
      webhook_url: "https://file-webhook.com"  # 会被环境变量覆盖
    dingtalk:
      webhook_url: "https://dingtalk.com"      # 使用文件配置
```

**结果：**
- 飞书使用环境变量的 webhook（https://env-webhook.com）
- 钉钉使用文件配置的 webhook（https://dingtalk.com）
- WebUI 保存时不会修改飞书的文件配置

#### 场景 2: 查询配置来源

```bash
# 获取环境变量状态
curl http://localhost:5000/api/config/env-status

# 响应：
{
  "notification": {
    "channels": {
      "feishu": {
        "webhook_url": true  # 来自环境变量
      },
      "dingtalk": {
        "webhook_url": false # 来自文件
      }
    }
  }
}
```

### 完整 API 列表

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/config` | GET/POST | 完整配置 |
| `/api/config/app` | GET/POST | 应用配置 |
| `/api/config/platforms` | GET/POST | 平台列表 |
| `/api/config/rss` | GET/POST | RSS配置 |
| `/api/config/report` | GET/POST | 报告配置 |
| `/api/config/notification` | GET/POST | 通知渠道配置 |
| `/api/config/push-window` | GET/POST | 推送时间窗口 |
| `/api/config/storage` | GET/POST | 存储配置 |
| `/api/config/advanced` | GET/POST | 高级配置 |
| `/api/config/env-status` | GET | 环境变量状态 |
| `/api/keywords` | GET/POST | 关键词配置 |
| `/api/test-notification` | POST | 测试通知 |
| `/api/reload` | POST | 热重载配置 |
| `/api/restart` | POST | 重启容器 |

详细 API 文档请查看 [API.md](./API.md)

### 技术细节

#### 配置加载逻辑

```python
def load_config():
    # 1. 加载 YAML 文件
    config = load_yaml_config()

    # 2. 合并环境变量（优先级更高）
    # 为来自环境变量的配置添加 _from_env 标记

    # 3. 返回合并后的配置
    return config
```

#### 配置保存逻辑

```python
def save_config(config):
    # 1. 深拷贝配置
    config_to_save = copy(config)

    # 2. 移除所有 _from_env 标记
    # 3. 移除所有被环境变量控制的字段

    # 4. 保存到 YAML 文件
    # （只保存文件配置，不包含环境变量）
```

### 文件结构

```
webui/
├── app.py              # 主应用文件（已更新）
├── API.md              # API 文档（新增）
├── CHANGELOG.md        # 更新日志（本文件）
├── README.md           # 使用说明
├── requirements.txt    # Python 依赖
└── templates/          # HTML 模板
    └── index.html
```

### 下一步

1. **前端开发**: 基于这些 API 开发前端界面
2. **功能增强**:
   - 实现通知测试功能
   - 实现配置热重载
   - 添加配置验证
3. **用户体验**:
   - 在 UI 中标识哪些字段来自环境变量（只读）
   - 添加配置项说明和提示
   - 添加配置导入/导出功能

### 注意事项

⚠️ **重要提醒**:
1. 环境变量控制的配置在 WebUI 中应显示为只读
2. 保存配置时会自动过滤环境变量配置，无需担心覆盖
3. 如需修改环境变量控制的配置，请直接修改环境变量或 .env 文件
4. Docker 容器需要重启才能应用环境变量的更改
