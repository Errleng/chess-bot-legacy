import pyautogui
from PIL import Image
from PIL import ImageGrab
import time
import requests
import numpy as np

get1 = requests.get("https://echecservice.000webhostapp.com/color.txt")
read1 = get1.text
SAVE_PATH = "D:/Screenshots/"
img = Image.open(SAVE_PATH + "chessScreenshot.jpg")
x = None

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


if read1 == "WHITE":
    print("Player is: " + read1)
    x = 0
elif read1 == "BLACK":
    print("Player is: " +  read1)
    x = 1

print("BEGIN")
while True:
    get1 = requests.get("https://echecservice.000webhostapp.com/color.txt")
    read1 = get1.text
    time.sleep(2)
    if read1 == 'WHITE':
        if x == 0:

            print("START WHITE SEQUENCE")
            ImageGrab.grab().save(SAVE_PATH + "chessScreenshot.jpg", "JPEG")
            print("SAVED SCREENSHOT")
            img = Image.open(SAVE_PATH + "chessScreenshot.jpg")
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
            time.sleep(1)
        else:
            print("OPPONENT IS " + read1)
            time.sleep(3)


    if read1 == 'BLACK':
        if x == 1:
            print("START BLACK SEQUENCE")
            ImageGrab.grab().save(SAVE_PATH + "chessScreenshot.jpg", "JPEG")
            print("SAVED SCREENSHOT")
            img = Image.open(SAVE_PATH + "chessScreenshot.jpg")
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
            time.sleep(1)



