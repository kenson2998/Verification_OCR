from PIL import Image
from pytesseract import image_to_string
import pytesseract, os, requests, shutil
import cv2
import numpy as np


# 參考來源 : https://www.twblogs.net/a/5baaec092b7177781a0eaf8d/zh-cn

def save_pic(pic_url, pic_name):
    '''
    :param pic_url: 'https://xxx.xxxxx.jpg'
    :param pic_name: 'picture.jpg'
    :return pic_name
    '''
    headers = {
        'user-agent': 'Mozilla/6.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3359.181 Safari/537.36'}
    html = requests.get(pic_url, headers=headers)
    with open(pic_name, 'wb') as file:
        file.write(html.content)
    return pic_name


def OCR_Procs(picname, c_mode="L", threshold=80, driver=None, img_ele=None):
    app_path = os.path.dirname(os.path.abspath(__file__))
    '''
    :param driver: selenium 浏览器
    :param img_ele: 验证马 css ".validate-img"
    :param picname: 图片档名
    :return ocr_text: 图转文字的内容
    '''
    if driver:  # 有driver就執行class搜索img_ele 元素
        codeimage = driver.find_element_by_css_selector(img_ele)
        left = codeimage.location['x']
        top = codeimage.location['y']
        elementWidth = codeimage.location['x'] + codeimage.size['width']
        elementHeight = codeimage.location['y'] + codeimage.size['height']
        print(f"X:{elementWidth},Y:{elementHeight}")
        driver.save_screenshot(os.path.join(app_path, picname))
        driver.save_screenshot(os.path.join(app_path, picname))
        pic = Image.open(os.path.join(app_path, picname))
        pic = pic.crop((left, top, elementWidth, elementHeight))
        pic.save(os.path.join(app_path, picname))

    image = Image.open(os.path.join(app_path, picname))
    imgry = image.convert(c_mode)
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    out.save(os.path.join(app_path, picname))
    ocr_text = OCR_judge(imgry)
    return ocr_text


def OCR_judge(img):
    '''
    :param img: "pic.jpg" or image
    :return: 回传文字
    '''
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ORC_PATH = os.path.join(BASE_DIR, 'Tesseract-OCR')
    if os.path.exists(ORC_PATH) is True:
        pass
    else:
        shutil.copytree(os.path.join(BASE_DIR, 'Tesseract-OCR'), ORC_PATH)
    pytesseract.pytesseract.tesseract_cmd = ORC_PATH + r'\tesseract.exe'
    # ocr_text = image_to_string(img, config='-psm 7', lang='chi_sim') # 簡體中文
    ocr_text = image_to_string(img, config='-psm 7')
    print(f"({img})辨識結果: {ocr_text} ")
    return ocr_text


def Opencv_noise(picname, level=7):
    image = cv2.imread(picname)
    # remove_noise
    image_mid_blur = np.hstack(
        [cv2.medianBlur(image, 3), cv2.medianBlur(image, 5),
         cv2.medianBlur(image, 7)])  # 邻域越大，过滤椒盐噪声效果越好，但是图像质量也会下降明显。除非非常密集椒盐噪声，否则不推荐Ksize=7这么大的卷积核
    cv2.imwrite(picname, image_mid_blur)
    cv2.imwrite('1_noise.png', image_mid_blur)
    print('去雜訊:')
    return OCR_judge(picname)


def dev1(picname, level=7):
    img = cv2.imread(picname, 0)
    kernel = np.ones((5, 5), np.uint8)
    erosion = np.hstack([cv2.erode(img, kernel, iterations=1), cv2.dilate(img, kernel, iterations=3),
                         cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)])
    cv2.imwrite(picname, erosion)
    cv2.imwrite('1_noise.png', erosion)

    return OCR_judge(picname)


def Opencv_Gray(picname):
    image = cv2.imread(picname)
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 将输入转换为灰度图片
    cv2.imwrite(picname, img_hsv)
    cv2.imwrite('1_gray.png', img_hsv)
    print('灰色:')
    return OCR_judge(picname)


def Opencv_Black(picname):
    image = cv2.imread(picname)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    # 执行边缘检测
    edged1 = cv2.Canny(blurred, 50, 200, 255)
    cv2.imwrite(picname, edged1)
    cv2.imwrite('1_black.png', edged1)
    print('黑色:')
    return OCR_judge(picname)


def Open_pic(PIC):
    i0 = cv2.imread(PIC)
    i1 = cv2.imread('1_noise.png')
    i2 = cv2.imread('1_gray.png')
    i3 = cv2.imread('1_black.png')
    i4 = cv2.imread('handle.png')
    or0 = np.hstack([i0,i4])
    or1 = np.vstack([i1, i2, i3])
    cv2.imshow('full', or0)
    c0 = cv2.imshow('N_G_B', or1)
    cv2.waitKey(0)


if __name__ == "__main__":
    # PIC_url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png'
    # PIC_name1 = 'google.png'
    # save_pic(PIC_url, PIC_name1)  # 下载存图

    PIC_name1 = 'd01.png'
    PIC_name = 'handle.png'
    with open(PIC_name1, 'rb') as f1, open(PIC_name, 'wb') as f2:
        f2.write(f1.read())

    OCR_judge(PIC_name)  # 直接判断图片回传结果

    # 处理图片回传结果 # c_mode(1,P,L), threshold(50~200)數值會影響圖片處理
    # d01~03.png threshold用L,80  ,
    # d04~07.png threshold用L,180  ,
    OCR_Procs(picname=PIC_name, c_mode="L", threshold=80)
    # dev1(picname=PIC_name)  # 处理图片回传结果
    Opencv_noise(picname=PIC_name)  # opencv 辨识
    Opencv_Gray(picname=PIC_name)  # opencv 辨识
    Opencv_Black(picname=PIC_name)  # opencv 辨识
    Open_pic(PIC_name1)