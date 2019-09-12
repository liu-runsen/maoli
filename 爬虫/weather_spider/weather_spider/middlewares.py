# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import time
import scrapy




from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class WeatherSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s


    def process_request(self, request, spider):

        if request.meta.get('selenium'):
            # 为了让浏览器能够无界面的工作
            chrome_options = Options()
            # 设置chrome浏览器无界面模式
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=chrome_options)
            # 用浏览器去访问这个地址
            driver.get(request.url)
            time.sleep(1.5)  # 因为浏览器需要加载渲染
            html = driver.page_source
            driver.quit()
            return scrapy.http.HtmlResponse(url=request.url, body=html, encoding='utf-8', request=request)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)




import random
class RandomUserAgentMiddleware(object):
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        # 从settings.py中导入MY_USER_AGENT
        s = cls(user_agents=crawler.settings.get('MY_USER_AGENT'))
        return s

    def process_request(self, request, spider):
        agent = random.choice(self.user_agents)
        request.headers['User-Agent'] = agent
        return None




import random
class ddleware(object):
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        # 从settings.py中导入MY_USER_AGENT
        s = cls(user_agents=crawler.settings.get('MY_USER_AGENT'))

        return s

    def process_request(self, request, spider):
        agent = random.choice(self.user_agents)
        request.headers['User-Agent'] = agent
        return None