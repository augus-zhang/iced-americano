import logging
from run import app
from flask import request
from wxcloudrun.dev.messages.handle import *
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

# 新增一个测试接口
@app.route('/api/hello', methods=['GET'])
def hello():
    """
    :return: 测试接口返回hello world
    """
    return make_succ_response('hello world')

# 接收消息推送接口
@app.route('/api/message_event_push', methods=['GET', 'POST'])
def message_event_push():
    """处理消息推送事件"""
    if request.method == 'GET':
        verify_resp = verify_wechat_request(request.args)
        if verify_resp.get("status"):
            return verify_resp.get("data")
        else:
            app.logger.error('--------Verify wechat request failed: {}'.format(verify_resp))
            return ""
    
    app.logger.info('--------Received wechat message: {}'.format(request.data.decode('utf-8')))
    # 过滤探测请求(云托管上填写URL时会有此类请求)
    if request.data.decode('utf-8') == "CheckContainerPath":
        return "success"
    msg_handle = MsgHandle(request.data.decode('utf-8'))
    reply_xml = msg_handle.handle()
    if reply_xml is None:
        return ""
    return reply_xml    
