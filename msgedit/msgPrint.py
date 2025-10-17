from app_logging import get_logger

import pushWork.DingTalk.pushDingTalk

logger = get_logger("MsgEdit")


def msg_print(msg):
    platforms = msg['platform']
    for platform in platforms:
        if platform == "DingTalk":
            pushWork.DingTalk.pushDingTalk.push(msg)
            logger.info("收到一条钉钉推送")
