#coding = utf-8
import cv2
import numpy as np


class TextCtrs:
    def __init__(self):
        pass

    def get_text_contours(self, contours, contours_minus, ignore_list, thresh_src, src, out_path):
        """
        [外方]根据单元格轮廓利用掩膜筛选出需要定位的文本
        :param contours:进行了正向偏置（offset>0)的contours列表
        :param contours_minus:进行了负向偏置（offset<0)的contours列表
        :param ignore_list:不是单元格的contours的index列表
        :param thresh_src:二值化的图片
        :param src:原始图片
        :param out_path:输出路径
        :return:
        """
        assert isinstance(contours,list) and isinstance(contours_minus,list)
        assert isinstance(ignore_list,list) and isinstance(thresh_src,np.ndarray)
        assert isinstance(src,np.ndarray) and isinstance(out_path,str)
        text_contours = []
        for i, contour_i in enumerate(contours):
            if i in ignore_list:
                continue
            image_ofs = self.get_empty_img(thresh_src)
            image_ofs_minus = self.get_empty_img(thresh_src)
            image_mask = self.get_empty_img(thresh_src)
            cv2.drawContours(image_ofs, [contours[i]], 0, 255, cv2.FILLED)
            cv2.drawContours(image_ofs_minus, [contours_minus[i]], 0, 255, cv2.FILLED)
            cv2.bitwise_and(image_ofs, image_ofs_minus, image_mask)
            cv2.imwrite(r'..\data\image_mask.png', image_mask)
            image = cv2.add(thresh_src, self.get_empty_img(thresh_src), mask=image_mask)
            cv2.imwrite(r'..\data\test.png',image)
            # self.one_text_contour(image, out_path, src, text_contours,i)#分割src(原图）
            self.one_text_contour(image, out_path, thresh_src, text_contours, i)#分割thresh_src(二值图）
        return text_contours

    def one_text_contour(self, image, out_path, src, text_contours,i):
        """
        [秘方]获取某个text文本的contour
        :param image:仅包含本次text文本的图片
        :param out_path:文本待输出地址
        :param src:待画框的图片（包含所有的text文本）
        :param text_contours:所有text_contours的列表
        :return:
        """
        assert isinstance(image,np.ndarray) and isinstance(out_path,str)
        assert isinstance(src,np.ndarray) and isinstance(text_contours,list)
        col_end, col_start = self.get_start_end_num(image, axis=0, offset=3)
        row_end, row_start = self.get_start_end_num(image, axis=1, offset=3)
        text_img = self.get_empty_img(src)
        if row_start:
            text_img[row_start:row_end, col_start:col_end] = 255
        _, contours_text, hierarchy = cv2.findContours(text_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if contours_text:
            x,y,w,h = cv2.boundingRect(contours_text[0])
            image_text = src[y - 1:y + h + 1, x - 1:x + w + 1]
            image_path = r'..\data\sample\{}_sample_{}.png'.format(66,i)
            # cv2.bitwise_not(image_text, image_text)
            image_text = cv2.resize(image_text,(0,0),fx=4,fy=4)
            cv2.imwrite(image_path, image_text)
            # try:
            #     for i in range(2,11):
            #         image_text = src[y-i:y+h+i,x-i:x+w+i]
            #         image_path = r'..\data\image_text.png'
            #         cv2.imwrite(image_path, image_text)
            #         # words_result = albb_ocr(image_path)
            #         words_result = bd_ocr(image_path)
            #         print(words_result)
            #     print('-------------------------------')
            # except:
            #     pass

        if contours_text:
            cv2.drawContours(src, contours_text[0], -1, (0, 0, 255), 1)
            text_contours.extend(contours_text)
            cv2.imwrite(out_path, src)

    def get_start_end_num(self, image,axis,offset):
        """
        [秘方]获取image的text文本在矩阵中的起始、结束编号（已进行了偏置）
        :param image: 带获取的图像矩阵
        :param axis: 方向，0为获取列，1为获取行
        :param offset: 偏置量，即后面的框与文本最外围的距离
        :return:
        """
        assert isinstance(image,np.ndarray) and isinstance(axis,int)
        assert isinstance(offset,int)
        start = None
        end = None
        range_sum = image.sum(axis=axis)#获取按某个方向的分组求和
        for i, col_i in enumerate(range_sum):
            if col_i != 0:
                start = i
                break
        for i, col_i in enumerate(range_sum):
            if col_i != 0:
                end = i
        if start:
            start = start - offset
            end = end + offset
        return end, start

    def get_empty_img(self,thresh_src):
        """
        [秘方]获取二值化的空img
        :param thresh_src: 空Img的shape来源图片
        :return:
        """
        assert isinstance(thresh_src,np.ndarray)
        return np.zeros((thresh_src.shape[0], thresh_src.shape[1]), dtype=np.uint8)