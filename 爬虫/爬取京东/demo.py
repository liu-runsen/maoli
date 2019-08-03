# -*- coding：utf-8 -*-
# time ：2019/8/3 22:32
# author: 毛利

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import csv
import random

# 声明一个谷歌驱动器，并设置不加载图片，间接加快访问速度
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
browser = webdriver.Chrome(options=options)
# url
url = 'https://www.jd.com/'
# 声明一个list，存储dict
data_list = []

def start_spider():
    # 请求url
    browser.get(url)
    # 获取输入框的id，并输入关键字python爬虫
    browser.find_element_by_id('key').send_keys('python爬虫')
    # 输入回车进行搜索
    browser.find_element_by_id('key').send_keys(Keys.ENTER)
    # 显示等待下一页的元素加载完成
    WebDriverWait(browser, 1000).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'pn-next')
        )
    )
    # 先获取一个有多少页
    all_page = eval(browser.find_element_by_css_selector('span.p-skip em b').text)
    all_pages = browser.find_element_by_css_selector('span.p-skip em b').text
    print(all_page)
    print(all_pages)
    # 设置一个计数器
    count = 0
    # 无限循环
    while True:
        try:
            count += 1
            # 显示等待商品信息加载完成
            WebDriverWait(browser, 1000).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, 'gl-item')
                )
            )
            # 将滚动条拉到最下面的位置，因为往下拉才能将这一页的商品信息全部加载出来
            browser.execute_script('document.documentElement.scrollTop=10000')
            # 随机延迟,等下元素全部刷新
            time.sleep(random.randint(1, 3))
            browser.execute_script('document.documentElement.scrollTop=0')
            # 开始提取信息,找到ul标签下的全部li标签
            lis = browser.find_elements_by_class_name('gl-item')
            # 遍历
            for li in lis:
                # 名字
                name = li.find_element_by_xpath('.//div[@class="p-name p-name-type-2"]//em').text
                # 价格
                price = li.find_element_by_xpath('.//div[@class="p-price"]//i').text
                # 评论数
                comment = li.find_elements_by_xpath('.//div[@class="p-commit"]//a')
                if comment:
                    comment = comment[0].text
                else:
                    comment = None
                # 商铺名字
                shop_name = li.find_elements_by_class_name('J_im_icon')
                if shop_name:
                    shop_name = shop_name[0].text
                else:
                    shop_name = None
                # 商家类型
                shop_type = li.find_elements_by_class_name('goods-icons')
                if shop_type:
                    shop_type = shop_type[0].text
                else:
                    shop_type = None
                # 声明一个字典存储数据
                data_dict = {}
                data_dict['name'] = name
                data_dict['price'] = price
                data_dict['comment'] = comment
                data_dict['shop_name'] = shop_name
                data_dict['shop_type'] = shop_type
                data_list.append(data_dict)
                print(data_dict)
        except Exception as e:
            print(e)
            continue
        # 如果count==all_page就退出循环
        if count == all_page:
            break
        # 找到下一页的元素pn-next

        fp_next = browser.find_element_by_xpath('//a[@class="fp-next"]')
        # 点击下一页
        fp_next.click()

def main():
    start_spider()
    # 将数据写入json
    with open('data_json.json', 'a+', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    print('json文件写入完成')
    with open('data_csv.csv', 'w', encoding='utf-8', newline='') as f:
        # 表头
        title = data_list[0].keys()
        # 声明writer
        writer = csv.DictWriter(f, title)
        # 写入表头
        writer.writeheader()
        # 批量写入数据
        writer.writerows(data_list)
    print('csv文件写入完成')

if __name__ == '__main__':
    main()
    # 退出浏览器
    browser.quit()
