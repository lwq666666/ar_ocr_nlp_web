import unicodedata
table = {ord(f):ord(t) for f,t in zip(
     u'，。！？【】（）％＃＠＆１２３４５６７８９０；',
     u',.!?[]()%#@&1234567890;')}
#将句子分成多个小问
def splitbynum(sentence):
    sentence = sentence.translate(table)
    sentence = unicodedata.normalize('NFKC', sentence)
    sentence = sentence.replace("等于", '=')
    i=1
    sentenceList=[]
    onesentence=""
    index=0
    while index<len(sentence):
        if sentence[index]=='(' and sentence[index+1]==str(i) and sentence[index+2]==')':
            i=i+1
            index=index+3
            sentenceList.append(onesentence.strip())
            onesentence=""
        else:
            onesentence=onesentence+sentence[index]
            index=index+1
    sentenceList.append(onesentence.strip())
    while '' in sentenceList:
        sentenceList.remove('')
    for index in range(len(sentenceList)):
        sentenceList[index]=sentenceList[index]+'.'
    return sentenceList
#分成小短句
def splitbysymbol(sentenceList):
    finalsentenceList=[]
    cutLineFlag = ["？", "！", "。", "，", '.', '；', ';', ',']
    oneSentence = ""
    for index,sentence in enumerate(sentenceList):
        tmpList=[]
        for word in sentence:
            if word not in cutLineFlag:
                oneSentence = oneSentence + word
            else:
                tmpList.append(oneSentence.strip())
                oneSentence = ""
        while '' in tmpList:
            tmpList.remove('')
        finalsentenceList.append(tmpList)
    return finalsentenceList

# sentence ="已知函数f(x)=lnx-x+1/2a(x-1)^2+1。(1)讨论f(x)的单调性；(2)若x>=1,f(x)>=0恒成立，求实数a的取值范围"
# sentenceList =splitbynum(sentence)
# print(sentenceList)
# finalsentenceList =splitbysymbol(sentenceList)
# print(finalsentenceList)