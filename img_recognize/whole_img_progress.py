import cv2
import numpy as np
import os
from PIL import Image
# from skimage.morphology import skeletonize

from img_recognize.cnn_handwrite import recongnize
# 水平投影
def getHProjection(image):
    hProjection = np.zeros(image.shape, np.uint8)
    # 图像高与宽
    h = img.shape[0]
    w = img.shape[1]
    # 长度与图像高度一致的数组
    h_ = [0]*h
    # 循环统计每一行白色像素个数
    for y in range(h):
        for x in range(w):
            if image[y, x] == 255:
                h_[y] += 1
    # 绘制水平投影图像
    for y in range(h):
        for x in range(h_[y]):
            hProjection[y, x] = 255
    cv2.imshow('hProjection', hProjection)
    return h_


def getVProjection(image):
    vProjection = np.zeros(image.shape, np.uint8)
    # 图像高与宽
    (h,w) = image.shape
    # 长度与图像宽度一致的数组
    w_ = [0]*w
    # 循环统计每一列白色像素的个数
    for x in range(w):
        for y in range(h):
            if image[y, x] == 255:
                w_[x] += 1
    # 绘制垂直平投影图像
    for x in range(w):
        for y in range(h-w_[x], h):
            vProjection[y, x] = 255
    cv2.imshow('vProjection', vProjection)
    # cv2.waitKey(0)
    return w_


def trim(img_arr):
    (row, col) = img_arr.shape
    tempr0 = 0
    tempr1 = 0
    tempc0 = 0
    tempc1 = 0
    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    threshold = 170
    img = np.array(img_arr)
    for r in range(0, row):
        for c in range(0, col):
            if img[r][c] < threshold:
                img[r][c] = 0
            else:
                img[r][c] = 255
    # 765 是255+255+255,如果是黑色背景就是0+0+0，彩色的背景，将765替换成其他颜色的RGB之和，这个会有一点问题，因为三个和相同但颜色不一定同
    for r in range(0, row):
        if img.sum(axis=1)[r] != 255 * col:
            tempr0 = r
            break

    for r in range(row - 1, 0, -1):
        if img.sum(axis=1)[r] != 255 * col:
            tempr1 = r
            break

    for c in range(0, col):
        if img.sum(axis=0)[c] != 255 * row:
            tempc0 = c
            break

    for c in range(col - 1, 0, -1):
        if img.sum(axis=0)[c] != 255 * row:
            tempc1 = c
            break

    new_img = img_arr[tempr0:tempr1 + 1, tempc0:tempc1 + 1]
    return new_img


if __name__ == '__main__':
    # 读入原始图像
    origineImage = cv2.imread('/Users/liweiqiang/PycharmProjects/ar_ocr/img_recognize/math5.jpg')
    print(origineImage.shape)
    # 图像灰度化
    image = cv2.cvtColor(origineImage, cv2.COLOR_BGRA2GRAY, )
    # cv2.imshow('gray', image)
    # 将图片二值化
    retval, img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    # 图像高宽
    h = img.shape[0]
    w = img.shape[1]
    Position = []
    H = getHProjection(img)

    start = 0
    H_Start = []
    H_End = []
    # 根据水平投射获取垂直分割位置
    for i in range(len(H)):
        if H[i] > 0 and start == 0:
            H_Start.append(i)
            start = 1
        if H[i] <= 0 and start == 1:
            H_End.append(i)
            start = 0
    len_ = len(H_Start) > len(H_End)  # 两个数组的长度差

    if len_ > 0:
        len_H_Start = len(H_Start) - len_
    elif len_ == 0:
        len_H_Start = len(H_Start)
    print(H_Start)
    print(H_End)
    # 分割行，分割之后再进行列分割并保存位
    for i in range(len_H_Start):
        # 获取行图像
        cropImg = img[H_Start[i]:H_End[i], 0:w]
        # cv2.imshow("cropImg", cropImg)
        # 对图像进行垂直投影
        W = getVProjection(cropImg)
        Wstart = 0
        Wend = 0
        W_Start = 0
        W_End = 0
        for j in range(len(W)):
            if W[j] > 0 and Wstart == 0:
                W_Start = j
                Wstart = 1
                Wend = 0
            if W[j] <= 0 and Wstart == 1:
                W_End = j
                Wstart = 0
                Wend = 1
            if Wend == 1:
                Position.append([W_Start, H_Start[i], W_End, H_End[i]])
                Wend = 0

    img_list = []
    precut_img_list = []
    for m in range(len(Position)):
        # 加矩形边框
        cv2.rectangle(origineImage, (Position[m][0], Position[m][1]), (Position[m][2], Position[m][3]), (0, 229, 238),
                      1)
        newimage = origineImage[Position[m][1]:Position[m][3], Position[m][0]:Position[m][2]]
        # 图像灰度化
        imgray = cv2.cvtColor(newimage, cv2.COLOR_BGRA2GRAY)
        # 图片二值化
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        # 图像宽与高
        h, w = thresh.shape
        # 删除长宽低于5个像素的
        if thresh.shape[0] * thresh.shape[1] > 25:
            cut_baibian = trim(thresh)
            cut_baibian = Image.fromarray(cut_baibian).resize((64, 64))
            cut_baibian = np.asarray(cut_baibian)
            print([Position[m][0], Position[m][3], w, h])
            precut_img_list.append([Position[m][0], Position[m][3], w, h])
            # print(type(cut_baibian))
            # print(cut_baibian.shape)
            # print(thresh.shape)
            # print('/n')
            img_list.append(cut_baibian)
            # cv2.imwrite('testres/%s.jpg' % m, cut_baibian)
    print(precut_img_list)
    img_list=np.asarray(img_list)
    print(img_list)
    print(img_list.shape)

    # cv2.waitKey(0)
    #最终获得的字符串
    str =recongnize(img_list)
    print(str)




