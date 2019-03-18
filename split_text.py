#coding = utf-8
#将

import cv2
import os

yuzhi = 150
def row_column_split(image_path):
    """
    将一个单元格文本按行切割后，再按列切割成一个个单字符
    :param image_path:
    :return:
    """
    """准备好待切割的文本，并按某个阈值二值化，获得比较容易切割的图像"""
    image_name = os.path.basename(image_path)[:-4]
    src = cv2.imread(image_path)
    gray_src = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(r'.\data\gray_src_test.png',gray_src)
    _, thresh_src = cv2.threshold(gray_src, yuzhi, 255, cv2.THRESH_BINARY)#不同阈值获得的图像清晰度不同
    # cv2.bitwise_not(thresh_src, thresh_src)  # 取反
    # thresh_src = cv2.adaptiveThreshold(gray_src,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 2)


    cv2.imwrite(r'.\data\test.png',thresh_src)
    # kernel_rect_3_3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # fix_src = cv2.morphologyEx(thresh_src,cv2.MORPH_ERODE,kernel_rect_3_3,None,None,1)
    # cv2.imwrite(r'.\data\fix_src.png',fix_src)
    # thresh_src = fix_src


    """下面是切割算法"""
    start = None
    end = None
    range_sum = thresh_src.sum(axis=1)  # 获取按某个方向的分组求和
    row_list = []
    start_mark = True
    end_mark = False
    row_split_num = 0
    for i, col_i in enumerate(range_sum):
        if start_mark:
            if col_i != row_split_num:
                start = i
                start_mark = False
                end_mark = True
        if end_mark:
            if col_i == row_split_num:
                end = i-1
                end_mark = False
                start_mark = True
                row_list.append((start,end))
    sigle_text_list = []
    for row_i in row_list:
        image_text = thresh_src[row_i[0]:row_i[1]]
        cv2.imwrite(r'.\data\image_text.png', image_text)

        start = None
        end = None
        range_sum = image_text.sum(axis=0)  # 获取按某个方向的分组求和
        column_list = []
        start_mark = True
        end_mark = False
        col_split_num = 256*0
        for i, col_i in enumerate(range_sum):
            if start_mark:
                if col_i > col_split_num:
                    start = i
                    start_mark = False
                    end_mark = True
            if end_mark:
                if col_i <= col_split_num or i == len(range_sum)-1:
                    end = i - 1
                    end_mark = False
                    start_mark = True
                    column_list.append((start, end))
                    sigle_text_list.append([row_i,(start,end)])



        # width_list = []
        # for col_i in column_list:
        #     width_list.append(col_i[1]-col_i[0])
        # width_counter = Counter(width_list)
        # width_avg = width_counter.most_common(1)[0][0]
        # width_ratio_list = []
        # for wid_i in width_list:
        #     width_ratio_list.append(int(wid_i/width_avg))
        # to_split_list = []
        # for i,ratio in enumerate(width_ratio_list):
        #     if ratio > 1:
        #         to_split_list.append((i,ratio))
        # index_list = []
        # if to_split_list:
        #     splited_column_list = []
        #     for to_split in to_split_list:
        #         column_num = column_list[to_split[0]]
        #         each_width = width_list[to_split[0]] /to_split[1]
        #         new_column_num_list = []
        #         for i in range(to_split[1]):
        #             new_column_num_list.append((int(column_num[0]+i * each_width),int(column_num[0] + (i+1) *each_width)))
        #         splited_column_list.append(new_column_num_list)
        #         index_list.append(to_split[0])
        # new_column_list =[]
        # for i,col_i in enumerate(column_list):
        #     if to_split_list:
        #         if i in index_list:
        #             new_column_list.extend(splited_column_list[index_list.index(i)])
        #         else:
        #             new_column_list.append(col_i)
        #     else:
        #         new_column_list.append(col_i)
        # column_list = new_column_list


        """这个是按切割出来的坐标在原图上画框，方便检查"""
        for col_i in column_list:
            cv2.rectangle(src,(col_i[0],row_i[0]),(col_i[1],row_i[1]),(0,0,255),1)
    cv2.imwrite(r'.\data\new_src.png', src)

    """这个是将单个字符切割出来然后增加边距，变成一个稍大的图，供后续识别"""
    for i,sigle_i in enumerate(sigle_text_list):
        image_text = thresh_src[sigle_i[0][0]-1:sigle_i[0][1]+1,sigle_i[1][0]-1:sigle_i[1][1]+1]
        border = 10
        new_image_text = cv2.copyMakeBorder(image_text,border,border,border,border,cv2.BORDER_CONSTANT,value=(0,0,0))
        # new_image_text = cv2.resize(new_image_text,(0,0),fx=2,fy=2,interpolation=cv2.INTER_NEAREST)
        # cv2.bitwise_not(new_image_text,new_image_text)
        cv2.imwrite(r'.\data\sample\chi\single\{}_{}.png'.format(image_name,i+1000), new_image_text)
        pass



    pass

for num in range(3,78):
    print(num)
    try:
        image_path = r'.\data\sample\chi\66_sample_{}.png'.format(num)
        aa = row_column_split(image_path)
        print('-----------------')
    except:
        pass