from pushWork.DingTalk import push_url
import requests
import json


def push(message):
    at_all = message.get('at_all', False)
    at_user_ids=message.get('at_user_ids',None)
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
            url=push_url.url(),
            data=json.dumps(body),
            headers=headers
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                print("消息发送成功！")
            else:
                print(f"消息发送失败，错误码：{result['errcode']}, 说明：{result['errmsg']}")
        else:
            print(f"请求失败，状态码：{response.status_code}, 响应内容：{response.text}")

    except Exception as e:
        print(f"发送消息时发生错误：{e}")
