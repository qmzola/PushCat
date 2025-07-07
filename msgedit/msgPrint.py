import json
import os
import sys

sys.path.append(os.path.abspath(".."))
from pushWork.DingTalk.pushDingTalk import push
project_root = os.path.abspath("..")  # 根据你当前路径调整
sys.path.append(project_root)


def msg_print(msg):
    if msg['token'] == "Kve2UuCqEWRaM66fMIU48uSB0ELfTKJAc5ZgO1H0f8W515eOLsvWearV9i9y2l48":
        push(msg)