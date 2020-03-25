# import cv2
#
# from img_recognize.tools import normalize_matrix_value_new
# from img_recognize.tools.img_preprocess import read_img_and_convert_to_binary,binary_img_segment,extract_img
#
# from img_recognize.tools import cnn_handwrite
#
# from img_recognize.tools.fraction_recognize import fraction_merge,find_div
# from img_recognize.tools.rect_change import rect_range,rect_merge
# import numpy as np
# original_img = cv2.imread('9.png')
# # print(original_img.shape)
# ## b.设置卷积核5*5
# kernel = np.ones((3,3), np.uint8)
#
# # c.图像的腐蚀，默认迭代次数
# original_img = cv2.erode(original_img, kernel)
# original_img, binary_img,binary_img_new = read_img_and_convert_to_binary(original_img)
# cv2.imwrite('tmp_img/huidu.png', binary_img_new)
#


import json
s1='["sin(A)=1","A=pi/2","sin(B+pi/2)=0","B+(pi/2)=pi","B=pi/2"]'
s2=json.loads(s1)
print(s2)