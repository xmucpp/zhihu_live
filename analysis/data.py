# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 00:04:10 2017

@author: Lily
"""
#data cleaning for zhihu_live

import re
import pandas as pd

# How to improve this code?
import sys
reload(sys)
sys.setdefaultencoding('utf8')

df_ended = pd.read_csv('live_ednde.csv')
df_ended = df_ended[df_ended<>0]
df_ongo = pd.read_csv('live_ongoing.csv')
df_ongo = df_ongo[df_ongo<>0]

# pick numbers from string


def pick_int(x):
    m = re.compile(r'\d+')
    num = m.findall(x)[0]
    if x == '0':
        x = None
    else:
        x = int(num)
    return x

# pick out the number
df_ongo['费用'] = df_ongo['费用'].map(pick_int)
df_ended['费用'] = df_ended['费用'].map(pick_int)

# fetch data: count the words
words = []
def count_words(text):
    text = text.decode('utf-8')
    num = 0
    for i in text:
        if i not in ' \n!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~':
            num += 1
    words.append(num)
    return words

# the data is useless


def count_mark(text):
    text = text.decode('utf-8')
    print text.count('?')

df_ongo['介绍'].map(count_words)
s1 = pd.DataFrame({'介绍字数': words})
df_ongo = pd.concat([df_ongo,s1],axis=1)

words=[]
df_ended['介绍'].map(count_words)
s2 = pd.DataFrame({'介绍字数': words})
df_ended = pd.concat([df_ended,s2],axis=1)

df_all = pd.concat([df_ended,df_ongo])


# save
df_ongo.to_csv('ongoing.csv')
df_ended.to_csv('ended.csv')
df_all.to_csv('all.csv')
