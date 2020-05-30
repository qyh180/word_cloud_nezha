# encoding:gbk
import csv
import json
import os

import requests
import time
import pandas as pd
import random
from lxml import etree
from io import BytesIO
import jieba
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import time

class nezha:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
        self.url = 'https://movie.douban.com/subject/26794435/comments?start=%d&limit=20&sort=new_score&status=P'


    def get_comments(self):
        users =[]
        stars = []
        date_times = []
        comment_texts = []
        for i in range(0, 500, 20):
            response = requests.get(self.url % i, headers=self.headers)
            list_comments = etree.HTML(response.text)
            comments = list_comments.xpath("//div[@class='comment-item']")
            # user_01 = list_comments.xpath("//h3/span[@class='comment-info']/span[3]/@title")
            dic_comments = {}
            for comment in comments:
                user = comment.xpath(".//h3/span[@class='comment-info']/a/text()")
                star = comment.xpath(".//h3/span[@class='comment-info']/span[2]/@title")[0]
                date_time = comment.xpath(".//h3/span[@class='comment-info']/span[3]/@title")
                if len(date_time) != 0:
                    date_time = date_time[0]
                else:
                    date_time = None
                comment_text = comment.xpath(".//p/span[@class='short']/text()")[0].strip()
                users.append(user)
                stars.append(star)
                date_times.append(date_time)
                comment_texts.append(comment_text)
                print(user,star,date_time, comment_text)

            time.sleep(0.5)
        comment_dic = {'user': users, 'star': stars, 'time': date_times, 'comments': comment_texts}
        comments_df = pd.DataFrame(comment_dic)
        comments_df.to_csv('nezha_comments.csv')
        comments_df['comments'].to_csv('comment_only.csv', index=False)


    def jieba_(self):
        # 打开评论数据文件
        content = open('comment_only.csv', 'r', encoding='utf-8').read()
        # jieba分词
        word_list = jieba.cut(content)
        # 添加自定义词，该片经典台词‘我命由我不由天’必须加进去
        with open('自定义词.txt', encoding='utf-8') as f:
            jieba.load_userdict(f)
        # 新建列表，收集词语
        word = []
        # 去掉一些无意义的词和符号，我这里自己整理了停用词库
        for i in word_list:
            with open('停用词库.txt', encoding='utf-8') as f:
                meaningless_file = f.read().splitlines()
                f.close()
            if i not in meaningless_file:
                word.append(i.replace(' ', ''))
        # 全局变量，方便词云使用
        global word_cloud
        # 用逗号隔开词语
        word_cloud = '，'.join(word)
        print(word_cloud)

    def word_cloud_(self):
        # 打开你喜欢的词云展现背景图，这里选用哪吒电影里的图片
        cloud_mask = np.array(Image.open('nezha.jpg'))
        # 定义词云的一些属性
        wc = WordCloud(
            background_color="white",  # 背景图分割颜色为白色
            mask=cloud_mask,  # 背景图样
            max_words=300,  # 显示最大词数
            font_path='./fonts/simhei.ttf',  # 显示中文
            min_font_size=5,  # 最小尺寸
            max_font_size=100,  # 最大尺寸
            width=400  # 图幅宽度
        )
        # 使用全局变量，刚刚分出来的词
        global word_cloud
        # 词云函数
        x = wc.generate(word_cloud)
        # 生成词云图片
        image = x.to_image()
        # 展示词云图片
        image.show()
        # 保存词云图片
        wc.to_file('pic.png')

# print(response.status_code)
# print(response.text)

nezha = nezha()
nezha.get_comments()
nezha.jieba_()
nezha.word_cloud_()
