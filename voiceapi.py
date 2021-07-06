# -*- coding: utf-8 -*-
import requests
from configparser import ConfigParser
import time
import datetime
from playsound import playsound
import threading


class AiPlat():
    def __init__(self):
        self.__updateini()

    def __updateini(self):
        '''
        更新配置
        '''
        config = ConfigParser()
        with open('api.ini', encoding='utf-8') as f:
            config.read_file(f)
        self.__AppID = config.get('Baidu', 'AppID')
        self.__APIKey = config.get('Baidu', 'APIKey')
        self.__SecretKey = config.get('Baidu', 'SecretKey')
        self.__AccessToken = config.get('Baidu', 'AccessToken')
        self.__AccessTime = config.get('Baidu', 'AccessTime')
        with open('voice.ini', encoding='utf-8') as f:
            config.read_file(f)
        self.__voice_loc = config.get("file", "voiceloc")
        self.__voice_error = config.get("file","error")
        self.__voice_request = config.get("file","request")
        self.__spd=int(config.get('voice','spd'))
        self.__pit=int(config.get('voice','pit'))
        self.__vol=int(config.get('voice','vol'))
        self.__per=int(config.get('voice','per'))
        self.__aue=int(config.get('voice','aue'))
        self.__lastvoice=''

        if self.__aue==3:
            self.__fileName=self.__voice_loc+'voice.mp3'
        elif self.__aue==4:
            self.__fileName=self.__voice_loc+'voice.pcm'
        elif self.__aue==5:
            self.__fileName=self.__voice_loc+'voice.pcm'
        elif self.__aue==6:
            self.__fileName=self.__voice_loc+'voice.wav'



    def __accessTokenCheck(self) -> bool:
        '''
        验证AccessToken是否过期
        True:AccessToken可用
        False:AccessToken已过期
        '''
        if(self.__AccessTime==''):
            return False
        accesstime = time.mktime(
            time.strptime(self.__AccessTime, r"%Y-%m-%d %H:%M:%S"))
        nowtime = time.mktime(time.localtime())
        diff = nowtime - accesstime
        if diff >= 0:
            return False
        else:
            return True

    def __accessTokenRefresh(self):
        '''
        更新AccessToken
        '''
        url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.__APIKey + '&client_secret=' + self.__SecretKey
        response = requests.get(url)
        if response:
            json = response.json()
            sec = json['expires_in']
            day = sec / (60 * 60 * 24) - 1
            self.__AccessToken = json['access_token']
            self.__AccessTime = (
                datetime.datetime.now() +
                datetime.timedelta(days=day)).strftime(r"%Y-%m-%d %H:%M:%S")
            #写入配置
            config = ConfigParser()
            config.read('api.ini')
            config.set('Baidu', 'AccessToken', self.__AccessToken)
            config.set('Baidu', 'AccessTime', self.__AccessTime)
            config.write(open('api.ini', "r+"))

    def __getNlpVoice(self, tex):
        #验证accessToken
        if not self.__accessTokenCheck():
            self.__accessTokenRefresh()
            self.__updateini()

        url = 'https://tsn.baidu.com/text2audio'
        postdata={
            "tex":tex,
            "tok":self.__AccessToken,
            "cuid":self.__AppID,
            "ctp":1,
            "lan":"zh",
            "spd":self.__spd,
            "pit":self.__pit,
            "vol":self.__vol,
            "per":self.__per,
            "aue":self.__aue
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=postdata, headers=headers)
        try:
            dict_rsp={}
            dict_rsp['code']=response.status_code
            dict_rsp['data']=response.content
            dict_rsp['reason']=response.reason
 
            return dict_rsp
        except:

            dict_rsp = {}
            dict_rsp['code'] = -1
            dict_rsp['data'] = ""
            dict_rsp['reason'] = "system error"
            return dict_rsp
    
    def __ToFile(self, data):
        '''
        方法：保存文件
        '''
        fout = open(self.__fileName, 'wb')
        fout.write(data)
        fout.close()

    def getVoice(self,text):
        '''
        接口：语音合成并保存
        text：需要合成的文字
        '''
        req=self.__getNlpVoice(text)
        if req['code']==200:
            #保存
            self.__ToFile(req['data'])
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

if __name__ == '__main__':

    ai=AiPlat()
    ai.getVoice("攻击间隔为：1,2,3,4,5,6,7,8")
    ai.playVoice()
