import hashlib
import time
import xml.etree.ElementTree as ET
from wxcloudrun.dev.messages import receive
from wxcloudrun.dev.messages import reply


def verify_wechat_request(data):
    """验证消息来自微信服务器"""
    result = {"status": False}
    if len(data) == 0:
        result["message"] = "请求参数不能为空"
        return result
    try:
        signature = data.get("signature")
        timestamp = data.get("timestamp")
        nonce = data.get("nonce")
        echostr = data.get("echostr")
        token = "LkzwgjSUrno7Tz7Tql"  # 请按照公众平台官网\基本配置中信息填写

        list_ = [token, timestamp, nonce].sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list_)
        hashcode = sha1.hexdigest()
        print("message_event_push/GET func: hashcode - {}, signature - {}".format(hashcode, signature))
        if hashcode == signature:
            result["status"] = True
            result["data"] = echostr
            return result
        else:
            return {"status": False, "error": "signature error", 
                    "message": "cal results are not equal: hashcode - {}, signature - {}".format(hashcode, signature)}
    except Exception as Argument:
        return {"status": False, "error": str(Argument)}


class MsgHandle(object):
    def __init__(self, xml_data):
        self.xml_data = xml_data

    def handle(self):
        """处理接收到的消息并生成回复"""
        if len(self.xml_data) == 0:
            return "error: xml data is empty"
        xml_data = ET.fromstring(self.xml_data)
        if xml_data.find('MsgType') is None:
            return "error: xml data is invalid"
        msg_type = xml_data.find('MsgType').text

        if msg_type == 'text':
            msg = receive.TextMsg(xml_data)
            if msg.content.decode("utf-8") in ['你好', '哈喽', 'hi', 'hello']:
                reply_text = f"你好！很高兴和你聊天。"
            else:
                reply_text = f"我暂时还看不懂你发的消息哦~"
            reply_msg = reply.TextMsg(
                to_user_name=msg.from_user_name,
                from_user_name=msg.to_user_name,
                content=reply_text
            )
            return reply_msg.send()

        elif msg_type == 'image':
            msg = receive.ImageMsg(xml_data)
            reply_text = f"你发送的是一张图片"
            reply_msg = reply.TextMsg(
                to_user_name=msg.from_user_name,
                from_user_name=msg.to_user_name,
                content=reply_text
            )
            return reply_msg.send()

        else:
            reply_text = f"暂不支持回复该类型消息~"
            msg = receive.Msg(xml_data)
            reply_msg = reply.TextMsg(
                to_user_name=msg.from_user_name,
                from_user_name=msg.to_user_name,
                content=reply_text
            )
            return reply_msg.send()

