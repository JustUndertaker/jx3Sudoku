# -*- coding: utf-8 -*-
import requests
from configparser import ConfigParser
import time
import datetime
import base64



class OCR():
    def __init__(self):
        self.__updateini()

    def __updateini(self):
        '''
        更新配置
        '''
        config = ConfigParser()
        with open('ocr.ini', encoding='utf-8') as f:
            config.read_file(f)
        self.__AppID = config.get('OCR', 'AppID')
        self.__APIKey = config.get('OCR', 'APIKey')
        self.__SecretKey = config.get('OCR', 'SecretKey')
        self.__AccessToken = config.get('OCR', 'AccessToken')
        self.__AccessTime = config.get('OCR', 'AccessTime')

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
            config.read('ocr.ini')
            config.set('OCR', 'AccessToken', self.__AccessToken)
            config.set('OCR', 'AccessTime', self.__AccessTime)
            config.write(open('ocr.ini', "r+"))

    def OCRapiByFileName(self, filename):
        #验证accessToken
        if not self.__accessTokenCheck():
            self.__accessTokenRefresh()
            self.__updateini()

        request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate'
        url = request_url + '?access_token=' + self.__AccessToken
        f = open(filename, 'rb')
        img = base64.b64encode(f.read())
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        postdata = {"image": img, "recognize_granularity": "small"}
        response = requests.post(url, data=postdata, headers=headers)
        if response:
            jsondata = response.json()
            print(jsondata)
            data=str(jsondata).replace("'",'"')
            with open('./img/data5.json','w',encoding='utf-8') as f:
                f.write(data)

if __name__ == '__main__':

    ocr=OCR()
    img='./img/data5.jpg'
    ocr.OCRapiByFileName(img)
