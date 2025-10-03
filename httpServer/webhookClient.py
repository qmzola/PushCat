from flask import Blueprint,jsonify,request
import sys
import os

# 引入消息处理部分代码
sys.path.append(os.path.abspath(("../magedit")))
from msgedit import msgPrint

#创建一个蓝图对象
webhook_client_bp = Blueprint('webhook_cclient_bp',__name__)

#消息接受以及基本处理，并调用消息处理
@webhook_client_bp.route('/webhookinput',methods=['POST'])
def msg_input():
    date= request.json
    msgPrint.msg_print(date)
    return 'Created',201