# -*- coding：utf-8 -*-
# time ：2019/3/29 17:09
# author: 毛利

import re
import base64
import requests
import time
import json
import rsa
from binascii import b2a_hex

class WeiBo(object):
    def __init__(self,username,password):
        self.password = password
        self.username = username
        self.session = requests.session()
    def encrypt_username(self):
        '''
        对账号进行base64加密
        :return:
        '''
        return base64.b64encode(self.username.encode())

    def encrypt_password(self):
        '''
        对密码进行rsa加密
        :return:
        '''
        result = self.per_login()
        my_password = str(result['servertime']) + '\t' + str(result['nonce']) + '\n' + str(self.password)
        publicky = rsa.PublicKey(int(result['pubkey'],16),int('10001',16))
        return b2a_hex(rsa.encrypt(my_password.encode(),publicky))

    def per_login(self):
        '''
        预请求拿到加密的参数
        :return:
        '''
        params = {
            'entry': 'weibo',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': self.encrypt_username(),
            'rsakt': 'mod',
            'checkpin': '1',
            'client': 'ssologin.js(v1.4.19)',
            '_': int(time.time()*1000)
        }
        url = 'https://login.sina.com.cn/sso/prelogin.php'
        response = self.session.get(url,params=params,verify = False)
        # print(response.text)
        json_data = re.findall(r'preloginCallBack\((.*?)\)',response.text,re.S)
        # print(json_data)
        if json_data:
            print('预请求已拿到加密的参数')
            return json.loads(json_data[0])
        else:
            print('预请求失败')
    def login(self):
        '''
        提交post的数据
        :return:
        '''
        result = self.per_login()
        print(result)
        data = {
            'entry': 'weibo',
            'gateway': '1',
            'from':'',
            'savestate':'7',
            'qrcode_flag': 'false',
            'useticket': '1',
            'pagerefer':'https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fpassport.weibo.com%2Fwbsso%2Flogout%3Fr%3Dhttps%253A%252F%252Fweibo.com%26returntype%3D1',
            'vsnf': '1',
            'su': self.encrypt_username(),
            'service': 'miniblog',
            'servertime':result.get('servertime'),
            'nonce': result.get('nonce'),
            'pwencode': 'rsa2',
            'rsakv': result.get('rsakv'),
            'sp': self.encrypt_password(),
            'sr': '1920 * 1080',
            'encoding': 'UTF - 8',
            'prelt':' 63',
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        post_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        login_data = self.session.post(post_url,data=data)
        login_data.encoding = 'gbk'
        if login_data.status_code == 200:
            next_url = re.findall(r'location.replace\("(.*?)"\)',login_data.text,re.S)
            if next_url:
                response = self.session.get(next_url[0]).content.decode('gbk')
                print(response)
                print('正在登陆')
                self.session.get(re.findall(r"location.replace\('(.*?)'\)",response,re.S)[0])
            print(self.session.get('https://www.weibo.com').text)
            print('你的账号{}已成功登录'.format(self.username))


if __name__ == '__main__':
    username = input('你的账号是：')
    password = input('账号的密码是：')
    weibo = WeiBo(username,password)
    weibo.login()