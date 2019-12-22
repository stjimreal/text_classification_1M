import os
import json
import csv
import string

def write_to_csv(list, path, str):
    headers = ['id', 'content', 'tag']
    with open(os.path.join(path, str+'RawDB') + '.csv', 'x', newline='') as f:
        f_csv = csv.writer(f, delimiter='\t')
        f_csv.writerow(headers)
        f_csv.writerows(list)
        f.close()


def dir_to_csv(pathname, dumpPath):
    trainlist = []
    testlist = []
    for subdir in os.listdir(pathname):
        path = os.path.join(pathname, subdir)
        if os.path.isfile(path) or subdir == '.DS_Store':
            continue
        extract(path, subdir, trainlist, testlist)
        
    write_to_csv(trainlist, dumpPath, 'train')
    write_to_csv(testlist, dumpPath, 'test')

    return

def extract(path, topic, trainlist, testlist):
    for cnt, name in enumerate(os.listdir(path)):
        oneline = [-1]
        filepath = os.path.join(path, name)
        if os.path.isfile(filepath):
            # print(path)
            if name == '.DS_Store':
                continue
            try:
                fin = open(filepath, 'r', encoding='utf-8')
                oneline.append(fin.read())
            except:
                print('[Warning]Unkown Encode', filepath)
                continue
            fin.close()

            cnt += 1
            oneline[0] = cnt
            oneline.append(topic)
        if cnt < 50000:
            trainlist.append(oneline)
        else:
            testlist.append(oneline)
        

    print(cnt)


""" 把新闻从总的数据库取出来每类50000个并且移除原来的文本, args是类别"""
if __name__ == "__main__":
    dir_to_csv('DB/raw', 'DB')