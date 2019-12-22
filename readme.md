# 数据挖掘与数据仓库大作业——文本分类(中文)

## 数据预处理

### 关键词提取(tokenize)

> 方法：  

1. 分词工具、中科院的分词工具——pynlpir: `pip install pynlpir; pynlpir update`
2. 只取名词  
3. 去除停用词  
4. 允许用英文(词根还原)斯坦福的包(nltk)

爬虫程序参考[[github]新浪新闻文本分类](https://github.com/qyfang/TextClassification)项目`spider.py`完成，使用了新浪滚动新闻[API](http://api.roll.news.sina.com.cn/)和清华开放新闻数据[THUCNEWS](http://thuctc.thunlp.org/message)，爬取100w 篇文本。

`dir2csv.py`将以文件保存的文本处理成csv格式，并且分成训练集与测试集(后续用sklearn卡方检验降维时又合在一起，可能没有研究清楚接口)

`text2words.py`将csv格式自然语言文本用`pynlpir`转成`List`，需要注意`pynlpir`内存占用过大时，可以在处理特定数量(比如5000例)的时候释放一下再打开，分词用时可能比较长，两个进程用了`4h`

>注意：  
TF/IDF ——> 有问题  单纯CHI也有问题  
TF/IDF ✖️ CHI 做一个加权？

### Vectorizer、TSR

文本的向量表示方法——过万的维度(1W - 10W)

1、去噪(分词已经去除了停用词)  
2、维度灾难问题(可采用chi2_TF/IDF方法、PDA、LDA等)  
100万篇中/英文本

(LDA不适合处理短文本，可以运用知识图谱的方法对短文本进行二次主题加权)

>使用`sklearn`进行数据预处理:  
仅利用`df`进行降维: `preprocess_baseline.ipynb`(`df_min` = 0.001)  
`chi`卡方检验降维: `chi2_result.ipynb`、`chi2_preprosess.ipynb`

`sklearn`在上述两种情况下的训练结果F1-Score分别为`86%`、`90%`

## 训练：每类不超过50% 如果测试集远远大于训练集可以加分

内容：

### 一、基本项：朴素贝叶斯方法

### 二、SVM可以加分

### 三、其他的方法(Adaboost)

## 性能测试：召回率、准确率、F1-Score
