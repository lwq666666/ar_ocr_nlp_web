import sys
import os
import nltk
import json
from nlp_process import varparse
from nlp_process import AddTimesSignAndBrackets
import unicodedata
from pyltp import Segmentor, NamedEntityRecognizer, Postagger, SentenceSplitter, Parser
from nltk.tree import Tree    #导入nltk tree结构
from nltk.grammar import DependencyGrammar  #导入依存句法包
from nltk.parse import *
from nlp_process.AnalyzedifSign import replace,answer_replace
import gc
from nlp_process import SplitSentence

mw =["m","w","ws","wp"]
import copy

tagcansave=['ws','n','nd','nz','a']
def parse(answer_list):
    sentence_list = answer_replace(answer_list)
    tmpPostaggerList = []
    model_path = "/usr/local/pyltp/ltp_data_v3.4.0/cws.model"
    userdict_path = 'userdict.txt'
    segmentor = Segmentor()  # 实力化分词模块
    segmentor.load_with_lexicon(model_path, userdict_path)
    for index_one, sents in enumerate(sentence_list):
        sent = segmentor.segment(sents)
        # print('|'.join(sent))

        postagger = Postagger()
        postagger.load_with_lexicon("/usr/local/pyltp/ltp_data_v3.4.0/pos.model", userdict_path)  # 导入词性标注模块
        sent = list(sent)
        postags = list(postagger.postag(sent))
        # print(type(postags))
        # print(postags)
        postagger.release()
        # recognizer = NamedEntityRecognizer()
        # recognizer.load("/usr/local/pyltp/ltp_data_v3.4.0/ner.model")  # 导入命名实体识别模块
        # netags = recognizer.recognize(sent, postags)

        sentandpostags = list(zip(sent, postags))
        splist = []
        for sp in sentandpostags:
            splist.append(list(sp))
        # 整合词性
        for index, sp in enumerate(splist):
            while (index < len(splist) - 1 and splist[index][1] in mw and splist[index + 1][1] in mw):
                splist[index][0] = splist[index][0] + splist[index + 1][0]
                splist[index][1] = "ws"
                splist.pop(index + 1)

        sents = []
        postags = []
        for sp in splist:
            sents.append(sp[0])
            postags.append(sp[1])
        sentence_list[index_one] = sents
        tmpPostaggerList.append(postags)

    # 取出已知条件的等式
    num = len(sentence_list)
    tmpnum = list(range(num))
    final_result_dict = {}
    tmplist = []  # 构造句子的结构，判断是否已取出有用数据
    # 有用信息添加到输出结果
    for i in range(num):
        result_dict = {}
        for j in range(len(sentence_list[i])):
            # 将等式加入result
            if ('=' in sentence_list[i][j] and tmpPostaggerList[i][j] == 'ws' and sentence_list[i][j][-1] != '='):
                equal_dic = {}

                equal_dic["equalExpresion"] = AddTimesSignAndBrackets.AddTimesSignAndBrackets(sentence_list[i][j])
                equal_dic["vars"] = varparse.equalparse(sentence_list[i][j])

                result_dict['equals'] = equal_dic
                result_dict["type"] = 0
                if i in tmpnum:
                    tmpnum.remove(i)
            final_result_dict[i] = result_dict
            tmplist.append(tmpnum)

    deliver_dict = {}
    deliver_dict["num"] = len(sentence_list)
    deliver_dict["nlpAnswerRootEntity"] = []
    for i in range(len(sentence_list)):
        deliver_dict["nlpAnswerRootEntity"].append(final_result_dict[i])
        # 转成json
    answer_json = json.dumps(deliver_dict, ensure_ascii=False)
    # print(final_result_dict)
    # print(tmplist)
    for x in locals().keys():
        # print(locals()[x])
        del locals()[x]
    gc.collect()
    return answer_json



# answer_list = ["∵sin(A)=1", "∴A=pi/2", "∴sin(B+pi/2)=0", "∴B+pi/2=pi", "∴B=pi/2"]
# print(parse(answer_list))