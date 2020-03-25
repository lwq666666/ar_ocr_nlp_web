import config


#将location的第i个元素返回
def takeone(elem,i):
    if type(elem)==tuple:
        return elem[i]
    else:
        return elem[0][i]
# list1=[[(3,4,5,6)],(1,2,3,4)]
# list1.sort(key = lambda x: takeforth(x))
# print(list1)
# # l1 =[(1,2,3,4)]
# print(takeforth(l1))

#找出所有分号
def find_div(locations):
    div_locations=[]
    for i in range(len(locations)):
        if locations[i][2]/locations[i][3] > config.DIV_LONG_WIDE:
            div_locations.append(locations[i])
    #按照长度升序
    div_locations.sort(key=lambda x:takeone(x,3))
    return div_locations
#
# locations =[(12, 106, 82, 114), (201, 140, 56, 45), (435, 28, 38, 95), (437, 153, 352, 66), (482, 296, 53, 78), (607, 315, 56, 25), (702, 267, 80, 184), (548, 22, 71, 69), (714, 5, 48, 70)]
# div =find_div(locations)
# print(div)

#将分式整合起来
def fraction_merge(locations,div_locations):
    for div_location in div_locations:
        index =locations.index(div_location)
        if index!=-1:
            tmp_div_list=[[],[],[],[]]
            tmp_div_list[1]=div_location
            #找前面和后面的部分
            for i in range(len(locations)):
                #若是单一字符并且不是当前位置
                if i!=index and type(locations[i])==tuple:
                    #如果 x2<x1+a1/2<x2+a2 |y1-(y2+b2)|<设定宽度或|y2-(y1+b1)|<设定宽度
                    if locations[i][0]+locations[i][2]/2 >div_location[0] and locations[i][0]+locations[i][2]/2<div_location[0]+div_location[2] and (abs(div_location[1]-locations[i][1]-locations[i][3]) < config.DIV_BLANK_SIZE or abs(locations[i][1] - div_location[1] - div_location[3]) < config.DIV_BLANK_SIZE):
                        #按照y的中点确定 分号在下
                        if div_location[1]+div_location[3]/2>locations[i][1]+locations[i][3]/2:
                            tmp_div_list[2].append(locations[i])
                        #分号在上
                        else:
                            tmp_div_list[3].append(locations[i])
                #若是复合字符（目前是分式）
                elif type(locations[i])==list:
                    if locations[i][0][0]+locations[i][0][2]/2 >div_location[0] and locations[i][0][0]+locations[i][0][2]/2<div_location[0]+div_location[2] and (div_location[1] - locations[i][0][1] - locations[i][0][3] < config.DIV_BLANK_SIZE or locations[i][0][1] - div_location[1] - div_location[3] < config.DIV_BLANK_SIZE):
                        if div_location[1] + div_location[3] / 2 > locations[i][0][1] + locations[i][0][3] / 2:
                            tmp_div_list[2].append(locations[i])
                        else:
                            tmp_div_list[3].append(locations[i])
            # 合并一个新的
            if len(tmp_div_list[2])>0 and len(tmp_div_list[3])>0:
                #找到最大边框
                tmp_div_list[2].sort(key=lambda x :takeone(x,0))
                tmp_div_list[3].sort(key=lambda x :takeone(x,0))
                x1=div_location[0]
                y1=div_location[1]
                x2=div_location[0]+div_location[2]
                y2=div_location[1]+div_location[3]
                for location in tmp_div_list[2]:
                    if takeone(location,0)<x1:
                        x1=takeone(location,0)
                    if takeone(location,1)<y1:
                        y1=takeone(location,1)
                    if takeone(location,0)+takeone(location,2)>x2:
                        x2=takeone(location,0)+takeone(location,2)
                    if takeone(location,1)+takeone(location,3)>y2:
                        y2=takeone(location,1)+takeone(location,3)
                for location in tmp_div_list[3]:
                    if takeone(location,0)<x1:
                        x1=takeone(location,0)
                    if takeone(location,1)<y1:
                        y1=takeone(location,1)
                    if takeone(location,0)+takeone(location,2)>x2:
                        x2=takeone(location,0)+takeone(location,2)
                    if takeone(location,1)+takeone(location,3)>y2:
                        y2=takeone(location,1)+takeone(location,3)

                #tmp_div_list=[(),(),[],[]],1为新的边框，2为分号位置，3为上边的内容，4为下边的内容
                tmp_div_list[0]=(x1,y1,x2-x1,y2-y1)
                locations[index]=tmp_div_list
                #删除原来的字符
                for location in tmp_div_list[2]:
                    locations.remove(location)
                for location in tmp_div_list[3]:
                    locations.remove(location)
    return locations

# locations = [(12, 106, 82, 114), (201, 140, 56, 45), (435, 28, 38, 95), (437, 153, 352, 66), (482, 296, 53, 78), (607, 315, 56, 25), (702, 267, 80, 184), (548, 22, 71, 69), (714, 5, 48, 70)]
# div_locations =find_div(locations)
# print(div_locations)
# locations =fraction_merge(locations,div_locations)
# print(locations)