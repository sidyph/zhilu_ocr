#读取图片，初步处理，二值化
#获取表格线
#获取轮廓并筛选出单元格的轮廓
#根据单元格轮廓利用掩膜筛选出需要定位的文本
#定位文本并框选出来

#coding = utf-8
import cv2
import numpy as np

class ReadTable:
    kernel_rect_3_3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self):
        pass

    def thres_img(self,img_path,max_threshold = 232,text_threshold = 190,close_num = 1,dnmt_hor=50,dnmt_ver=50,is_noise_point = False):
        """
        [外方]将src单阈值二值化，筛去色块，获得纯粹黑色线条，并做反向操作，获得黑底白线，供后续使用
        :param img_path: 输入的图像地址
        :param max_threshold: 二值化，获取表格线框时的最大阈值
        :param text_threshold: 二值化，获取表格全部内容的时候的阈值
        :param close_num: 开闭操作的次数
        :return:
        """
        assert isinstance(img_path,str) and isinstance(max_threshold,int)
        assert isinstance(text_threshold,int) and isinstance(close_num,int)
        src = cv2.imread(img_path)
        # gray_src = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
        gray_src = self.remove_red(src)
        cv2.imwrite(r'..\data\gray_src.png', gray_src)
        _, thresh_src = cv2.threshold(gray_src, max_threshold, 255, cv2.THRESH_BINARY)
        cv2.bitwise_not(thresh_src, thresh_src)  # 取反
        cv2.imwrite(r'..\data\thresh_src1.png', thresh_src)
        thresh_src2 = self.get_lines(thresh_src, dnmt_hor,dnmt_ver)
        cv2.imwrite(r'..\data\thresh_src2.png', thresh_src2)
        clean_src = cv2.morphologyEx(thresh_src2, cv2.MORPH_CLOSE, self.kernel_rect_3_3, None, None, close_num)
        _, thresh_src = cv2.threshold(gray_src, text_threshold, 255, cv2.THRESH_BINARY)
        cv2.bitwise_not(thresh_src, thresh_src)  # 取反
        cv2.imwrite(r'..\data\thresh_src.png',thresh_src)
        if is_noise_point:
            kerner1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
            src1 =cv2.morphologyEx(thresh_src,cv2.MORPH_OPEN,kerner1,None,None,1)
            kerner2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
            src2 = cv2.morphologyEx(thresh_src, cv2.MORPH_OPEN, kerner2, None, None, 1)
            cv2.bitwise_or(src1,src2,thresh_src)
        return thresh_src,clean_src,src

    def remove_red(self, src):
        """
        移除红色印章，并转为灰度图
        :param src: 原始图片
        :return:
        """
        assert isinstance(src,np.ndarray)
        # 利用hsv方法将红色部分提取出来
        hsv_src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
        lower_red = np.array([140, 25, 0])#红色部分的参数区间，包含两部分
        upper_red = np.array([180, 255, 255])
        mask = cv2.inRange(hsv_src, lower_red, upper_red)
        lower_red1 = np.array([0, 25, 0])
        upper_red1 = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv_src, lower_red1, upper_red1)
        mask_all = mask + mask1
        res = cv2.bitwise_and(src, src, mask=mask_all)
        gray_red = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(r'..\data\gray_red.png', gray_red)

        #将原图的红色部分设置为白色
        gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        rows, cols = gray_red.shape
        for i in range(rows):
            for j in range(cols):
                value = gray_red[i, j]
                if value != 0:
                    gray_src[i, j] = 255
        cv2.imwrite(r'..\data\gray_src2.png', gray_src)

        #通道分离，仅对红色通道进行阈值处理
        b_channel, g_channel, r_channel = cv2.split(src)
        _, thresh_src1 = cv2.threshold(r_channel, 200, 255, cv2.THRESH_BINARY)
        cv2.imwrite(r'..\data\thresh_src11.png', thresh_src1)

        #将上面得到的阈值处理后的图片增添到灰度图中.
        for i in range(rows):
            for j in range(cols):
                value = thresh_src1[i, j]
                value_gray = gray_src[i,j]
                if value == 0 and value_gray !=0:#当二值化图thresh_src1中为黑色,灰度图中对应位置不为黑色时，将gray_src对应的位置也改成黑色
                    gray_src[i, j] = 0
        cv2.imwrite(r'..\data\gray_src3.png', gray_src)
        return gray_src

    def get_lines(self,thresh_src,dnmt_hor,dnmt_ver):
        """
        [秘方]获取表格线
        :param thresh_src:
        :return:
        """
        assert isinstance(thresh_src,np.ndarray)
        #获取水平线
        shape_hor = int(thresh_src.shape[0] / dnmt_hor)
        if shape_hor == 0:
            shape_hor = 1
        kernel_hor = cv2.getStructuringElement(cv2.MORPH_RECT, (shape_hor, 1))  # 获取n*1的矩形结构元素
        bin_src_hor = cv2.morphologyEx(thresh_src, cv2.MORPH_OPEN, kernel_hor, None, None, 1)  # 做一次开操作，先腐蚀后膨胀，一次
        bin_src_hor = cv2.morphologyEx(bin_src_hor, cv2.MORPH_DILATE, kernel_hor, None, None, 1) #继续膨胀，延伸线条

        #获取垂直线
        shape_ver = int(thresh_src.shape[0] / dnmt_ver)
        if shape_ver == 0:
            shape_ver = 1
        kernel_ver = cv2.getStructuringElement(cv2.MORPH_RECT, (1, shape_ver))  # 获取1*n的矩形结构元素
        bin_src_ver = cv2.morphologyEx(thresh_src, cv2.MORPH_OPEN, kernel_ver, None, None, 1)  # 做一次开操作，先腐蚀后膨胀，一次
        bin_src_ver = cv2.morphologyEx(bin_src_ver, cv2.MORPH_DILATE, kernel_ver, None, None, 1) #继续膨胀，延伸线条

        #水平线垂直线合并
        bin_src_mask = bin_src_hor + bin_src_ver  # 水平线和垂直线或操作，都显示在图像里

        #用正方的kernel消除一些局部坑洞
        bin_src_mask = cv2.morphologyEx(bin_src_mask, cv2.MORPH_CLOSE, self.kernel_rect_3_3, None, None, 1)  # 做一次闭操作，先膨胀后腐蚀，一次
        return bin_src_mask














