import cv2

from img_recognize.tools import normalize_matrix_value
from img_recognize.tools.img_preprocess import read_img_and_convert_to_binary,binary_img_segment,extract_img

from img_recognize.tools import cnn_handwrite

from img_recognize.tools.fraction_recognize import fraction_merge,find_div
from img_recognize.tools.rect_change import rect_range,rect_merge,rect_range_row
import numpy as np
def answerimg_to_txt(original_img):
    #original_img = cv2.imread('math1.jpg')
    kernel = np.ones((3, 3), np.uint8)

    # c.图像的腐蚀，默认迭代次数
    original_img = cv2.erode(original_img, kernel)
    original_img, binary_img, binary_img_new = read_img_and_convert_to_binary(original_img)
    # print(binary_img.shape,original_img.shape)
    symbols = binary_img_segment(binary_img, binary_img_new, original_img)

    # print(symbols)
    locations = [x['location'] for x in symbols]
    # print(len(locations), locations)
    locations = rect_merge(locations)
    # print(len(locations), locations)
    locations = rect_range(locations)
    # print(len(locations), locations)
    locations_row =rect_range_row(locations)
    return_list=[]
    for (index,locations) in locations_row.items():
        src_img = []

        div_locations = find_div(locations)
        # print(div_locations)
        locations = fraction_merge(locations, div_locations)
        # 需要方式送入cnn识别

        for location in locations:
            if type(location) == tuple:
                extracted_img = extract_img(location, binary_img_new, None)
                src_img.append(extracted_img)

            else:
                extracted_img = extract_img(location[1], binary_img_new, None)
                src_img.append(extracted_img)
                for head_location in location[2]:
                    extracted_img = extract_img(head_location, binary_img_new, None)
                    src_img.append(extracted_img)
                for foot_location in location[3]:
                    extracted_img = extract_img(foot_location, binary_img_new, None)
                    src_img.append(extracted_img)
        # print(src_img)
        symbols_to_be_predicted = np.array([x for x in src_img])
        # print(symbols_to_be_predicted.shape)
        # print(symbols_to_be_predicted[0].shape)
        # # print(type(symbols_to_be_predicted[1]))
        # # print(symbols_to_be_predicted[1])
        # # print(symbols_to_be_predicted.shape)
        # from PIL import Image
        # for i, img in enumerate(symbols_to_be_predicted):
        #     # print(img.shape)
        #     tmp_img = Image.fromarray(img)
        #     # print(tmp_img.format,tmp_img.mode)
        #     tmp_img.save('tmp_img/' + str(i) + '.jpg')
        # print(symbols_to_be_predicted)
        predictions = cnn_handwrite.recongnize(symbols_to_be_predicted)

        # print(predictions)

        str1 = ''
        j = 0
        for i, location in enumerate(locations):

            if type(location) == tuple:
                str1 += predictions[j]['symbol']
                j += 1
            else:
                tmp_str = ''
                if predictions[j]['symbol'] == '-'or predictions[j]['symbol']=='一':
                    tmp_symbol = '/'
                else:
                    tmp_symbol = predictions[j]['symbol']
                j += 1
                if (len(location[2]) > 1):
                    tmp_str += '('
                for head_location in location[2]:
                    tmp_str += predictions[j]['symbol']
                    j += 1
                if (len(location[2]) > 1):
                    tmp_str += ')'
                tmp_str += tmp_symbol
                if (len(location[3]) > 1):
                    tmp_str += '('
                for foot_location in location[3]:
                    tmp_str += predictions[j]['symbol']
                    j += 1
                if (len(location[3]) > 1):
                    tmp_str += ')'
                str1 += tmp_str
        return_list.append(str1)
    return return_list

# img =cv2.imread("12.png")
#
# # print(img)
# str =img_to_txt(img)
# print(str)