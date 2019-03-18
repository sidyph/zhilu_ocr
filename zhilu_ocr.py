from PIL import Image
import pytesseract


#打开图片
image_path = r'.\data\sample\num\single\1011.png'
# for i in range(1,23):
# image_path = r'.\data\sample\test5\{}.png'.format(15)

# image = Image.open(image_path)
# #加载一下图片防止报错，此处可以省略
# image.load()
# #调用show来展示图片，调试用此处可以省略
# image.show()
# text = pytesseract.image_to_string(Image.open(image_path), lang='yhj',config='--psm 10 digits')
# print(text)


"""读取yhj的traineddata库来识别字符，参数说明：
    --psm 10 :按单字符识别
    --psm 7 :按行识别
    -c tessedit_char_whitelist="0123456789"：表示强制设置识别白名单为数字
    lang:表示本次识别采用的识别库
"""
def yhj_ocr(image_path):
    text = pytesseract.image_to_string(Image.open(image_path),lang='yhj',config='--psm 10 -c tessedit_char_whitelist="0123456789"')
    print(text)

"""利用tesseract识别图片"""
import os
dir_name = r'.\data\sample\chi\single'
for a,b,c in os.walk(dir_name):
    res_list = c
for res_i in res_list:
    image_path = dir_name+ '\\' + res_i
    print(image_path)
    yhj_ocr(image_path)
    print('------------------')