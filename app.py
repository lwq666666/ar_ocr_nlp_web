import base64

import cv2
from flask import Flask, request, Response, render_template
import json
app = Flask(__name__)
import numpy as np
import matplotlib.pyplot as plt
from img_recognize.whole_img_process_new import img_to_txt
from nlp_process.nlpparse import testparse
from nlp_process.Answer_parse import parse

@app.route("/health")
def health():
    result = {'status': 'UP'}
    return Response(json.dumps(result), mimetype='application/json')
@app.route("/getUser")
def getUser():
    result = {'username': 'python', 'password': 'python'}
    return Response(json.dumps(result), mimetype='application/json')
@app.route("/ImgRecognize", methods=['POST'])
def ImgRecognize():
    if request.method == "POST":

        Img = request.form['faceImg']
        by = str.encode(Img)
        by =base64.b64decode(by)
        img = cv2.imdecode(np.frombuffer(by, np.uint8), cv2.IMREAD_COLOR)
        res = img_to_txt(img)

        return res
    else:
        return "{'status': 'E0001'}"
from img_recognize.answer_img_process import answerimg_to_txt
# list 转成Json格式数据
def listToJson(lst):
    import json
    import numpy as np
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, ensure_ascii=False)  # json转为string

    return str_json

@app.route("/AnswerImgRecognize", methods=['POST'])
def ImgRecognize_a():
    if request.method == "POST":

        Img = request.form['AnswerImg']
        by = str.encode(Img)
        by =base64.b64decode(by)
        img = cv2.imdecode(np.frombuffer(by, np.uint8), cv2.IMREAD_COLOR)
        res = answerimg_to_txt(img)
        return_answer =json.dumps(res)
        print(return_answer)
        return return_answer
    else:
        return "{'status': 'E0001'}"
@app.route('/nlpRecognize', methods=['GET', 'POST'])
def question_parse():
    if request.method == 'POST':
        s1=request.form['string'] # 获取post穿过来的参数
          # 将请求参数解析成字典
        s2=testparse(s1)
        return s2
    else:
           # 获取get传过来的参数
        s1 = request.args['string']  # 将请求参数解析成字典
        s2=testparse(s1)
        return s2
@app.route('/nlpanswerRecognize', methods=['GET', 'POST'])
def answer_parse():
    answer = json.loads(request.form['answer'])
    answer_list= parse(answer)
    return answer_list
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug='True')
