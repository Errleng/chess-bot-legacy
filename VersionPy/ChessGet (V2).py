import numpy as np
from PIL import Image
from PIL import ImageGrab
import pyautogui
import win32gui
import time
import random
import requests

x = 0
playSpeed = random.randint(1, 2)


SAVE_PATH = "D:/Screenshots/"

ImageGrab.grab().save(SAVE_PATH + "chessShotted.jpg", "JPEG")
print("SAVED SCREENSHOT")
# def find_rgb(imagename , r_q, g_q, b_q):

img = Image.open(SAVE_PATH + "chessShotted.jpg")

# try:
#     while True:
#         mousePos = win32gui.GetCursorPos()
#         print(mousePos)
#         RGBint = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), mousePos[0], mousePos[1])
#         rgb_im = img.convert('RGB')
#         r, g, b = rgb_im.getpixel(mousePos)
#         print(r, g, b)
#         time.sleep(0.5)
#
# except:
#     pass

def find_rgb(imagename, r_q, g_q, b_q):
    channels = 3
    width = 1920
    height = 1080
    imgnp = np.array(img)
    # print(imgnp)
    r = 0
    g = 1
    b = 2
    # print("SPINNING...")
    # result = np.where((imgnp[:, :, r] == r_q) & (imgnp[:, :, g] == g_q) & (imgnp[:, :, b] == b_q))
    result = (np.where((imgnp[:, :, r] == r_q) & (imgnp[:, :, g] == g_q) & (imgnp[:, :, b] == b_q)))
    # print(result)
    if result[0].size != 0 and result[1].size != 0:
        for arrays in result:
            # print("ARRAYS")
            # print(arrays)
            argon = np.dstack(arrays)
            # print("NOBLE")
            a = result[0]
            # print("A", a)
            b = result[1]
            # print("B:", b)
            noble = (np.array(list(zip(a.ravel(), b.ravel())), dtype=('i4,i4')).reshape(a.shape))
            # print(noble)
            # print(noble[0])
            # for single in noble:
            #     print(single)
            #     pyautogui.moveTo(single[0], single[1])
            return noble

    else:
        print("NONE")
        return None

# channels = 3
# width = 1920
# height = 1080
# imgnp = np.array(img)
# # print(imgnp)
# r = 0
# g = 1
# b = 2
# r_q = 181
# g_q = 240
# b_q = 134
# print("SPINNING...")
# # result = np.where((imgnp[:, :, r] == r_q) & (imgnp[:, :, g] == g_q) & (imgnp[:, :, b] == b_q))
# result = (np.where((imgnp[:, :, r] == r_q) & (imgnp[:, :, g] == g_q) & (imgnp[:, :, b] == b_q)))
# print(result)
# print(result[0])
'''
TEST = find_rgb(img, 179, 239, 105)
print("TEST TEST")
print(TEST)
print(TEST[0], TEST[1])
for single in TEST:
    mousePos = win32gui.GetCursorPos()
    print(single[0], single[1])
    pyautogui.moveTo(single[0], single[1])
    RGBint = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), mousePos[0], mousePos[1])
    rgb_im = img.convert('RGB')
    r, g, b = rgb_im.getpixel(mousePos)
    print(r, g, b)
    time.sleep(0.5)
'''
get2 = requests.get("https://echecservice.000webhostapp.com/color.txt")
read2 = get2.text
x = None
if read2 == 'WHITE':
    x = 0
    print("PLAYER IS WHITE")
if read2 == 'BLACK':
    x = 1
    print("PLAYER IS BLACK")

