import re
#将字符串中指定部分替换成指定字符
def replace(string):
    replace_sign = {'∠': '角', '△': '三角形','√':'sqrt','√':'sqrt','∵':'因为','∴':'所以'}

    substrings = sorted(replace_sign, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: replace_sign[match.group(0)], string)

def answer_replace(answer_list):
    for i,answer in enumerate(answer_list):
        answer_list[i]=replace(answer)

    return answer_list
