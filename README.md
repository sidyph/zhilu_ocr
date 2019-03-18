# zhilu_ocr

# 代码结构

读取本地表格图片，将其按单元格拆解开来

read_picture 外层执行函数，将图片读取并执行拆解全过程

select_cell_conrours 内层函数，将各单元格的轮廓一一框选出来

text_contours 内层函数，将单元格中的文本内容框选出来，并切割存入本地

split_text 将文本切割成单字符

zhilu_ocr 使用训练所得的字库（如命名为yhj的字库），用来识别待识别文字

test_read_picture 输入参数执行read_picture函数

# ocr识别教程

参见该链接内容：https://www.jianshu.com/p/8b4d789f234c

