import json

import unicodedata
from pyltp import Segmentor, NamedEntityRecognizer, Postagger, SentenceSplitter, Parser
import re
from config import LTP_PATH
import re

#将字符串中指定部分替换成空格
def replace(string, substitutions):

    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)
mw =["w","ws","n","nh"]
#判断现有标记list中是否都是变量的类型
def allmw(postags):
    for tag in postags:
        if tag not in mw:
            return False
    return True
#等式解析
def equalparse(equal):
    equal_vars=[]
    #需要去掉的固定元素
    del_dic = {'sin': ' ', 'f(x)': ' ', 'cos': ' ', 'tan': ' ', 'cot': ' ', 'ln': ' ','pi':' ','sqrt':''}
    equal = replace(equal, del_dic)
    # print(equal)
    #将非零字符去除并替换成空格，方便分词处理
    equal = re.sub(u"([^a-zA-z])", ' ', equal)
    equal = equal.replace('^', ' ')
    # print(equal)
    model_path = LTP_PATH+"cws.model"
    userdict_path = 'nlp_process/equal.txt'
    segmentor = Segmentor()  # 实力化分词模块
    segmentor.load_with_lexicon(model_path, userdict_path)
    sent = segmentor.segment(equal)
    postagger = Postagger()
    postagger.load_with_lexicon(LTP_PATH+"pos.model", userdict_path)  # 导入词性标注模块
    sent = list(sent)
    postags = list(postagger.postag(sent))
    # print(sent,postags)

    # 取出变量去重
    if allmw(postags):
        equal_vars = list(set(sent))
    else:
        for i in range(len(sent)):
            if postags[i] in mw:
                equal_vars.append(sent[i])
        equal_vars = list(set(equal_vars))

    return equal_vars


def normalparse(normal):
    normal_var=[]

    return normal_var

# #测试equal-》var
# equal_va =equalparse("x>=1")
# print(equal_va)

