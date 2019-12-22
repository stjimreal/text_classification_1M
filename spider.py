# -*- coding: UTF-8 -*-

import re

import sys

import json

import requests

import multiprocessing

import os

from bs4 import BeautifulSoup


def getNewsUrl(*params):
    url_param = {
        'channel': params[0],
        'page': str(params[1]),
        'show_all': '1',
        # 'cat_1': 'stock', #gnxw,
        'show_num': '5000',
        'tag': '1',
        'format': 'json',
    }

    proxiesSet = params[2]

    # 构造api的url
    api_url = 'http://api.roll.news.sina.com.cn/zt_list?'
    for key, value in url_param.items():
        api_url += key + '=' + value + '&'
    print(api_url)
    api_url = api_url[:-1]

    # 请求api数据
    response = requests.get(api_url)
    data = json.loads(response.content, encoding='utf-8')
    data = data['result']
    # print(data)
    if 'data' not in data:
        return
    data = data['data']

    # 提取新闻的url
    for term in data:
        url = term['url']
        yield url


def loadNews(*params):
    url = params[0]
    clsf = params[1]
    proxiesSet = params[3]

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 提取新闻id
    news_id = '-'.join(url.split('/')[-2:])
    news_id = re.sub(r'\..*', '', news_id)

    # 提取新闻内容
    news_content = [p.text for p in soup.select('p') if not p.findChildren()]
    news_content = '\n'.join(news_content)
    # print(news_content)

    # 存储新闻文本
    if len(news_content) >= 30 and not news_content.startswith('Privoxy encountered an error') and not news_content.startswith('1.请检查输入的网址是否正确。') and not news_content.startswith('没有找到相关文章...') and not news_content.startswith('\n\n Copyright © 1996 - 2018 SINA Corporation'):
        path = str(news_id + '.txt')
        with open(path, 'x') as f:
            f.write(news_content)
            f.close()


def runSpider(clsf, path):
    os.chdir(path)
    proxiesSet = {
    "http": None,
    "https": None,
    }

    for page in range(32, 40):
        pool = multiprocessing.Pool(4)
        urls = getNewsUrl(*(clsf, page, proxiesSet))
        print('Page',page)
        for url in urls:
            # loadNews(*(url, clsf))
            pool.apply_async(loadNews, (url, clsf, page, proxiesSet))
        pool.close()
        pool.join()


if __name__ == '__main__':
    # sports tech finance edu ent games fashion mil (news)
    runSpider('mil', 'DB/raw/军事')
