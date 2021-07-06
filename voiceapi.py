#-*- coding: UTF-8 -*-
from hashlib import md5
import requests
from ast import literal_eval
from time import time
from configparser import ConfigParser
from playsound import playsound
import base64
import threading


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
        self.__voice_loc = config.get("file", "voiceloc")
        self.__voice_error = config.get("file","error")
        self.__voice_request = config.get("file","request")
        self.__app_id = int(config.get("voice", "APPID"))
        self.__app_key = config.get("voice", "APPKEY")
        self.__speaker = int(config.get("voice", "speaker"))
        self.__format = int(config.get("voice", "format"))
        self.__volume = int(config.get("voice", "volume"))
        self.__speed = int(config.get("voice", "speed"))
        self.__aht = int(config.get("voice", "aht"))
        self.__apc = int(config.get("voice", "apc"))
        self.__lastvoice=''

        if self.__format==1:
            self.__fileName=self.__voice_loc+'voice.pcm'
        elif self.__format==2:
            self.__fileName=self.__voice_loc+'voice.wav'
        elif self.__format==3:
            self.__fileName=self.__voice_loc+'voice.mp3'

    def __getSignString(self,parser):
        '''
        计算sign值
        parser:请求参数  dict[]
        app_key:appkey的值，单独传入
        '''
        uri_str = ""
        for key in sorted(parser.keys()):
            if key == 'app_key':
                continue
            uri_str = uri_str + \
                "%s=%s&" % (key, requests.utils.quote(str(parser[key])))
        sign_str = uri_str + 'app_key=' + self.__app_key
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
        header={}
        header['Content-Type'] = 'application/x-www-form-urlencoded'
        req = requests.post(url, headers=header, data=params)
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

    def __getNlpVoice(self, text):
        '''
        方法：获取语音合成内容
        text:合成内容
        '''
        url = "https://api.ai.qq.com/fcgi-bin/aai/aai_tts"
        postdata = {}
        postdata['app_id'] = self.__app_id
        postdata['time_stamp'] = int(time())
        postdata['nonce_str'] = str(int(time()))
        postdata['speaker'] = self.__speaker
        postdata['format'] = self.__format
        postdata['volume'] = self.__volume
        postdata['speed'] = self.__speed
        postdata['text'] = text
        postdata['aht'] = self.__aht
        postdata['apc'] = self.__apc
        sign = self.__getSignString(postdata)
        postdata['sign'] = sign
        return self.__invoke(url, postdata)

    def __ToFile(self, data):
        '''
        方法：保存文件
        '''
        ori_image_data=base64.b64decode(data)
        fout = open(self.__fileName, 'wb')
        fout.write(ori_image_data)
        fout.close()


    def getVoice(self,text):
        '''
        接口：语音合成并保存
        text：需要合成的文字
        '''
        req=self.__getNlpVoice(text)
        if req['ret']==0:
            #保存
            self.__ToFile(req['data']['speech'])
            self.__lastvoice=self.__fileName
        else:
            self.__lastvoice=self.__voice_error
            print(req)

    def playVoice(self):
        '''
        接口：播放已合成语音，请求失败则播放错误提示
        '''
        t=threading.Thread(target=playsound,args=(self.__lastvoice,))
        t.start()
