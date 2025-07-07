from flask import Flask
from webhookClient import webhook_cclient_bp  # 导入我们刚才写的蓝图

# 创建 Flask 应用
app = Flask(__name__)

# 把蓝图注册到应用中，并加上一个统一的前缀 /webhook
app.register_blueprint(webhook_cclient_bp, url_prefix='/test')

# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)