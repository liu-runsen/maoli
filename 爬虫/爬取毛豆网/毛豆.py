# -*- coding：utf-8 -*-
# time ：2019/7/29 18:21
# author: 毛利
import threading
from threading import Thread
from queue import Queue
import requests
from lxml import etree
from fake_useragent import UserAgent

def page_url(base_url):
    headers = {
        'User-Agent': ua.random,
    }
    page = '1'
    url_list = []
    while True:
        url = base_url % page
        print(url)
        # 解码
        html = requests.get(url, headers=headers).content.decode('utf-8')
        #
        page = str(int(page) + 1)
        tree = etree.HTML(html)
        a_list = tree.xpath('//div[@class="list-wrap clearfix"]/a/@href')
        for a in a_list:
            url_list.append(a)
        if len(a_list) == 0:
            break
    return url_list


class Crawl_MD(Thread):
    def __init__(self, url_queue):
        # 类的写法
        super(Crawl_MD, self).__init__()
        self.url_queue = url_queue
    def run(self):
        while True:
            if self.url_queue.empty():
                break
            try:
                url = self.url_queue.get(block=False)
                self.get_request(url)
            except Exception as e:
                print(e)
    def get_request(self, url):
        headers = {
            'User-Agent': ua.random,
        }
        response = requests.get(url, headers=headers).content.decode('utf-8')
        get_queue.put(response)

class Customer_MD(Thread):
    def run(self):
        while True:
            if get_queue.empty() and flag:
                break
            try:
                response = get_queue.get(block=False)
                self.get_data(response)
            except Exception as e:
                print(e)
    def get_none(self, word):
        if len(word) > 0:
            return word[0]
        else:
            return ''
    def get_data(self, response):
        tree = etree.HTML(response)
        title = tree.xpath('//h2[@class="banner-tit"]/text()')
        img = tree.xpath('//div[@class="slider"]//li[1]/img/@src')
        soufu = tree.xpath('//div[@class="sy-yf"]//p[@class="sy-num"]/text()')
        yuegong = tree.xpath('//div[@class="sy-yf"]/div[2]/p[@class="yf-num sy-num"]/text()')
        firm_money = tree.xpath('//p[@class="price "]/text()')
        peizhi = tree.xpath('//ul[@class="config-detail"]//p/text()')
        PZ = {}
        for i, j in zip(peizhi[::2], peizhi[1::2]):
            PZ[i] = j
        # print(title, img, soufu, yuegong, firm_money, peizhi)
        data = {
            'title': self.get_none(title),
            'img': self.get_none(img),
            '首付': ''.join(soufu).replace('   ', '|'),
            '月供': ''.join(yuegong).replace('  ', '|'),
            'firm_money': self.get_none(firm_money),
            '配置': PZ
        }
        print(data)
        global num
        word = [{"num": num}, {'data': data}]
        if lock.acquire():
            with open('data.txt', 'a') as f:
                f.write(str(word) + '\n')
                num += 1
                lock.release()

# num = 1
# flag = False
# get_queue = Queue()
if __name__ == '__main__':
    # 创建队列用于储存翻页url
    get_queue = Queue()
    ua = UserAgent()
    # 用来做标识
    flag = False
    # 每辆车详细页的url
    list = page_url('https://www.maodou.com/car/list/all/pg%s')
    # 创建队列用于爬取数据
    url_queue = Queue()
    # 翻页的url列表
    crawl_list = []
    # 每辆车的url
    customer_list = []
    # 锁起来
    lock = threading.Lock()
    # 详细页的url的队列
    [url_queue.put(i) for i in list]
    # 开三个线程来爬翻页的url
    for cre in range(3):
        crawl = Crawl_MD(url_queue)
        crawl.start()
        crawl_list.append(crawl)
    # 开三个线程来爬数据
    for cus in range(3):
        customer = Customer_MD()
        customer.start()
        customer_list.append(customer)
    # 释放锁
    [i.join() for i in crawl_list]
    # 如果分页的队列可能为空
    flag = True
    # 释放锁
    [a.join() for a in customer_list]



