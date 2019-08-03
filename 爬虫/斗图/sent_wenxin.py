# -*- coding：utf-8 -*-
# time ：2019/8/2 23:30
# author: 毛利


import glob
import time

import itchat
from itchat.content import TEXT, PICTURE


imgs = []

def searchImage(text):
    print('收到关键词: ', text)
    for name in glob.glob('D:\images\imgs\*'+text+'*'):
        imgs.append(name)
    print(imgs)

@itchat.msg_register([PICTURE, TEXT])
def text_reply(msg):
    # print(msg['Content'])
    print(msg)
    searchImage(msg['Content'])
    for img in imgs[:2]:
        # print(msg)
        itchat.send_image(img,toUserName=msg['ToUserName'])
        time.sleep(1)

        print('开始向{}发送表情:'.format(msg['ToUserName']),img)
    imgs.clear()


itchat.auto_login(hotReload=True)
itchat.run()