import json
import os
import threading
import time
from typing import Optional, Tuple

import httpx
from playsound import playsound

from src.config import config as base_config

config = base_config.get('voice')


class VoiceManager(object):
    '''声音管理器'''

    def __init__(self):
        self._app_id = config.get('app-id')
        self._app_key = config.get('app-key')
        self._secret_key = config.get('secret-key')
        self._request_dict = {
            "spd": config['spd'],
            "pit": config['pit'],
            "vol": config['vol'],
            "per": config['per'],
            "aue": config['aue'],
        }
        self._thread = threading

    def _get_token(self) -> Tuple[Optional[str], Optional[int]]:
        '''
        :说明
            获取token

        :返回
            str：token值，可能是None
            int：有效期
        '''
        path = base_config['data']
        token_file = f"{path['path']}/{path['file']}"
        if not os.path.exists(token_file):
            return None, None

        with open(token_file, 'r', encoding='utf-8') as f:
            file = json.load(f)

        token = file['token']
        access_time = file['accesstime']
        return token, access_time

    def _check_token(self) -> bool:
        '''
        验证token是否可用
        '''
        token, access_time = self._get_token()
        if token is None:
            return False

        now_time = time.time()
        return (now_time > access_time)

    async def _update_token(self) -> bool:
        '''更新token'''
        url = 'https://aip.baidubce.com/oauth/2.0/token'
        params = {
            "grant_type": "client_credentials",
            "client_id": self._app_key,
            "client_secret": self._secret_key
        }
        async with httpx.AsyncClient() as client:
            try:
                req_url = await client.get(url=url, params=params)
                req_json = req_url.json()
                sec = req_json['expires_in']
                access_time = time.time()+sec
                data = {
                    "token": req_json['access_token'],
                    "access_time": access_time
                }
                path = base_config['data']
                token_file = f"{path['path']}/{path['file']}"
                with open(token_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f)
                return True

            except Exception:
                return False

    async def _get_nlp_voice(self, text) -> dict:
        '''
        :说明
            输入文字请求语音

        :参数
            * text：请求文字

        :返回
            * dict：返回字典
        '''
        # 验证token
        if not self._check_token():
            await self._update_token()
        token, _ = self._get_token()
        postdata = self._request_dict
        postdata['tex'] = text
        postdata['tok'] = token
        postdata['cuid'] = self._app_id
        postdata['ctp'] = 1
        postdata['lan'] = 'zh'

        url = 'https://tsn.baidu.com/text2audio'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        async with httpx.AsyncClient(headers=headers) as client:
            try:
                req_url = await client.post(url=url, data=postdata)
                req_dict = {
                    "code": req_url.status_code,
                    "data": req_url.content,
                    "reason": req_url.reason_phrase
                }
            except Exception as e:
                req_dict = {
                    "code": -1,
                    "data": "",
                    "reason": str(e)
                }
        return req_dict

    async def out_voice(self, text):
        '''
        :说明
            输入文字播放声音
        '''
        req_dict = await self._get_nlp_voice(text)
        if req_dict['code'] == 200:
            playsound(req_dict['data'])
