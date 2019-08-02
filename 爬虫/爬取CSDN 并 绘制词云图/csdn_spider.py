# -*- coding：utf-8 -*-
# time ：2019/7/20 17:57
# author: 毛利
from matplotlib import pyplot as plt
from  cv2 import imread
import requests
import jieba
from bs4 import BeautifulSoup
import re
from wordcloud import WordCloud
titles = set()
def html(url):
    if url:
        r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'})
        if r.status_code == 200:
            # print('访问成功')
            return r.text
    else:
        print('访问失败')
        return None

def get_text(html):
    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all('a', href=re.compile(r'/weixin_44510615/article/details'))
    for i in links:
        titles.add(i.get_text())


def get_img_1():
    # 不使用图片背景
    strs = ''
    # 如果为空就直接退出
    if titles.__len__() == 0:
        return
    for item in titles:
        strs = strs + item
    # 去掉空格和换行
    s = strs.replace('\n','').replace(' ','')
    # 进行分词
    word_cut = jieba.cut(s)
    # 把分词用空格连起来
    word_cut_join = " ".join(word_cut)
    print(word_cut_join)
    w = WordCloud(
        # 设置字体 (在C盘是固定的）
        font_path='C:/Windows/Fonts/simfang.ttf',
        # 设置输出的图片宽高像素值
        width=1000, height=700,
        # 设置输出的图片背景色
        background_color='white')
    # 生成词云
    w.generate(word_cut_join)
    # 保存图片
    w.to_file('demo1.jpg')
    # 展示图片
    plt.show()

def get_img_2():
    # 使用中国地图的图片作为背景
    strs = ''
    if titles.__len__() == 0:
        return
    for item in titles:
        strs = strs +item
    s =  strs.replace('\n','').replace(' ','')
    # 设置背景图片
    img_file = 'China.jpg'
    # 解析背景图片（从cv2中导入）
    mask_img = imread(img_file)
    # 进行分词
    word_cut = jieba.cut(s)
    # 把分词用空格连起来
    word_cut_join = " ".join(word_cut)
    # 设置词云参数
    wc = WordCloud(
        # 设置字体
        font_path='C:/Windows/Fonts/simfang.ttf',
        # 允许最大词汇量
        max_words=2000,
        # 设置最大号字体大小
        max_font_size=90,
        # 设置使用的背景图片，这个参数不为空时，width和height会被忽略
        mask=mask_img,
        # 设置输出的图片背景色
        background_color='white')
    # 生成词云
    wc.generate(word_cut_join)
    # 显示图片
    plt.imshow(wc)
    # 将图片保存到本地
    plt.savefig('demo.jpg')
    plt.show()


def main():
    for i in range(1,30):
        url = 'https://blog.csdn.net/weixin_44510615/article/list/{}'.format(str(i))
        res = html(url)
        get_text(res)
    get_img_1()
if __name__ == '__main__':
    main()