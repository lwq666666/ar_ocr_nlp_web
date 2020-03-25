import re
#将字符串中指定部分替换成指定字符
def replace(string, substitutions):

    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)


#数字字母后面带（字母或特定符号）加乘号
special_list=['!','@','#','$','%','&','√']

def AlpnumAndAlpSpe(string):
    i=0
    while i<len(string)-1:
        if string[i].isalnum() and (string[i + 1].isalpha() or string[i+1] in special_list):
            if string[i].isupper() and string[i+1].isupper():
                i+=1
                continue
            string = string[:i + 1] + '*' + string[i + 1:]
        i+=1
    return string
#带（）前后跟着字母加乘号
leftbrackets_list =['(','[','{']
rightbrackets_list =[')',']','}']
def BracketsAndAlp(string):
    i = 1
    while i<len(string):
        if (string[i] in leftbrackets_list) and string[i-1].isalpha():
            string = string[:i]+'*'+string[i:]
        i+=1
    i = 0
    while i<len(string)-1:
        if (string[i] in rightbrackets_list )and string[i+1].isalpha():
            string = string[:i+1]+'*'+string[i+1:]
        i+=1
    return string
#补全括号
def AddBrackets(string):
    i=0
    while i < len(string)-1:
        if string[i] in special_list and string[i+1].isalpha():
            string = string[:i+1]+'('+string[i+1]+')'+string[i+2:]
        i+=1
    return string

#将等式补全乘号和括号
def AddTimesSignAndBrackets(equal):
    replace_dic = {'sin': '!', 'f(x)': '@', 'cos': '#', 'tan': '$', 'cot': '%', 'ln': '&','sqrt':'√','pi':'π'}
    equal = replace(equal, replace_dic)
    equal = AlpnumAndAlpSpe(equal)
    equal = BracketsAndAlp(equal)
    equal = AddBrackets(equal)
    replace2_dic = dict(zip(replace_dic.values(), replace_dic.keys()))
    equal = replace(equal, replace2_dic)
    return equal

#
# equal='f(x)=asina+cosbsinc+(a+b)c+3ac'
# print(AddTimesSignAndBrackets(equal))