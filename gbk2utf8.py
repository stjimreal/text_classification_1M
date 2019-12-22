import os
import multiprocessing

def gbk2utf8(*args):
    filepath = args[0]
    try :
        fin = open(filepath, 'r', encoding='gbk')
        string = str(fin.read().encode('utf-8'), encoding='utf-8')
        fin.close()
        fout = open(filepath, 'w')
        fout.write(string)
        fout.close()
        print('Switch OK')
    except:
        try:
            fin = open(filepath, 'r', encoding='utf-8')
            s = fin.readline()
        except:
            print("[Warning] Unkown code type", filepath)

def iterdir(dirpath):
    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)
        if os.path.isdir(dirpath):
            continue
        gbk2utf8(filepath)

def main(route=''):
    for dir in os.listdir(route):
        pool = multiprocessing.Pool(6)
        dirpath = os.path.join(route, dir)
        if os.path.isfile(dirpath):
            continue
        print(dir)
        for file in os.listdir(dirpath):
            filepath = os.path.join(dirpath, file)
            if os.path.isdir(filepath) or file == '.DS_Store':
                continue
            # print(filepath)
            pool.apply_async(gbk2utf8, (filepath,))
            # gbk2utf8(filepath)
        pool.close()
        pool.join()

if __name__ == "__main__":
    main('DB/raw')
    # gbk2utf8('test/“P2P”第一案新进展 e租宝22人被公诉03_19_06.txt')