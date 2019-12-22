""" 
将爬取的内容完全相同的新闻删除，指针对名字进行了排除
 """

import os
import re
import multiprocessing

def parse_file_name(name:str):
    name = name.strip('.txt')
    if len(name) > 8 and name[-2:].isdigit() and name[-3] == '_' and name[-5:-3].isdigit() and name[-6] == '_' and name[-8:-6]:
        name = name[:-8]
    return name

def exclude(path):
    d = set()
    if not os.path.isdir(path):
        return
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            continue
        name = parse_file_name(file)
        if name not in d:
            d.add(name)
        else:
            os.remove(os.path.join(path, file))

""" 一样的参数可以产生不一样的结果可以用进程池 """
def iter_arsonal(path):
    # pool = multiprocessing.Pool(4)
    for dir in os.listdir(path):
        dirpath = os.path.join(path, dir)
        print(dirpath)
        # pool.apply_async(exclude, tuple(dirpath))
        exclude(dirpath)
    # pool.close()
    # pool.join()

if __name__ == "__main__":
    iter_arsonal('DB/raw')
