#-*- coding: UTF-8 -*-
from hashlib import md5
import requests
from ast import literal_eval
from time import time
from configparser import ConfigParser
import base64

from requests.sessions import session


fileName='./img/2.jpg'

class AiPlat(object):
    '''
    获得单次请求类
    初始化方式:
    A=AiPlat(text)
    '''

    def __init__(self):
        '''
        初始化：获取配置文件参数
        '''
        config = ConfigParser()
        config.read_file(open('voice.ini', encoding='utf-8'))
        self.__app_id = int(config.get("voice", "APPID"))
        self.__app_key = config.get("voice", "APPKEY")

    def __getSignString(self, parser):
        '''
        计算sign值
        parser:请求参数  dict[]
        '''
        uri_str = ""
        for key in sorted(parser.keys()):
            if key == 'app_key':
                continue
            uri_str = uri_str + \
                "%s=%s&" % (key, requests.utils.quote(str(parser[key]).upper(),safe=''))
        sign_str = uri_str + 'app_key=' + self.__app_key
        sign_str=sign_str.replace('%20','+')
        print(sign_str)
        hash_md5 = md5(sign_str.encode("utf-8"))
        return hash_md5.hexdigest().upper()

    def __invoke(self, url, params):
        '''
        进行API链接
        url:API地址
        params:请求参数
        目前问题：req.json()返回的是带单引号的json格式，用json.loads()无法读取
        目前解决方法：将rsp转化为str，使用ast.literal_eval()方法转换
        '''
        req = requests.post(url, data=params)
        try:
            rsp = req.json()
            dict_rsp = literal_eval(str(rsp))
            return dict_rsp
        except:

            dict_error = {}
            dict_error['ret'] = -1
            dict_error['httpcode'] = -1
            dict_error['msg'] = "system error"
            return dict_error

    def __getNlpWord(self, session):
        '''
        方法：获取语音合成内容
        text:合成内容
        '''
        url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_imagetranslate"
        postdata = {}
        postdata['app_id'] = self.__app_id
        postdata['time_stamp'] = int(time())
        postdata['nonce_str'] = str(int(time()))
        with open(fileName,'rb') as fp:
            image=base64.encodebytes(fp.read())
        postdata['image']=image
        postdata['session_id'] = session
        postdata['scene']='word'
        postdata['source']='zh'
        postdata['target']='en'
        sign = self.__getSignString(postdata)
        postdata['sign'] = sign
        return self.__invoke(url, postdata)

    def getWord(self, session):
        '''
        接口：语音合成并保存
        text：需要合成的文字
        '''
        req = self.__getNlpWord(session)
        print(req)


if __name__ == "__main__":

    bot = AiPlat()
    session = str(int(time()))
    bot.getWord(session)
