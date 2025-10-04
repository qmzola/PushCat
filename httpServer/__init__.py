from flask import Flask
from httpServer.webhookClient import webhook_client_bp
from app_logging import get_logger

logger = get_logger("httpServer")

# 创建 Flask 应用
app = Flask(__name__)

# 把蓝图注册到应用中，并加上一个统一的前缀 /webhook
app.register_blueprint(webhook_client_bp, url_prefix='/test')


# 启动服务器
def start_http_server():
    app.run(debug=True)
