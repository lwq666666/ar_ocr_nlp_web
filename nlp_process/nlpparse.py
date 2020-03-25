# -*- coding:utf-8 -*-

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
from nlp_process.AnalyzedifSign import replace
import gc

mw =["m","w","ws","wp"]
import copy

tagcansave=['ws','n','nd','nz','a']

def isnot_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return False
    return True

#后序遍历conlltree
def postOrderTraverse(conlltree,num,head_num):
    questionOrothers=[]
    if conlltree.nodes[num]["deps"]:
        for i in conlltree.nodes[num]["deps"]:
            for j in conlltree.nodes[num]["deps"][i]:
                questionOrothers.extend(postOrderTraverse(conlltree,j,num))
    if conlltree.nodes[num]['word'] is not None:
        if isnot_Chinese(conlltree.nodes[num]['word']):
            questionOrothers.append(conlltree.nodes[num]['word'])
        else:
            if conlltree.nodes[num]['rel']!='ROOT' and conlltree.nodes[num]['tag']in tagcansave and (conlltree.nodes[head_num]['rel']=='ROOT'or not conlltree.nodes[num]['deps']):
                 questionOrothers.append(conlltree.nodes[num]['word'])
    return questionOrothers
from nlp_process import SplitSentence

def testparse(sentence):
    sentence=replace(sentence)
    finalsentenceList =SplitSentence.splitbysymbol(SplitSentence.splitbynum(sentence))
    tmpsentenceList=copy.deepcopy(finalsentenceList)
    postaggerList = []


    model_path = "/usr/local/pyltp/ltp_data_v3.4.0/cws.model"
    userdict_path ='userdict.txt'
    segmentor =Segmentor()#实力化分词模块
    segmentor.load_with_lexicon(model_path,userdict_path)
    for sentenceList in finalsentenceList:
        tmpPostaggerList = []
        for index_one,sents in enumerate(sentenceList):
            sent = segmentor.segment(sents)
            # print('|'.join(sent))

            postagger =Postagger()
            postagger.load_with_lexicon("/usr/local/pyltp/ltp_data_v3.4.0/pos.model",userdict_path)  # 导入词性标注模块
            sent =list(sent)
            postags = list(postagger.postag(sent))
            # print(type(postags))
            # print(postags)
            postagger.release()
            # recognizer = NamedEntityRecognizer()
            # recognizer.load("/usr/local/pyltp/ltp_data_v3.4.0/ner.model")  # 导入命名实体识别模块
            # netags = recognizer.recognize(sent, postags)

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

                    equal_dic["equalExpresion"]=AddTimesSignAndBrackets.AddTimesSignAndBrackets(finalsentenceList[index][i][j])
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
                        # for j,value_1 in enumerate(postaggerList[index][value]):
                        #
                        #     if postaggerList[index][value][j] in mw:
                        #         postaggerList[index][value][j]='n'
                        #         #去除英文名词前后的中文名词
                                # if 'n' in postaggerList[index][value][j+1]:
                                #     postaggerList[index][value].pop(j+1)
                                #     finalsentenceList[index][value].pop(j+1)
                                # if 'n' in postaggerList[index][value][j-1]:
                                #     postaggerList[index][value].pop(j-1)
                                #     finalsentenceList[index][value].pop(j-1)


                        #进行取问题操作
                        parser = Parser()      #句法解析
                        parser.load("/usr/local/pyltp/ltp_data_v3.4.0/parser.model")
                        arcs = parser.parse(finalsentenceList[index][value], postaggerList[index][value])
                        parser.release()
                        # print(arcs)
                        arclen = len(arcs)
                        conll = ""
                        # relation_list=[[],[],[]]
                        for j in range(arclen):  # 构建Conll标准的数据结构
                            # print(arcs[j].head,arcs[j].relation)
                            if arcs[j].head == 0:
                                arcs[j].relation = "ROOT"
                            conll += "\t" + finalsentenceList[index][value][j] + "\t" + postaggerList[index][value][j] + "\t" + str(arcs[j].head) +"\t" +arcs[j].relation+"\t"  "\n"
                            # relation_list[0].append(finalsentenceList[index][value][j])
                            # relation_list[1].append(postaggerList[index][value][j])
                            # relation_list[2].append(arcs[j].head)
                        # print(conll)
                        # print(relation_list)
                        conlltree = DependencyGraph(conll)  # 转换为依存句法图
                        # print(conlltree)

                        #判断宽度是否为1
                        question_list=[]
                        # #宽度不为1
                        # if len(relation_list[2])!=len(set(relation_list[2])):
                        #     if(relation_list[1][relation_list[2].index(0)]=='v'):
                        #         for j,k in enumerate(relation_list[2]):
                        #             if(k==1 and relation_list[1][j]=='n'):
                        #                 question_list.append(relation_list[0][j])
                        # #宽度为1
                        # else:
                        #     if (relation_list[1][relation_list[2].index(0)] == 'v'):
                        #         for j, k in enumerate(relation_list[2]):
                        #             if (k == 1 and relation_list[1][j] == 'n'):
                        #                 question_list.append(relation_list[0][j])
                        # # print(question_list)
                        question_list=postOrderTraverse(conlltree,0,0)
                        # print(question_list)
                        if question_list:
                            relationslist = []
                            conditionslist = []
                            otherlist = []
                            if len(question_list) > 2:
                                if len(question_list)==3:
                                    conditionslist.append(question_list[:2])
                                    if not isnot_Chinese(conditionslist[0][0]) and isnot_Chinese(conditionslist[0][1]):
                                        tmp = conditionslist[0][0]
                                        conditionslist[0][0] = conditionslist[0][1]
                                        conditionslist[0][1] = tmp
                                elif len(question_list)==4:
                                    relationslist.append(question_list[:3])
                                    if isnot_Chinese(relationslist[0][0]) and not isnot_Chinese(relationslist[0][1]) and isnot_Chinese(relationslist[0][2]):
                                        tmp =relationslist[0][0]
                                        relationslist[0][0]=relationslist[0][2]
                                        relationslist[0][2]=relationslist[0][1]
                                        relationslist[0][1]=tmp

                                else:
                                    otherlist.append(question_list[:-2])
                                question_list=question_list[-2:]
                            if 'problems' in final_result_dict[index]:
                                final_result_dict[index]['problems'].append(question_list)
                            else:
                                final_result_dict[index]['problems']=[question_list]
                            tmpnum.append(value)
                            if otherlist:

                                if 'other' in final_result_dict[index]:
                                    final_result_dict[index]['others'].append(otherlist)
                                else:
                                    final_result_dict[index]['others'] = otherlist
                            if relationslist:

                                if 'other' in final_result_dict[index]:
                                    final_result_dict[index]['relations'].append(relationslist)
                                else:
                                    final_result_dict[index]['relations'] = relationslist
                            if conditionslist:

                                if 'other' in final_result_dict[index]:
                                    final_result_dict[index]['conditions'].append(conditionslist)
                                else:
                                    final_result_dict[index]['conditions'] = conditionslist
                if tmpnum:
                    for j in tmpnum:
                        tmplist[index].remove(j)

    # print(tmplist)
    #其他情况
    for index in range(len(tmplist)):
        relationslist=[]
        conditionslist=[]
        otherlist=[]
        if(tmplist[index]):
            for i in tmplist[index]:
                parser = Parser()  # 句法解析
                parser.load("/usr/local/pyltp/ltp_data_v3.4.0/parser.model")
                arcs = parser.parse(finalsentenceList[index][i], postaggerList[index][i])
                parser.release()
                # print(arcs)
                arclen = len(arcs)
                conll = ""
                # relation_list=[[],[],[]]
                for j in range(arclen):  # 构建Conll标准的数据结构
                    if arcs[j].head == 0:
                        arcs[j].relation = "ROOT"
                    conll += "\t" + finalsentenceList[index][i][j] + "\t" + postaggerList[index][i][j] + "\t" + str(arcs[j].head) + "\t" + arcs[j].relation + "\t"  "\n"

                # print(conll)
                # print(relation_list)
                conlltree = DependencyGraph(conll)  # 转换为依存句法图
                other_list = postOrderTraverse(conlltree, 0, 0)
                if other_list:
                    if len(other_list)==2:
                        if not isnot_Chinese(other_list[0])and isnot_Chinese(other_list[1]):
                            tmp = other_list[0]
                            other_list[0]=other_list[1]
                            other_list[1]=tmp
                        conditionslist.append(other_list)
                    elif len(other_list)==3:
                        relationslist.append(other_list)
                    else:
                        otherlist.append(tmpsentenceList[index][i])
        if otherlist:

            if 'other' in final_result_dict[index]:
                final_result_dict[index]['others'].append(otherlist)
            else:
                final_result_dict[index]['others'] = otherlist
        if relationslist:

            if 'other' in final_result_dict[index]:
                final_result_dict[index]['relations'].append(relationslist)
            else:
                final_result_dict[index]['relations'] = relationslist
        if conditionslist:

            if 'other' in final_result_dict[index]:
                final_result_dict[index]['conditions'].append(conditionslist)
            else:
                final_result_dict[index]['conditions'] = conditionslist

    deliver_dict={}
    deliver_dict["num"]=len(finalsentenceList)
    deliver_dict["problemEntity"]=[]
    for i in range(len(finalsentenceList)):
        deliver_dict["problemEntity"].append(final_result_dict[i])

    #转成json
    result_json =json.dumps(deliver_dict, ensure_ascii=False)
    # print(final_result_dict)
    # print(tmplist)
    for x in locals().keys():
        # print(locals()[x])
        del locals()[x]
    gc.collect()
    return result_json
# s1="已知函数f(x)=lnx-x+1/2a(x-1)^2+1。(1)讨论f(x)的单调性；(2)若x>=1,f(x)>=0恒成立，求实数a的取值范围."
# s1="已知sin(A)=1,sin(B+A)=0,求B的值"
# s1='已知在△ABC中，AB=√(3)，∠ABC=2*pi/3,BD是AC边上的高，AC=2√(3)BD.(1)求BC边的长;（2）求BC边中线AE的长'
# # #s1='∠ABC=120°，求BC边的长'
# s2 = testparse(s1)
# print(s2)
