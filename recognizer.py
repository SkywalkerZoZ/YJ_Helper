import cv2
import numpy as np
import pytesseract
import os
import pyautogui

def get_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot


def recognize_cards(screenshot):
    chars=[]
    # 将屏幕截图转换为OpenCV格式并转换为灰度图像
    screenshot_cv = np.array(screenshot)
    screenshot_cv_gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2GRAY)

    # 加载模板图像并转换为灰度图像
    template = cv2.imread("./img/template.png", cv2.IMREAD_GRAYSCALE)

    # 执行模板匹配
    result = cv2.matchTemplate(screenshot_cv_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 获取最佳匹配的位置
    top_left = (max_loc[0],max_loc[1]+48)
    wide=840
    height=21
    bottom_right = (top_left[0] + wide, top_left[1] + height)


    # 截取窗口区域
    card_region = screenshot_cv[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]


    # TODO debug
    # cv2.imwrite("card_region.png", card_region)

    # output_folder="./cards"
    # os.makedirs(output_folder, exist_ok=True)


    # 将彩色图片转为灰度图
    gray = cv2.cvtColor(card_region, cv2.COLOR_BGR2GRAY)

    # 使用自适应阈值来将图片二值化
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 使用形态学操作来消除噪点
    kernel = np.ones((4, 4), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    # 寻找轮廓
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历轮廓，将每个竖线保存为一个卡片
    min_line_length = 18  # 最小竖线长度
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if h > min_line_length and w > 12:
            number = card_region[y:y+h, x+3:x+19]
            number_gray=cv2.cvtColor(number, cv2.COLOR_BGR2GRAY)

            # 降噪
            number_gray = cv2.GaussianBlur(number_gray, (1,1), 0)

            # 形态学操作
            kernel = np.ones((1,1), np.uint8)
            number_gray = cv2.erode(number_gray, kernel, iterations=1)

            # 增加对比度
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(1,1))
            number_gray = clahe.apply(number_gray)

            custom_config = r'--psm 7 -c tessedit_char_whitelist=2345678910JQKA'
            text = pytesseract.image_to_string(number_gray, config=custom_config)
            #TODO debug
            # cv2.imwrite(f'cards/card_{i}.png', number_gray)

            text = text.replace(' ', '').replace('\n', '')
            if(text=="0"):
                text="Q"
            if(text in [ '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K','A']):
                chars=[text]+chars
                # print(text)
    # print(chars)
    return chars


def char2number(char_list,number_list):
    char_to_number = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
                      '10': 10, '11':11,'12':12,'13':13,
                      'J': 11, 'Q': 12, 'K': 13, 'A': 1,
                      'j': 11,'q': 12,'k': 13,'a': 1}

    for char in char_list:
        number_list.append(char_to_number[char])
    return number_list


if __name__ =='__main__':
    screenshot = cv2.imread("./img/7.jpg")
    recognize_cards(screenshot)





