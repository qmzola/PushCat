import configparser
import time
import hmac
import hashlib
import base64
import urllib.parse
import os

# 获取当前脚本所在目录
current_dir = os.path.dirname(__file__)
# 构建配置文件路径
config_path = os.path.join(current_dir, "..", "..", "configs", "config.ini")
config_path = os.path.normpath(config_path)
# 判断配置文件是否存在
if not os.path.exists(config_path):
    print("配置文件config.ini不存在")
    print("配置文件路径:", config_path)
# 读取配置文件的内容
config = configparser.ConfigParser()
config.read(config_path)
access_token = config.get("DingTalk", "ding_access_token").strip('"')
secret = config.get("DingTalk", "ding_secret").strip('"')
# 确保对应值不为空
if not access_token and secret:
    print("配置文件中签名信息为空")


# 计算加签
def calculate_push_key():
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return f"timestamp={timestamp}&sign={sign}"


#拼接DIngTalk WebHook地址
def url():
    push_keys = calculate_push_key()
    return f"https://oapi.dingtalk.com/robot/send?access_token={access_token}&{push_keys}"
