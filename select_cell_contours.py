#coding = utf-8
import cv2
import numpy as np

class SltCellCtrs:
    def __init__(self):
        pass

    def get_cell_contours(self, bin_src_mask,offset_num=3):
        """
        [外方]获取轮廓并筛选出单元格的轮廓
        :param bin_src_mask:仅包含表格横竖线的图片
        :param offset_num: 表格线框相对于真实单元格的偏置数，默认为3
        :return:
        """
        assert isinstance(bin_src_mask,np.ndarray)
        assert isinstance(offset_num,int)
        _, contours, hierarchy = cv2.findContours(bin_src_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE,
                                                  offset=(offset_num, offset_num))
        _, contours_minus, hierarchy_minus = cv2.findContours(bin_src_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE,
                                                              offset=(-offset_num, -offset_num))
        if not contours:
            return None,None,None
        tree = hierarchy[0]
        table_tree_list = self.get_table_tree_list(contours, tree)
        if not table_tree_list:
            return None, None, None
        ignore_list = self.get_ignore_list(contours, table_tree_list)
        return contours, contours_minus, ignore_list

    def get_table_tree_list(self, contours, tree):
        """
        [秘方]获取多个表格组成的list
        :param contours: 页面全部的轮廓
        :param tree: hierarchy指代的轮廓的树状结构
        :return:
        """
        assert isinstance(contours,list) and isinstance(tree,np.ndarray)
        table_tree_list = []
        table_mark = False
        table_tree = []
        upon_contour_num = 0
        for index, contour_i in enumerate(contours):
            if (tree[index][2] == -1 and tree[index][3] == -1) or tree[index][3] is None:
                continue
            if tree[index][2] != -1 and tree[index][3] == -1:
                table_mark = True
                upon_contour_num = tree[index + 1][3]
                if table_tree:
                    table_tree_list.append(table_tree)
            if table_mark:
                table_tree = []
                table_mark = False
            if tree[index][3] in [upon_contour_num, -1]:
                table_tree.append(index)
        table_tree_list.append(table_tree)
        return table_tree_list

    def get_ignore_list(self, contours, table_tree_list):
        """
        [秘方]获取忽略列表
        :param contours: 页面全部的轮廓
        :param table_tree_list: 多个表格组成的list
        :return:
        """
        assert isinstance(contours,list) and isinstance(table_tree_list,list)
        ignore_list = []
        index_list = []
        for table_tree in table_tree_list:
            index_list.extend(table_tree[1:])
        for i in range(len(contours)):
            if i not in index_list:
                ignore_list.append(i)
        return ignore_list



