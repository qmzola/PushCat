import requests
import json

import time
import hmac
import hashlib
import base64
import urllib.parse
from ConfigRead.ConfigReader import load_config
from app_logging import get_logger

logger = get_logger("DingTalkPush")

config = load_config()

access_token = config.dingtalk.access_token
secret = config.dingtalk.secret


# 计算加签
def calculate_push_key():
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return f"timestamp={timestamp}&sign={sign}"


# 拼接DIngTalk WebHook地址
def url():
    push_keys = calculate_push_key()
    return f"https://oapi.dingtalk.com/robot/send?access_token={access_token}&{push_keys}"


def push(message):
    at_all = message.get('at_all', False)
    at_user_ids = message.get('at_user_ids', None)
    message_title = message['message']['content'][0]['title']
    message_body = message['message']['content'][0]['body']

    body = {
        "at": {
            "isAtAll": bool(at_all),  # 是否@所有人
            "atUserIds": at_user_ids or [],  # @用户ID列表
        },
        "text": {
            "content": f"{message_title}\n{message_body}"  # 消息内容
        },
        "msgtype": "text"  # 消息类型为文本
    }
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            url=url(),
            data=json.dumps(body),
            headers=headers
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                logger.info("消息发送成功！")
            else:
                logger.error(f"消息发送失败，错误码：{result['errcode']}, 说明：{result['errmsg']}")
        else:
            logger.error(f"请求失败，状态码：{response.status_code}, 响应内容：{response.text}")

    except Exception as e:
        logger.error(f"发送消息时发生错误：{e}")
