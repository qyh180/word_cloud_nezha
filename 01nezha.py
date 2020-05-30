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
        # �����������ļ�
        content = open('comment_only.csv', 'r', encoding='utf-8').read()
        # jieba�ִ�
        word_list = jieba.cut(content)
        # ����Զ���ʣ���Ƭ����̨�ʡ��������Ҳ����졯����ӽ�ȥ
        with open('�Զ����.txt', encoding='utf-8') as f:
            jieba.load_userdict(f)
        # �½��б��ռ�����
        word = []
        # ȥ��һЩ������Ĵʺͷ��ţ��������Լ�������ͣ�ôʿ�
        for i in word_list:
            with open('ͣ�ôʿ�.txt', encoding='utf-8') as f:
                meaningless_file = f.read().splitlines()
                f.close()
            if i not in meaningless_file:
                word.append(i.replace(' ', ''))
        # ȫ�ֱ������������ʹ��
        global word_cloud
        # �ö��Ÿ�������
        word_cloud = '��'.join(word)
        print(word_cloud)

    def word_cloud_(self):
        # ����ϲ���Ĵ���չ�ֱ���ͼ������ѡ����߸��Ӱ���ͼƬ
        cloud_mask = np.array(Image.open('nezha.jpg'))
        # ������Ƶ�һЩ����
        wc = WordCloud(
            background_color="white",  # ����ͼ�ָ���ɫΪ��ɫ
            mask=cloud_mask,  # ����ͼ��
            max_words=300,  # ��ʾ������
            font_path='./fonts/simhei.ttf',  # ��ʾ����
            min_font_size=5,  # ��С�ߴ�
            max_font_size=100,  # ���ߴ�
            width=400  # ͼ�����
        )
        # ʹ��ȫ�ֱ������ոշֳ����Ĵ�
        global word_cloud
        # ���ƺ���
        x = wc.generate(word_cloud)
        # ���ɴ���ͼƬ
        image = x.to_image()
        # չʾ����ͼƬ
        image.show()
        # �������ͼƬ
        wc.to_file('pic.png')

# print(response.status_code)
# print(response.text)

nezha = nezha()
nezha.get_comments()
nezha.jieba_()
nezha.word_cloud_()
