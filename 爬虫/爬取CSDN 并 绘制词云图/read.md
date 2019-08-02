![效果图](https://img-blog.csdnimg.cn/20190720212927924.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDUxMDYxNQ==,size_16,color_FFFFFF,t_70)
> 最近，有点兴趣爬下自己在CSDN 的博客，并做出词云图来看下自己究竟写了什么

说起，就开干，下面是博客主页

> https://blog.csdn.net/weixin_44510615


### 环境
操作系统：Windows

Python版本：3.7.2

### 模块
本文涉及到的Python第三方模块，共计五个：分词模块jieba，文字云模块wordcloud，画图模块matplotlib，用来处理背景图片的模块cv2，访问的模块requests，解析的模块bs4
这些模块均可通过pip方式进行安装


### 实现思路
先获得每个文章的前言，用集合来存储，这样可以达到去重，在拼接成字符串。再通过jieba模块对字符串进行分词处理，然后对处理后的材料使用wordcloud文字云模块生成相应的词云图片即可。


![在这里插入图片描述](https://img-blog.csdnimg.cn/20190720212410254.png)


**先判断是否访问成功**
```
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
```




**通过BeautifulSoup来解析对应的字符串**
```
def get_text(html):
    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all('a', href=re.compile(r'/weixin_44510615/article/details'))
    for i in links:
    	# 通过集合达到去重的操作
        titles.add(i.get_text())
```

**制作云图的思路，直接看代码，代码中已添加详细注释说明。**
```
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
```
![效果图](https://img-blog.csdnimg.cn/20190720214233878.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDUxMDYxNQ==,size_16,color_FFFFFF,t_70)
### 使用图片来展示


```
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
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190720214734122.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDUxMDYxNQ==,size_16,color_FFFFFF,t_70)

### 总结


看似简单，但敲起来又会遇到坑的。通过生成词云图，对文章中出现频率较高的“关键词”予以视觉化的展现，帮助读者快速领略文章的主旨，既方便又高效！



在公众号回复 【CSDN 】 ，获取本文全套代码