# # 从img截取location区域的图像，并归一化成IMG_SIZE*IMG_SIZE
# def extract_img(location,img,contour=None):
#     x,y,w,h=location
#     # 只提取轮廓内的字符
#     if contour is None:
#         extracted_img = img[y:y + h, x:x + w]
#     else:
#         mask = np.zeros(img.shape, np.uint8)
#         cv2.drawContours(mask, [contour], -1, 255, cv2.FILLED)
#         img_after_masked = cv2.bitwise_and(mask, img)
#         extracted_img = img_after_masked[y:y + h, x:x + w]
#     # 将提取出的img归一化成IMG_SIZE*IMG_SIZE大小的二值图
#     black = np.zeros((64, 64), np.uint8)
#     if (w > h):
#         res = cv2.resize(extracted_img, (64, (int)(h * 64 / w)), interpolation=cv2.INTER_AREA)
#         d = int(abs(res.shape[0] - res.shape[1]) / 2)
#         black[d:res.shape[0] + d, 0:res.shape[1]] = res
#     else:
#         res = cv2.resize(extracted_img, ((int)(w * 64 / h), 64), interpolation=cv2.INTER_AREA)
#         d = int(abs(res.shape[0] - res.shape[1]) / 2)
#         black[0:res.shape[0], d:res.shape[1] + d] = res
#     extracted_img = skeletonize(black)
#     extracted_img = np.logical_not(extracted_img)
#     return extracted_img
#
# #将二值图里面的字符切割成单个字符，返回三维数组，每一个元素是一个字典，包含字符所在位置大小location，以及字符切割图src_img
# def binary_img_segment(binary_img,original_img=None):
#     # binary_img = skeletonize(binary_img)
#     # plot.imshow( binary_img,cmap = 'gray', interpolation = 'bicubic')
#     # plot.show()
#     #寻找每一个字符的轮廓，使用cv2.RETR_EXTERNAL模式，表示只需要每一个字符最外面的轮廓
#     img, contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#cv2.RETR_TREE
#     #cv2.drawContours(img_original, contours, -1, (0, 255, 0), 2)
#     if len(contours) > 50:
#         raise ValueError('symtem cannot interpret this image!')
#     symbol_segment_location = []
#     # 将每一个联通体，作为一个字符
#     symbol_segment_list = []
#     index = 1
#     for contour in contours:
#         location = cv2.boundingRect(contour)
#         x, y, w, h = location
#         if(w*h<100):
#             continue
#         symbol_segment_location.append(location)
#         # 只提取轮廓内的字符
#         extracted_img = extract_img(location,img,contour)
#         symbol_segment_list.append(extracted_img)
#         if len(original_img):
#             cv2.rectangle(original_img, (x, y), (x + w, y + h), (0, 0, 255), 3)
#         symbols=[]
#         for i in range(len(symbol_segment_location)):
#             symbols.append({'location':symbol_segment_location[i],'src_img':symbol_segment_list[i]})
#         # 对字符按字符横坐标排序
#         symbols.sort(key=lambda x:x['location'][0])
#     return symbols

