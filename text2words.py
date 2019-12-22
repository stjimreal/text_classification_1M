# encoding=utf-8
import os
import sys
import time
import csv

import pickle


import multiprocessing

import re
import pynlpir
import jieba

import show

from copy import deepcopy

def each2words(*args):
    """
    将Text文本文件转为Term分词文件
    此函数作为可重入代码
    使用中科院分词系统pynlpir
    """

    """ 第一个参数是字符串文件内容，第二个是停用词表 """
    assert len(args) == 2
    text = args[0]
    stopwordsList = args[1]

    # try:
        # current = pynlpir.segment(text)
    # except:
    #     print('[WARNING] Unkown Type')
    #     raise RuntimeError

    # 分词只分出名词
    content = list()
    for word in jieba.cut(text):
        word = word.strip()
        if word not in stopwordsList and len(word) >= 2 and not word.isnumeric() and not word.isspace():
            content.append(word)

    # 存储content: list
    return deepcopy(content)

def getStop():
    """
    获取停用词表
    """

    stopwordsList = set()
    with open('stop_words_ch-停用词表.txt', 'r') as fin:
        stopwordsList = set(lines.strip() for lines in fin)
        fin.close()
    assert len(stopwordsList) > 0

    return deepcopy(stopwordsList)

def text2Word(csvPath, dumpPath):
    """
    处理指定CSV文件，输出分词后数据到dumpPath
    """

    # 初始化pynlpir分词
    # pynlpir.open(encoding='utf-8')

    # 初始化返回列表
    retDB = []
    # 获取停用词
    stopwordsList = getStop()

    with open(csvPath, 'r', encoding='utf-8') as fin:
        reader = csv.reader(fin, delimiter='\t')
        headers = next(reader)
        for id, line in enumerate(reader):
            # 调用文本转向量的进程
            try:
                content = each2words(line[1], stopwordsList)
            except:
                print('[ERROR] Parse Failure')
                continue
            retDB.append((line[0], content, line[2]))
            # if id % 500 == 0:
            #     pynlpir.close()
            #     pynlpir.open(encoding='utf-8')
            if id >= 50:
                # pynlpir.close()
                break


    for id, content, tag in retDB[-2:]:
        print(id, content, tag)
    try:
        outPath = os.path.join(dumpPath, 'words.pkl')
        f = open(outPath, 'xb')
        pickle.dump(retDB, f)
    except:
        print('[WARNING]No output')


if __name__ == '__main__':

    """ (序号，文件内容，标签) """
    beg = time.time()
    pool = multiprocessing.Pool(2)

    l = [('DB/rawTestDB.csv', '.'), ('DB/rawTrainDB.csv', './test')]

    for i in range(2):
        pool.apply_async(text2Word, l[i])

    pool.close()
    pool.join()
    end = time.time()
    print('\n\nConsumed time:', end - beg)
    
    
