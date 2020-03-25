# -*- coding:utf-8 -*-

import sys
import os
import nltk
import json
from nlp_process import varparse
import unicodedata
from pyltp import Segmentor, NamedEntityRecognizer, Postagger, SentenceSplitter, Parser
from nltk.tree import Tree    #导入nltk tree结构
from nltk.grammar import DependencyGrammar  #导入依存句法包
from nltk.parse import *
from config import LTP_PATH

mw =["m","w","ws","wp"]
import copy


from nlp_process import SplitSentence
def testparse(sentence):
    finalsentenceList =SplitSentence.splitbysymbol(SplitSentence.splitbynum(sentence))
    tmpsentenceList=copy.deepcopy(finalsentenceList)
    postaggerList = []


    model_path = LTP_PATH+"cws.model"
    userdict_path ='nlp_process/userdict.txt'
    segmentor =Segmentor()#实力化分词模块
    segmentor.load_with_lexicon(model_path,userdict_path)
    for sentenceList in finalsentenceList:
        tmpPostaggerList = []
        for index_one,sents in enumerate(sentenceList):
            sent = segmentor.segment(sents)
            # print('|'.join(sent))

            postagger =Postagger()
            postagger.load_with_lexicon(LTP_PATH+"pos.model",userdict_path)  # 导入词性标注模块
            sent =list(sent)
            postags = list(postagger.postag(sent))
            # print(type(postags))
            # print(postags)
            recognizer = NamedEntityRecognizer()
            recognizer.load(LTP_PATH+"ner.model")  # 导入命名实体识别模块
            netags = recognizer.recognize(sent, postags)
            sentandpostags=list(zip(sent,postags))
            splist=[]
            for sp in sentandpostags:
                splist.append(list(sp))
            #整合词性
            for index,sp in enumerate(splist):
                while(index<len(splist)-1 and splist[index][1]in mw and splist[index+1][1]in mw ):
                    splist[index][0]=splist[index][0]+splist[index+1][0]
                    splist[index][1]="ws"
                    splist.pop(index+1)

            sents=[]
            postags=[]
            for sp in splist:
                sents.append(sp[0])
                postags.append(sp[1])
            sentenceList[index_one]=sents
            tmpPostaggerList.append(postags)
        # print(sentenceList,tmpPostaggerList)
        postaggerList.append(tmpPostaggerList)
    # print(finalsentenceList)
    # print(postaggerList)
    final_result_dict={}
    tmplist=[] #构造句子的结构，判断是否已取出有用数据
    #取出已知条件的等式
    for index in range(len(finalsentenceList)):
        num=len(finalsentenceList[index])
        tmpnum = list(range(num))
        #有用信息添加到输出结果
        result_dict={}
        for i in range(num):
            for j in range(len(finalsentenceList[index][i])):
                #将等式加入result
                if ('=' in finalsentenceList[index][i][j] and postaggerList[index][i][j]=='ws'and finalsentenceList[index][i][j][-1]!='='):
                    equal_dic ={}
                    equal_dic["equalExpresion"]=finalsentenceList[index][i][j]
                    equal_dic["vars"]=varparse.equalparse(finalsentenceList[index][i][j])
                    if 'equals' in result_dict:
                        result_dict['equals'].append(equal_dic)
                    else:
                        result_dict['equals']=[equal_dic]

                    if i in tmpnum:
                        tmpnum.remove(i)
        final_result_dict[index]=result_dict
        tmplist.append(tmpnum)


    #取出问题
    for index in range(len(tmplist)):
        if len(tmplist[index])!=0:
            tmpnum=[]
            if(index==0 and len(tmplist)==1)or(len(tmplist)>1 and index >0):
                for i,value in enumerate(tmplist[index]):
                    if(i==len(tmplist[index])-1):
                        for j,value_1 in enumerate(postaggerList[index][value]):

                            if postaggerList[index][value][j] in mw:
                                postaggerList[index][value][j]='n'
                                #去除英文名词前后的中文名词
                                if 'n' in postaggerList[index][value][j+1]:
                                    postaggerList[index][value].pop(j+1)
                                    finalsentenceList[index][value].pop(j+1)
                                if 'n' in postaggerList[index][value][j-1]:
                                    postaggerList[index][value].pop(j-1)
                                    finalsentenceList[index][value].pop(j-1)


                        #进行取问题操作
                        parser = Parser()      #句法解析
                        parser.load(LTP_PATH+"parser.model")
                        arcs = parser.parse(finalsentenceList[index][value], postaggerList[index][value])
                        # print(arcs)
                        arclen = len(arcs)
                        conll = ""
                        relation_list=[[],[],[]]
                        for j in range(arclen):  # 构建Conll标准的数据结构
                            # print(arcs[j].head,arcs[j].relation)
                            if arcs[j].head == 0:
                                arcs[j].relation = "ROOT"
                            conll += "\t" + finalsentenceList[index][value][j] + "(" + postaggerList[index][value][j] + ")" + "\t" + postaggerList[index][value][j] + "\t" + str(arcs[j].head) +  "\n"
                            relation_list[0].append(finalsentenceList[index][value][j])
                            relation_list[1].append(postaggerList[index][value][j])
                            relation_list[2].append(arcs[j].head)
                        # print(conll)
                        # print(relation_list)
                        #判断宽度是否为1
                        question_list=[]
                        if len(relation_list[2])!=len(set(relation_list[2])):
                            if(relation_list[1][relation_list[2].index(0)]=='v'):
                                for j,k in enumerate(relation_list[2]):
                                    if(k==1 and relation_list[1][j]=='n'):
                                        question_list.append(relation_list[0][j])
                        else:
                            if (relation_list[1][relation_list[2].index(0)] == 'v'):
                                for j, k in enumerate(relation_list[2]):
                                    if (k == 1 and relation_list[1][j] == 'n'):
                                        question_list.append(relation_list[0][j])
                        # print(question_list)
                        if question_list:
                            if 'problems' in final_result_dict[index]:
                                final_result_dict[index]['problems'].append(question_list)
                            else:
                                final_result_dict[index]['problems']=[question_list]
                            tmpnum.append(value)
                if tmpnum:
                    for j in tmpnum:
                        tmplist[index].remove(j)

    # print(tmplist)
    #其他情况
    for index in range(len(tmplist)):
        otherlist=[]
        if(tmplist[index]):
            for i in tmplist[index]:
                otherlist.append(tmpsentenceList[index][i])
        if otherlist:
            if 'other' in final_result_dict[index]:
                final_result_dict[index]['others'].append(otherlist)
            else:
                final_result_dict[index]['others'] = otherlist

    deliver_dict={}
    deliver_dict["num"]=len(finalsentenceList)
    deliver_dict["problemEntity"]=[]
    for i in range(len(finalsentenceList)):
        deliver_dict["problemEntity"].append(final_result_dict[i])

    #转成json
    result_json =json.dumps(deliver_dict, ensure_ascii=False)
    # print(final_result_dict)
    # print(tmplist)
    return result_json
# s1="已知函数f(x)=lnx-x+1/2a(x-1)^2+1。(1)讨论f(x)的单调性；(2)若x>=1,f(x)>=0恒成立，求实数a的取值范围."
#
# s2 = testparse(s1)
# print(s2)
