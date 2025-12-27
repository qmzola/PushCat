import logging
from flask import Blueprint, request
import sys
import os
from ConfigRead.ConfigReader import load_config
from msgedit import msgPrint


config=load_config()
#创建一个蓝图对象
webhook_client_bp = Blueprint('webhook_cclient_bp',__name__)

#消息接受以及基本处理，并调用消息处理
@webhook_client_bp.route('/webhookinput/<url_token>',methods=['POST'])
def msg_input_check(url_token):
    try:
        if url_token != config.input_token.url_access_token:
            logging.debug(f"收到/webhookinput/{url_token}的无效请求，已忽略。原因是请求URL Token不正确。")
            return 'Not Found', 404
        data = request.json
        if data['token'] != config.input_token.input_access_token:
            logging.debug(f"收到/webhookinput/{url_token}的无效请求，已忽略。原因是请求内容Token不正确。")
            return 'Forbidden', 403
        else:
            msgPrint.msg_print(data)
            return 'Created',201
    except Exception as e:
        logging.error(f"处理webhook请求时出错: {str(e)}", exc_info=True)
        return 'Internal Server Error', 500