# -*- coding: utf-8 -*-
"""
# @Time    : 2018/05/26 下午5:13
# @Update  : 2018/09/28 上午10:30
# @Author  : zhanzecheng/片刻
# @File    : demo.py.py
# @Software: PyCharm
"""
import os
import jieba
from model import TrieNode
from utils import get_stopwords, load_dictionary, generate_ngram, save_model, load_model
from config import basedir


def load_data(filename, stopwords):
    """

    :param filename:
    :param stopwords:
    :return: 二维数组,[[句子1分词list], [句子2分词list],...,[句子n分词list]]
    """
    data = []
    with open(filename, 'r') as f:
        for line in f:
            word_list = [x for x in jieba.cut(line.strip(), cut_all=False) if x not in stopwords]
            data.append(word_list)
    return data


def load_data_2_root(data):
    print('------> 插入节点')
    for word_list in data:
        # tmp 表示每一行自由组合后的结果（n gram）
        # tmp: [['它'], ['是'], ['小'], ['狗'], ['它', '是'], ['是', '小'], ['小', '狗'], ['它', '是', '小'], ['是', '小', '狗']]
        ngrams = generate_ngram(word_list, 3)
        for d in ngrams:
            root.add(d)
    print('------> 插入成功')


if __name__ == "__main__":
    root_name = basedir + "/data/root.pkl"
    stopwords = get_stopwords()
    if os.path.exists(root_name):
        root = load_model(root_name)
    else:
        dict_name = basedir + '/data/dict.txt'
        word_freq = load_dictionary(dict_name)
        root = TrieNode('*', word_freq)
        save_model(root, root_name)

    # 加载新的文章
    filename = 'data/demo2.txt'
    data = load_data(filename, stopwords)
    # 将新的文章插入到Root中
    load_data_2_root(data)

    # 定义取TOP30个
    topN = 30
    result, add_word = root.find_word(topN)
    # 如果想要调试和选择其他的阈值，可以print result来调整
    # print("\n----\n", result)
    print("\n----\n", '增加了 %d 个新词, 词语和得分分别为: \n' % len(add_word))
    print('#############################')
    for word, score in add_word.items():
        print(word + ' ---->  ', score)
    print('#############################')

    # 前后效果对比
    test_sentence = '朝鲜核问题久拖不决的症结在于美国和朝鲜都采用威逼战略。朝鲜试图通过核导试验和虚言恫吓打破制裁、实现朝美关系正常化;美国则试图通过经济制裁和武力威胁迫使朝鲜无条件弃核。双方都试图迫使对方改变现状，立场相去甚远。解决朝核危机的关键在于朝鲜和美国都转变战略，变“双向威逼”为“双向吓阻”，即朝鲜用核武器吓阻美国的军事进攻，美国则吓阻朝鲜使用及扩散核武器。然后，按照中国提出的“双轨并进”思路，同时开展朝鲜半岛无核化及建立半岛和平机制谈判。'
    print('添加前：')
    print("".join([(x + '/ ') for x in jieba.cut(test_sentence, cut_all=False) if x not in stopwords]))

    for word in add_word.keys():
        jieba.add_word(word)
    print("添加后：")
    print("".join([(x + '/ ') for x in jieba.cut(test_sentence, cut_all=False) if x not in stopwords]))
