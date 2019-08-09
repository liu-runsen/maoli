# -*- coding：utf-8 -*-
# time ：2019/8/4 23:25
# author: 毛利

from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--proxy--server=http://127.0.0.1:8080')
driver = webdriver.Chrome(chrome_options=options)