import re
from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree
from handle_mongo import douban_mongo


class HandleDoubanMovieTop250(object):
    def __init__(self):
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        self.page_url = []

    def handle_page_url(self):
        #通过分析页面URL可以得知
        #通过range构造页码变量,从0开始,到249结束,步长为25
        for i in range(0,250,25):
            url = "https://movie.douban.com/top250?start=%s&filter="%i
            self.page_url.append(url)

    #处理请求方法
    def handle_request(self,url):
        response = requests.get(url=url)
        return response.text
    #处理页码页
    def handle_page_detail(self,url):
        # print(url)
        #处理特殊字符
        sub_search = re.compile(r"[\s\r\t]")
        response = self.handle_request(url=url)
        html = etree.HTML(response)
        #解析当前页面有多少个电影信息
        item_list = html.xpath("//ol[@class='grid_view']//li")
        print(item_list)
        for item in item_list:
            info = {}
            #电影名称,将特殊字符替换为空
            info['movie_name'] = sub_search.sub('',''.join(item.xpath(".//div[@class='hd']/a//span/text()")))
            info['actors_information'] = sub_search.sub('',''.join(item.xpath(".//div[@class='bd']/p/text()")))
            info['score'] = sub_search.sub('',''.join(item.xpath(".//div[@class='bd']/div[@class='star']/span[2]/text()")))
            info['evaluate'] = sub_search.sub('',''.join(item.xpath(".//div[@class='bd']/div[@class='star']/span[4]/text()")))
            info['describe'] = sub_search.sub('',''.join(item.xpath(".//p[@class='quote']/span/text()")))
            info['from_url'] = url
            #数据入库
            # print(info)
            douban_mongo.handle_save_data(info)

    #启动方法
    def run(self):
        self.handle_page_url()
        #创建线程池
        t = ThreadPoolExecutor()
        for i in self.page_url:
            t.submit(self.handle_page_detail,i)
        t.shutdown()
        print(self.page_url)
#入口函数
def main():
    douban = HandleDoubanMovieTop250()
    douban.run()

if __name__ == '__main__':
    #入口函数调用
    main()
