import xml.etree.ElementTree as ET

def parse_xml(xml_data):
    """解析xml消息"""
    if len(xml_data) == 0:
        return None
    xml_data = ET.fromstring(xml_data)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xml_data)
    elif msg_type == 'image':
        return ImageMsg(xml_data)
    elif msg_type == 'voice':
        return VoiceMsg(xml_data)
    elif msg_type == 'video':
        return VideoMsg(xml_data)
    elif msg_type == 'shortvideo':
        return ShortVideoMsg(xml_data)
    elif msg_type == 'location':
        return LocationMsg(xml_data)
    elif msg_type == 'link':
        return LinkMsg(xml_data)
    else:
        return None


class Msg(object):
    """消息基类"""
    def __init__(self, xml_data):
        self.to_user_name = xml_data.find('ToUserName').text
        self.from_user_name = xml_data.find('FromUserName').text
        self.create_time = xml_data.find('CreateTime').text
        self.msg_type = xml_data.find('MsgType').text
        self.msg_id = xml_data.find('MsgId').text


class TextMsg(Msg):
    """文本消息类"""
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.content = xml_data.find('Content').text.encode("utf-8")


class ImageMsg(Msg):
    """图片消息类"""
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.pic_url = xml_data.find('PicUrl').text
        self.media_id = xml_data.find('MediaId').text


class VoiceMsg(Msg):
    """语音消息类"""
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.media_id = xml_data.find('MediaId').text
        self.format = xml_data.find('Format').text

class VideoMsg(Msg):
    """视频消息类"""
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.media_id = xml_data.find('MediaId').text
        self.thumb_media_id = xml_data.find('ThumbMediaId').text


class ShortVideoMsg(Msg):
    """短视频消息类"""
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.media_id = xml_data.find('MediaId').text
        self.thumb_media_id = xml_data.find('ThumbMediaId').text


class LocationMsg(Msg):
    """位置消息类"""
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.location_x = xml_data.find('Location_X').text
        self.location_y = xml_data.find('Location_Y').text
        self.scale = xml_data.find('Scale').text
        self.label = xml_data.find('Label').text


class LinkMsg(Msg):
    """链接消息类"""
    def __init__(self, xml_data):
        super().__init__(xml_data)
        self.title = xml_data.find('Title').text
        self.description = xml_data.find('Description').text
        self.url = xml_data.find('Url').text
