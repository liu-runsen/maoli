# -*- coding：utf-8 -*-
# time ：2019/7/25 11:37
# author: 毛利

"""
    使用多线程安全queue下载爬取www.doutula.com最新表情包
"""
import requests
from lxml import etree
from queue import Queue
import threading
import os
# 用于保存图片的下载方式
from urllib import request



class Producer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/69.0.3497.100 Safari/537.36',
    }
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
        if  not os.path.exists(r'D:\images\imgs'):
            os.makedirs(r'D:\images\imgs')

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self, url):
        response = requests.get(url, headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        contents = html.xpath("//a[@class='col-xs-6 col-sm-3']")
        for content in contents:
            title = content.xpath(".//p[@style='display: none']/text()")[0]
            href = content.xpath(".//img/@data-original")[0]
            suffix = os.path.splitext(href)[1]
            filename = title + suffix
            self.img_queue.put((href, filename))

class Consumer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url, filename = self.img_queue.get()
            request.urlretrieve(img_url, 'D:\images\imgs\{}'.format(filename))
            print(filename + '----下载完成')


def main():
    page_queue = Queue(100)
    img_queue = Queue(1000)

    for p in range(1, 101):
        url = 'http://www.doutula.com/photo/list/?page={}'.format(p)
        page_queue.put(url)

    for x in range(5):
        producer = Producer(page_queue, img_queue)
        producer.start()

    for x in range(5):
        consumer = Consumer(page_queue, img_queue)
        consumer.start()


if __name__ == '__main__':
    main()
