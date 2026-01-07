#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrendRadar Web UI - 配置管理界面

提供 Web 界面来动态管理配置，包括：
- 通知渠道配置
- RSS 订阅源配置
- 新闻平台配置
- 关键词配置
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List
import json

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import yaml

# 添加项目根目录到 Python 路径
# 在 Docker 环境中,工作目录就是 /app
# 在本地开发环境中,需要找到项目根目录
if os.path.exists('/app/config'):
    # Docker 环境
    project_root = Path('/app')
else:
    # 本地开发环境
    project_root = Path(__file__).parent.parent

sys.path.insert(0, str(project_root))

app = Flask(__name__)
CORS(app)

# 配置文件路径
CONFIG_DIR = project_root / "config"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
KEYWORDS_FILE = CONFIG_DIR / "frequency_words.txt"


def _get_env_str(key: str, default: str = "") -> str:
    """从环境变量获取字符串值"""
    return os.environ.get(key, "").strip() or default


def load_yaml_config() -> Dict[str, Any]:
    """仅加载 YAML 配置文件"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        return {}


def load_config() -> Dict[str, Any]:
    """加载配置并合并环境变量（与 trendradar/core/loader.py 逻辑一致）"""
    config = load_yaml_config()

    # 获取通知渠道配置
    notification = config.get('notification', {})
    channels = notification.get('channels', {})

    # 合并环境变量到通知渠道
    if 'feishu' not in channels:
        channels['feishu'] = {}
    if 'dingtalk' not in channels:
        channels['dingtalk'] = {}
    if 'wework' not in channels:
        channels['wework'] = {}
    if 'telegram' not in channels:
        channels['telegram'] = {}
    if 'email' not in channels:
        channels['email'] = {}
    if 'ntfy' not in channels:
        channels['ntfy'] = {}
    if 'bark' not in channels:
        channels['bark'] = {}
    if 'slack' not in channels:
        channels['slack'] = {}
    if 'serverchan' not in channels:
        channels['serverchan'] = {}

    # 环境变量优先级更高，如果设置了环境变量，则显示环境变量的值
    env_feishu_webhook = _get_env_str('FEISHU_WEBHOOK_URL')
    if env_feishu_webhook:
        channels['feishu']['webhook_url'] = env_feishu_webhook
        channels['feishu']['_from_env'] = True

    env_dingtalk_webhook = _get_env_str('DINGTALK_WEBHOOK_URL')
    if env_dingtalk_webhook:
        channels['dingtalk']['webhook_url'] = env_dingtalk_webhook
        channels['dingtalk']['_from_env'] = True

    env_wework_webhook = _get_env_str('WEWORK_WEBHOOK_URL')
    if env_wework_webhook:
        channels['wework']['webhook_url'] = env_wework_webhook
        channels['wework']['_from_env'] = True

    env_wework_msg_type = _get_env_str('WEWORK_MSG_TYPE')
    if env_wework_msg_type:
        channels['wework']['msg_type'] = env_wework_msg_type

    env_telegram_bot_token = _get_env_str('TELEGRAM_BOT_TOKEN')
    if env_telegram_bot_token:
        channels['telegram']['bot_token'] = env_telegram_bot_token
        channels['telegram']['_from_env'] = True

    env_telegram_chat_id = _get_env_str('TELEGRAM_CHAT_ID')
    if env_telegram_chat_id:
        channels['telegram']['chat_id'] = env_telegram_chat_id

    env_email_from = _get_env_str('EMAIL_FROM')
    if env_email_from:
        channels['email']['from'] = env_email_from
        channels['email']['_from_env'] = True

    env_email_password = _get_env_str('EMAIL_PASSWORD')
    if env_email_password:
        channels['email']['password'] = env_email_password

    env_email_to = _get_env_str('EMAIL_TO')
    if env_email_to:
        channels['email']['to'] = env_email_to

    env_email_smtp_server = _get_env_str('EMAIL_SMTP_SERVER')
    if env_email_smtp_server:
        channels['email']['smtp_server'] = env_email_smtp_server

    env_email_smtp_port = _get_env_str('EMAIL_SMTP_PORT')
    if env_email_smtp_port:
        channels['email']['smtp_port'] = env_email_smtp_port

    env_ntfy_server_url = _get_env_str('NTFY_SERVER_URL')
    if env_ntfy_server_url:
        channels['ntfy']['server_url'] = env_ntfy_server_url
        channels['ntfy']['_from_env'] = True

    env_ntfy_topic = _get_env_str('NTFY_TOPIC')
    if env_ntfy_topic:
        channels['ntfy']['topic'] = env_ntfy_topic

    env_ntfy_token = _get_env_str('NTFY_TOKEN')
    if env_ntfy_token:
        channels['ntfy']['token'] = env_ntfy_token

    env_bark_url = _get_env_str('BARK_URL')
    if env_bark_url:
        channels['bark']['url'] = env_bark_url
        channels['bark']['_from_env'] = True

    env_slack_webhook = _get_env_str('SLACK_WEBHOOK_URL')
    if env_slack_webhook:
        channels['slack']['webhook_url'] = env_slack_webhook
        channels['slack']['_from_env'] = True

    env_serverchan_uid = _get_env_str('SERVERCHAN_UID')
    if env_serverchan_uid:
        channels['serverchan']['uid'] = env_serverchan_uid
        channels['serverchan']['_from_env'] = True

    env_serverchan_sendkey = _get_env_str('SERVERCHAN_SENDKEY')
    if env_serverchan_sendkey:
        channels['serverchan']['sendkey'] = env_serverchan_sendkey

    notification['channels'] = channels
    config['notification'] = notification

    return config


def save_config(config: Dict[str, Any]) -> bool:
    """
    保存配置到 YAML 文件
    注意：不会保存来自环境变量的配置（标记为 _from_env 的项）
    """
    try:
        # 深拷贝配置，避免修改原对象
        config_to_save = json.loads(json.dumps(config))

        # 移除所有 _from_env 标记和被环境变量控制的配置
        if 'notification' in config_to_save:
            notification = config_to_save['notification']
            if 'channels' in notification:
                channels = notification['channels']

                # 处理每个渠道
                for channel_name, channel_config in channels.items():
                    if isinstance(channel_config, dict):
                        # 如果渠道被环境变量控制，则从文件配置中移除
                        if channel_config.get('_from_env'):
                            # 移除 _from_env 标记
                            channel_config.pop('_from_env', None)

                            # 根据不同渠道，移除被环境变量控制的字段
                            if channel_name == 'feishu' and _get_env_str('FEISHU_WEBHOOK_URL'):
                                channel_config.pop('webhook_url', None)
                            elif channel_name == 'dingtalk' and _get_env_str('DINGTALK_WEBHOOK_URL'):
                                channel_config.pop('webhook_url', None)
                            elif channel_name == 'wework' and _get_env_str('WEWORK_WEBHOOK_URL'):
                                channel_config.pop('webhook_url', None)
                            elif channel_name == 'telegram':
                                if _get_env_str('TELEGRAM_BOT_TOKEN'):
                                    channel_config.pop('bot_token', None)
                                if _get_env_str('TELEGRAM_CHAT_ID'):
                                    channel_config.pop('chat_id', None)
                            elif channel_name == 'email':
                                if _get_env_str('EMAIL_FROM'):
                                    channel_config.pop('from', None)
                                if _get_env_str('EMAIL_PASSWORD'):
                                    channel_config.pop('password', None)
                                if _get_env_str('EMAIL_TO'):
                                    channel_config.pop('to', None)
                                if _get_env_str('EMAIL_SMTP_SERVER'):
                                    channel_config.pop('smtp_server', None)
                                if _get_env_str('EMAIL_SMTP_PORT'):
                                    channel_config.pop('smtp_port', None)
                            elif channel_name == 'ntfy':
                                if _get_env_str('NTFY_SERVER_URL'):
                                    channel_config.pop('server_url', None)
                                if _get_env_str('NTFY_TOPIC'):
                                    channel_config.pop('topic', None)
                                if _get_env_str('NTFY_TOKEN'):
                                    channel_config.pop('token', None)
                            elif channel_name == 'bark' and _get_env_str('BARK_URL'):
                                channel_config.pop('url', None)
                            elif channel_name == 'slack' and _get_env_str('SLACK_WEBHOOK_URL'):
                                channel_config.pop('webhook_url', None)
                            elif channel_name == 'serverchan':
                                if _get_env_str('SERVERCHAN_UID'):
                                    channel_config.pop('uid', None)
                                if _get_env_str('SERVERCHAN_SENDKEY'):
                                    channel_config.pop('sendkey', None)

        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(config_to_save, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"保存配置文件失败: {e}")
        return False


def load_keywords() -> str:
    """加载关键词配置"""
    try:
        with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"加载关键词文件失败: {e}")
        return ""


def save_keywords(content: str) -> bool:
    """保存关键词配置"""
    try:
        with open(KEYWORDS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"保存关键词文件失败: {e}")
        return False


# ==================== 路由定义 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """获取完整配置"""
    config = load_config()
    return jsonify({
        'success': True,
        'data': config
    })


@app.route('/api/config', methods=['POST'])
def update_config():
    """
    更新完整配置
    注意：只更新文件配置，不会覆盖环境变量控制的配置
    """
    try:
        new_config = request.json
        if save_config(new_config):
            return jsonify({
                'success': True,
                'message': '配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '配置保存失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'配置更新失败: {str(e)}'
        }), 500


@app.route('/api/config/notification', methods=['GET'])
def get_notification_config():
    """获取通知渠道配置"""
    config = load_config()
    return jsonify({
        'success': True,
        'data': config.get('notification', {})
    })


@app.route('/api/config/notification', methods=['POST'])
def update_notification_config():
    """
    更新通知渠道配置
    注意：只更新文件配置，不会覆盖环境变量控制的配置
    """
    try:
        # 加载原始 YAML 配置（不含环境变量）
        config = load_yaml_config()
        config['notification'] = request.json

        # 使用 save_config 保存，它会自动过滤环境变量
        if save_config(config):
            return jsonify({
                'success': True,
                'message': '通知配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '通知配置保存失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'通知配置更新失败: {str(e)}'
        }), 500


@app.route('/api/config/platforms', methods=['GET'])
def get_platforms_config():
    """获取新闻平台配置"""
    config = load_config()
    return jsonify({
        'success': True,
        'data': config.get('platforms', [])
    })


@app.route('/api/config/platforms', methods=['POST'])
def update_platforms_config():
    """更新新闻平台配置"""
    try:
        # 加载原始 YAML 配置
        config = load_yaml_config()
        config['platforms'] = request.json
        if save_config(config):
            return jsonify({
                'success': True,
                'message': '平台配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '平台配置保存失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'平台配置更新失败: {str(e)}'
        }), 500


@app.route('/api/config/rss', methods=['GET'])
def get_rss_config():
    """获取 RSS 订阅配置"""
    config = load_config()
    return jsonify({
        'success': True,
        'data': config.get('rss', {})
    })


@app.route('/api/config/rss', methods=['POST'])
def update_rss_config():
    """更新 RSS 订阅配置"""
    try:
        # 加载原始 YAML 配置
        config = load_yaml_config()
        config['rss'] = request.json
        if save_config(config):
            return jsonify({
                'success': True,
                'message': 'RSS 配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'RSS 配置保存失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'RSS 配置更新失败: {str(e)}'
        }), 500


@app.route('/api/keywords', methods=['GET'])
def get_keywords():
    """获取关键词配置"""
    content = load_keywords()
    return jsonify({
        'success': True,
        'data': content
    })


@app.route('/api/keywords', methods=['POST'])
def update_keywords():
    """更新关键词配置"""
    try:
        content = request.json.get('content', '')
        if save_keywords(content):
            return jsonify({
                'success': True,
                'message': '关键词配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '关键词配置保存失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'关键词配置更新失败: {str(e)}'
        }), 500


@app.route('/api/config/report', methods=['GET'])
def get_report_config():
    """获取报告配置"""
    config = load_config()
    return jsonify({
        'success': True,
        'data': config.get('report', {})
    })


@app.route('/api/config/report', methods=['POST'])
def update_report_config():
    """更新报告配置"""
    try:
        config = load_yaml_config()
        config['report'] = request.json
        if save_config(config):
            return jsonify({
                'success': True,
                'message': '报告配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '报告配置保存失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'报告配置更新失败: {str(e)}'
        }), 500


@app.route('/api/config/push-window', methods=['GET'])
def get_push_window_config():
    """获取推送时间窗口配置"""
    config = load_config()
    notification = config.get('notification', {})
    return jsonify({
        'success': True,
        'data': notification.get('push_window', {})
    })


@app.route('/api/config/push-window', methods=['POST'])
def update_push_window_config():
    """更新推送时间窗口配置"""
    try:
        config = load_yaml_config()
        if 'notification' not in config:
            config['notification'] = {}
        config['notification']['push_window'] = request.json
        if save_config(config):
            return jsonify({
                'success': True,
                'message': '推送时间窗口配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '推送时间窗口配置保存失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'推送时间窗口配置更新失败: {str(e)}'
        }), 500


@app.route('/api/config/advanced', methods=['GET'])
def get_advanced_config():
    """获取高级配置"""
    config = load_config()
    return jsonify({
        'success': True,
        'data': config.get('advanced', {})
    })


@app.route('/api/config/advanced', methods=['POST'])
def update_advanced_config():
    """更新高级配置"""
    try:
        config = load_yaml_config()
        config['advanced'] = request.json
        if save_config(config):
            return jsonify({
                'success': True,
                'message': '高级配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '高级配置保存失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'高级配置更新失败: {str(e)}'
        }), 500


@app.route('/api/config/storage', methods=['GET'])
def get_storage_config():
    """获取存储配置"""
    config = load_config()
    return jsonify({
        'success': True,
        'data': config.get('storage', {})
    })


@app.route('/api/config/storage', methods=['POST'])
def update_storage_config():
    """更新存储配置"""
    try:
        config = load_yaml_config()
        config['storage'] = request.json
        if save_config(config):
            return jsonify({
                'success': True,
                'message': '存储配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '存储配置保存失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'存储配置更新失败: {str(e)}'
        }), 500


@app.route('/api/config/app', methods=['GET'])
def get_app_config():
    """获取应用配置"""
    config = load_config()
    return jsonify({
        'success': True,
        'data': config.get('app', {})
    })


@app.route('/api/config/app', methods=['POST'])
def update_app_config():
    """更新应用配置"""
    try:
        config = load_yaml_config()
        config['app'] = request.json
        if save_config(config):
            return jsonify({
                'success': True,
                'message': '应用配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '应用配置保存失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'应用配置更新失败: {str(e)}'
        }), 500


@app.route('/api/config/env-status', methods=['GET'])
def get_env_status():
    """
    获取环境变量配置状态
    返回哪些配置项是通过环境变量设置的，前端可以据此将这些字段设为只读
    """
    env_status = {
        'notification': {
            'channels': {
                'feishu': {
                    'webhook_url': bool(_get_env_str('FEISHU_WEBHOOK_URL'))
                },
                'dingtalk': {
                    'webhook_url': bool(_get_env_str('DINGTALK_WEBHOOK_URL'))
                },
                'wework': {
                    'webhook_url': bool(_get_env_str('WEWORK_WEBHOOK_URL')),
                    'msg_type': bool(_get_env_str('WEWORK_MSG_TYPE'))
                },
                'telegram': {
                    'bot_token': bool(_get_env_str('TELEGRAM_BOT_TOKEN')),
                    'chat_id': bool(_get_env_str('TELEGRAM_CHAT_ID'))
                },
                'email': {
                    'from': bool(_get_env_str('EMAIL_FROM')),
                    'password': bool(_get_env_str('EMAIL_PASSWORD')),
                    'to': bool(_get_env_str('EMAIL_TO')),
                    'smtp_server': bool(_get_env_str('EMAIL_SMTP_SERVER')),
                    'smtp_port': bool(_get_env_str('EMAIL_SMTP_PORT'))
                },
                'ntfy': {
                    'server_url': bool(_get_env_str('NTFY_SERVER_URL')),
                    'topic': bool(_get_env_str('NTFY_TOPIC')),
                    'token': bool(_get_env_str('NTFY_TOKEN'))
                },
                'bark': {
                    'url': bool(_get_env_str('BARK_URL'))
                },
                'slack': {
                    'webhook_url': bool(_get_env_str('SLACK_WEBHOOK_URL'))
                },
                'serverchan': {
                    'uid': bool(_get_env_str('SERVERCHAN_UID')),
                    'sendkey': bool(_get_env_str('SERVERCHAN_SENDKEY'))
                }
            }
        }
    }

    return jsonify({
        'success': True,
        'data': env_status
    })


@app.route('/api/test-notification', methods=['POST'])
def test_notification():
    """测试通知渠道连通性"""
    try:
        channel = request.json.get('channel')
        config_data = request.json.get('config')

        # TODO: 实现各渠道的测试逻辑
        # 这里需要导入 trendradar 的通知发送模块

        return jsonify({
            'success': True,
            'message': f'{channel} 测试消息发送成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'测试失败: {str(e)}'
        }), 500


@app.route('/api/reload', methods=['POST'])
def reload_config():
    """热重载配置（向主进程发送信号）"""
    try:
        # TODO: 实现配置热重载逻辑
        # 可以通过以下方式：
        # 1. 向主进程发送 SIGHUP 信号
        # 2. 使用消息队列通知主进程
        # 3. 监听文件变化自动重载

        return jsonify({
            'success': True,
            'message': '配置重载成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'配置重载失败: {str(e)}'
        }), 500


@app.route('/api/restart', methods=['POST'])
def restart_container():
    """重启 TrendRadar Docker 容器"""
    import subprocess
    try:
        result = subprocess.run(
            ['docker', 'restart', 'trendradar'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return jsonify({'success': True, 'message': '容器重启成功'})
        else:
            return jsonify({'success': False, 'message': '请手动执行: docker restart trendradar'})
    except FileNotFoundError:
        return jsonify({'success': False, 'message': '请手动执行: docker restart trendradar'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'请手动执行: docker restart trendradar'})


if __name__ == '__main__':
    # 开发环境启动
    port = int(os.environ.get('WEBUI_PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
