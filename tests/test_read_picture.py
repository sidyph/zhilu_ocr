#coding = utf-8
from read_picture import ReadTable
from select_cell_contours import SltCellCtrs
from text_contours import TextCtrs
import time


def test_read_picture():
    read_table = ReadTable()
    slt_cell_ctrs = SltCellCtrs()
    text_ctrs = TextCtrs()
    for i in range(61,67):
        print(i)
        file_id = '1020120170816968567'
        img_path = r'..\data\images\{}\images_{}.png'.format(file_id,i)
        out_path = r'..\data\images\{}\out\out_{}.png'.format(file_id,i)
        thresh_src, clean_src, src = read_table.thres_img(img_path,max_threshold=233,text_threshold=200,dnmt_hor=50,dnmt_ver=50,is_noise_point=False)
        slt_cell_ctrs.get_cell_contours(clean_src)
        contours, contours_minus, ignore_list = slt_cell_ctrs.get_cell_contours(clean_src)
        if contours:
            text_contours = text_ctrs.get_text_contours(contours, contours_minus, ignore_list, thresh_src, src, out_path)
        pass

