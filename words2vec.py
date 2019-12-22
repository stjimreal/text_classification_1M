import os

import time

import pickle

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from sklearn.externals import joblib

def generateMatrix():
    """
    生成特征矩阵
    """
    vectorizer = CountVectorizer(min_df=0.001)

    for x in ['train', 'test']:
        # 分词数据的文件夹路径
        term_file_folder_path = 'data/%s/term/' % x
        # 特征矩阵保存路径
        matrix_path = 'matrix/%s/matrix.pkl' % x

        # 读取数据
        term_generator, target_generator = readTerm(term_file_folder_path)

        # 训练集拟合后转换为矩阵，测试集根据拟合好的矢量器直接转换为矩阵
        if x == 'train':
            matrix = vectorizer.fit_transform(term_generator)
            joblib.dump(vectorizer.vocabulary_, 'matrix/vocabulary.pkl')

        elif x == 'test':
            matrix = vectorizer.transform(term_generator)

        # 保存特征矩阵
        joblib.dump(matrix, matrix_path)



if __name__ == '__main__':

    with open(wordsPath, 'rb') as f:
        pickle.load(f)

    time_start = time.time()
    generateMatrix()
    print('Transform time:', time.time()-time_start, 's')



