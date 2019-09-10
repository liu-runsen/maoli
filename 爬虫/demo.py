# PROJECT： Reptile-master
# File: demo.py
# author： MaoLi (刘润森）
# DATE：  2019/9/9 22:44 


import requests
import hashlib
import time
import random

class fanyi(object):
    def __init__(self):
        self.headers= {
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-116786429@223.73.205.91; OUTFOX_SEARCH_USER_ID_NCOO=997889835.4626652; UM_distinctid=16be994bb1e142-0b7813bc2c777f-6353160-1fa400-16be994bb1f383; _ntes_nnid=1fe47fb7a39517ce84391a74d23c0644,1563159293320; _ga=GA1.2.1925019515.1563522506; JSESSIONID=aaa2M2sJpdWFq8kh_Ew0w; ___rl__test__cookies=1568042786896',
            'Referer':'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        self.data = {
            'i': None,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': None,
            'sign': None,
            'ts': None,
            'bv': None,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
        }
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    def fanyi(self,word):
        salt  = str(int(time.time()*10000)+random.random()*10)
        ts =  salt[:-1]
        sign_notmd5 = 'fanyideskweb' + word + salt + 'n%A-rKaT5fb[Gy?;N5@Tj'
        sign = hashlib.md5(sign_notmd5.encode('utf-8')).hexdigest()
        bv = hashlib.md5('5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'.encode('utf-8')).hexdigest()
        self.data['i'] = word
        self.data['salt'] = salt
        self.data['sign'] = sign
        self.data['ts'] = ts
        self.data['bv'] = bv
        res = requests.post(self.url, headers=self.headers, data=self.data)
        return res.json()['translateResult'][0][0]['tgt']
if __name__ == '__main__':
    youdao = fanyi()
    while True:
        content = input("请输入您需要翻译的内容:")
        if content == "q":
            break
        res = youdao.fanyi(content)
        print(res)