flick1 = True
while flick1 == True:
    get2 = requests.get("https://echecservice.000webhostapp.com/color.txt")
    read2 = get2.text

    if read2 == "WHITE":
        if x == 0:
            print("WHITE SEQUENCE START")
            # time.sleep(playSpeed)
            ImageGrab.grab().save(SAVE_PATH + "chessShotted.jpg", "JPEG")
            img = Image.open(SAVE_PATH + "chessShotted.jpg")
            print("SCREENSHOTTED")
            pinkzip = find_rgb(img, 238, 158, 147)
            redzip = find_rgb(img, 160, 99, 117)
            dgzip = find_rgb(img, 102, 180, 104)
            lgzip = find_rgb(img, 181, 240, 134)

            FIRST = None
            SECOND = None

            if pinkzip is None and redzip is not None:
                FIRSTX = redzip[0][0]
                FIRSTY = redzip[0][1]
                print("RED")
                # print(redzip)
                # time.sleep(1)
            elif redzip is None and pinkzip is not None:
                FIRSTX = pinkzip[0][0]
                FIRSTY = pinkzip[0][1]
                print("PINK")
                # print(pinkzip)
                # time.sleep(1)
            if dgzip is None and lgzip is not None:
                SECONDX = lgzip[0][0]
                SECONDY = lgzip[0][1]
                print("LG")
                # print(lgzip)
                # time.sleep(1)
            elif lgzip is None and dgzip is not None:
                SECONDX = dgzip[0][0]
                SECONDY = dgzip[0][1]
                print("DG")
                # print(dgzip)
                # time.sleep(1)

            print("FIRSTS", FIRSTX, FIRSTY)
            print("SECONDS", SECONDX, SECONDY)

            print("FIRST:", FIRST)
            print("SECOND", SECOND)

            pyautogui.moveTo(SECONDY, SECONDX)

            pyautogui.mouseDown()
            print("ONE")
            time.sleep(0.5)
            pyautogui.moveTo(FIRSTY, FIRSTX)
            pyautogui.mouseUp()
            print("TWO")
            time.sleep(playSpeed)
        else:
            print("OPPONENT IS PLAYING:", read2)
            # time.sleep(5)

    if read2 == "BLACK":
        if x == 1:
            print("BLACK SEQUENCE START")
            # time.sleep(playSpeed)
            ImageGrab.grab().save(SAVE_PATH + "chessShotted.jpg", "JPEG")
            img = Image.open(SAVE_PATH + "chessShotted.jpg")
            print("SCREENSHOTTED")
            pinkzip = find_rgb(img, 238, 158, 147)
            redzip = find_rgb(img, 160, 99, 117)
            dgzip = find_rgb(img, 102, 180, 104)
            lgzip = find_rgb(img, 181, 240, 134)

            FIRST = None
            SECOND = None

            if pinkzip is None and redzip is not None:
                FIRSTX = redzip[0][0]
                FIRSTY = redzip[0][1]
                print("RED")
                # print(redzip)
                # time.sleep(1)
            elif redzip is None and pinkzip is not None:
                FIRSTX = pinkzip[0][0]
                FIRSTY = pinkzip[0][1]
                print("PINK")
                # print(pinkzip)
                # time.sleep(1)
            if dgzip is None and lgzip is not None:
                SECONDX = lgzip[0][0]
                SECONDY = lgzip[0][1]
                print("LG")
                # print(lgzip)
                # time.sleep(1)
            elif lgzip is None and dgzip is not None:
                SECONDX = dgzip[0][0]
                SECONDY = dgzip[0][1]
                print("DG")
                # print(dgzip)
                # time.sleep(1)

            print("FIRSTS", FIRSTX, FIRSTY)
            print("SECONDS", SECONDX, SECONDY)

            print("FIRST:", FIRST)
            print("SECOND", SECOND)

            pyautogui.moveTo(SECONDY, SECONDX)

            pyautogui.mouseDown()
            print("ONE")
            time.sleep(0.5)
            pyautogui.moveTo(FIRSTY, FIRSTX)
            pyautogui.mouseUp()
            print("TWO")
            time.sleep(playSpeed)
        else:
            print("OPPONENT IS PLAYING", read2)
            # time.sleep(5)

# for results in result:
#     print("RESULTS")
#     print(results)

# resultList = list()

# for result in imgnp:
#     for single in result:
#         if tuple(single) == (r_q, g_q, b_q):
#             print("APPENDED")
#             resultList.append(single)
#
# print("TEST CASE")
# print(resultList)



