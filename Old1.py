import urllib.request
import requests
import win32api, win32con
import time
import pyautogui
import random
import win32gui
from PIL import Image
from PIL import ImageGrab
import math
import numpy as np
import cv2

x = 0
playSpeed = random.uniform(0, 0)

# playerColor = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), 1050, 925)
#
# pyautogui.moveTo(1050,925)
#
# print("PLAYER COLOR IS:",playerColor)
#
# if playerColor == 0:
#     print("PLAYER IS BLACK")
#     x = 1
# elif playerColor == 16777215:
#     print("PLAYER IS WHITE")
#     x = 0
#
# playerColor = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), 1050, 850)
# print("PLAYER COLOR IS:",playerColor)

# if playerColor == 5461079:
#     print("PLAYER IS BLACK")
#     x = 1
# elif playerColor == 5936501:
#     print("PLAYER IS WHITE")
#     x = 0

get1 = requests.get("https://echecservice.000webhostapp.com/color.txt",  headers={'User-Agent':'test'})
read1 = get1.text

if read1 == "WHITE":
    print("Player is: " + read1)
    x = 0
elif read1 == "BLACK":
    print("Player is: " +  read1)
    x = 1

# flick1 = False;
# while flick1 == True:
#     time.sleep(playSpeed)
#     # get1 = urllib.request.urlopen("https://echecservice.000webhostapp.com/file.txt")
#     # get2 = urllib.request.urlopen("https://echecservice.000webhostapp.com/color.txt")
#
#     # Suggested to use requests library to avoid server disconnecting us
#
#     get1 = requests.get("https://echecservice.000webhostapp.com/file.txt")
#     get2 = requests.get("https://echecservice.000webhostapp.com/color.txt")
#
#     # read1 = get1.readlines().decode()
#     # read2 = get2.readlines().decode()
#
#     read1 = get1.text
#     read2 = get2.text
#
#     if read1 != None:
#         print("CURRENT COLOR " + read2)
#         if x == 0:
#             if read2 == "WHITE":
#                 print(read1)
#                 coordinates = read1.split(' ')
#                 print(coordinates)
#                 click(coordinates[0], coordinates[1] + 100)
#                 print("CLICK ONE", coordinates[0], coordinates[1])
#                 time.sleep(1)
#                 clickoff(coordinates[2], coordinates[3] + 100)
#                 print("CLICK TWO", coordinates[2], coordinates[3])
#
#         if x == 1:
#             if read2 == "BLACK":
#                 print(read1)
#                 coordinates = read1.split(' ')
#                 print(coordinates)
#                 click(coordinates[0], coordinates[1] + 100)
#                 print("CLICK ONE", coordinates[0], coordinates[1])
#                 time.sleep(1)
#                 clickoff(coordinates[2], coordinates[3] + 100)
#                 print("CLICK TWO", coordinates[2], coordinates[3])

prevColor = str
prevCoords = None
while True:

    get2 = requests.get("https://echecservice.000webhostapp.com/color.txt",  headers={'User-Agent':'test'})

    read2 = get2.text

    get1 = requests.get("https://echecservice.000webhostapp.com/file.txt", headers={'User-Agent': 'test'})
    read1 = get1.text
    if prevCoords != read1:
        prevCoords = read1
        print(read1)
        coordinates = read1.split(' ')
        print(coordinates)
        print("CURRENT COLOR " + read2)
        if x == 0:
            if read2 == "WHITE":
                get1 = requests.get("https://echecservice.000webhostapp.com/file.txt", headers={'User-Agent':'test'})
                read1 = get1.text
                if prevCoords != read1:
                    prevCoords = read1
                    print(read1)
                    coordinates = read1.split(' ')
                    print(coordinates)
                    try:
                        coordX = round(float(coordinates[0]))
                        coordY = round(float(coordinates[1])) + 100
                        GreenCoordX = round(float(coordinates[2]))
                        GreenCoordY = round(float(coordinates[3])) + 100
                        pyautogui.moveTo(GreenCoordX, GreenCoordY)
                        pyautogui.mouseDown()
                        print("CLICK ONE", GreenCoordX, GreenCoordY)
                        time.sleep(0.5)
                        pyautogui.moveTo(coordX, coordY)
                        pyautogui.mouseUp()
                        print("CLICK TWO", coordX, coordY)
                        time.sleep(1)
                    except:
                        pass

        if x == 1:
            if read2 == "BLACK":
                try:
                    coordX = round(float(coordinates[0]))
                    coordY = round(float(coordinates[1])) + 100
                    GreenCoordX = round(float(coordinates[2]))
                    GreenCoordY = round(float(coordinates[3])) + 100
                    pyautogui.moveTo(GreenCoordX, GreenCoordY)
                    pyautogui.mouseDown()
                    print("CLICK ONE", GreenCoordX, GreenCoordY)
                    time.sleep(0.5)
                    pyautogui.moveTo(coordX, coordY)
                    pyautogui.mouseUp()
                    print("CLICK TWO", coordX, coordY)
                    time.sleep(1)
                except:
                    pass




