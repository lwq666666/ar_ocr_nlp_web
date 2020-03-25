import config


#融合分散的矩形块
def rect_merge(locations):
    i=0
    while i< len(locations)-1:
        j=i+1
        while j<len(locations):
            #可以合并的情况
            #x2-x1+a1 y1-y2+b2>0 y2-y1+b1>0
            if locations[j][0]-locations[i][0]-locations[i][2]< config.MAX_BLANK_SIZE and\
                    ((locations[i][1] - locations[j][1] > 0 and locations[i][1] - locations[j][1] - locations[j][3] < config.MAX_BLANK_SIZE) or (locations[j][1] - locations[i][1] > 0 and locations[j][1] - locations[i][1] - locations[i][3] < config.MAX_BLANK_SIZE)):
                #若y1<y2
                if locations[i][1]<locations[j][1]:
                    #(x1,y1,x2-x1+a2,y2-y1+b2)
                    locations[i]=(locations[i][0],locations[i][1],locations[j][0]-locations[i][0]+locations[j][2],locations[j][1]-locations[i][1]+locations[j][3])
                else:
                    locations[i]=(locations[i][0],locations[j][1],locations[j][0]-locations[i][0]+locations[j][2],locations[i][1]-locations[j][1]+locations[i][3])
                locations.pop(j)

            else:
                j+=1
        i+=1
    return locations

#矩形块排序
def rect_range(locations):
    i=0
    while i<len(locations)-1:
        j=i+1
        p=0
        while j<len(locations) and j<len(locations)-p:
            if abs(locations[i][1]+locations[i][3] / 2 - locations[j][1]-locations[j][3] / 2) > config.ROW_SIZE:
                locations.append(locations[j])
                locations.pop(j)
                p+=1
            else:
                j+=1
        i=len(locations)-p
    return locations

#矩阵块按行排列
def rect_range_row(locations):
    row_locations={}
    row=0
    while locations:
        i=0
        j=0
        while i<len(locations) and abs(locations[i][1]+locations[i][3] / 2 - locations[j][1]-locations[j][3] / 2) <= config.ROW_SIZE:
            i+=1
        row_locations[row]=locations[0:i]
        row +=1
        locations=locations[i:]

    return row_locations







# original_img, binary_img = read_img_and_convert_to_binary('math1.jpg')
# # print(binary_img.shape,original_img.shape)
# symbols = binary_img_segment(binary_img,original_img)
#
# # print(symbols)
# locations = [x['location'] for x in symbols]
# print(len(locations),locations)
# locations=rect_merge(locations)
# print(len(locations),locations)
# locations =rect_range(locations)
# print(len(locations),locations)
# src_img=[]
#
# div_locations =find_div(locations)
# print(div_locations)
# locations =fraction_merge(locations,div_locations)
# #需要方式送入cnn识别
#
# print(locations)
#
# for location in locations:
#     if type(location)==tuple:
#         extracted_img=extract_img(location,binary_img,None)
#         src_img.append(extracted_img)
#
#     else:
#         print(location[1])
#         extracted_img=extract_img(location[1],binary_img,None)
#         src_img.append(extracted_img)
#         for head_location in location[2]:
#             extracted_img =extract_img(head_location,binary_img,None)
#             src_img.append(extracted_img)
#         for foot_location in location[3]:
#             extracted_img = extract_img(foot_location,binary_img,None)
#             src_img.append(extracted_img)
#
#
# symbols_to_be_predicted = normalize_matrix_value([x for x in src_img])
# # print(type(symbols_to_be_predicted[1]))
# # print(symbols_to_be_predicted[1])
# from PIL import Image
# for i,img in enumerate(symbols_to_be_predicted):
#     # print(img.shape)
#     tmp_img=Image.fromarray(img)
#     # print(tmp_img.format,tmp_img.mode)
#     tmp_img.save('tmp_img/'+str(i)+'.jpg')
#
#
# predictions = cnn_handwrite.recongnize(symbols_to_be_predicted)
#
# print(predictions)
