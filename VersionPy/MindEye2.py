import win32api, win32con
import time
import os
import random
import win32gui
from PIL import Image
from PIL import ImageGrab
import math
import numpy as np
import cv2
import chess
import chess.uci
import glob
import image_slicer
import imutils

# SAVE_PATH = "C:/Users/aisae/Desktop/TRUTH/Screenshots/"
SAVE_PATH = "C:/Users/aisae/Documents/Sourcetree/ChessBot/Screenshots/"
# ImageGrab.grab().save(SAVE_PATH + "ChessShot.jpg", "JPEG")
# print("SAVED SCREENSHOT")

img = Image.open(SAVE_PATH + "ChessShot.jpg")

def rgbTemplateMatch(templatePath, img):
    global max_Val

    temp = cv2.imread(templatePath)

    # cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    # cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # cv2.imshow("grayImg", img)
    # cv2.waitKey(0)
    # cv2.imshow("grayTemp", temp)
    # cv2.waitKey(0)

    res = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF_NORMED)

    _, max_Val, _, _ = cv2.minMaxLoc(res)

    return max_Val

def rgbImgTM(imagePath, templatePath):
    global maximum_Val
    img = imagePath
    # img = imagePath
    temp = cv2.imread(templatePath)

    # temp = templatePath
    # w, h = temp.shape[:-1]

    # print('Width', w, 'Height', h)

    res = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF_NORMED)
    # print(cv2.minMaxLoc(res))
    min_val, maximum_Val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(maximum_Val)

    # top_left = max_loc
    # bottom_right = (top_left[0] + w, top_left[1] + h)

    # cv2.rectangle(img, top_left, bottom_right, 255, 2)
    return maximum_Val
    # cv2.imshow('read', img)
    # cv2.waitKey(0)

def templateMatch(template, img):
    global max_val
    # img_rgb = cv2.imread(SAVE_PATH + "ChessShot.jpg")
    # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # img_rgb = cv2.imread(img)
    img_rgb = img
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_edge = cv2.Canny(img_gray, 50, 200)
    templater = cv2.imread(template, 0)
    template_edge = cv2.Canny(templater, 50, 200)
    # cv2.imshow('template', template_edge)
    # cv2.waitKey(0)
    w, h = templater.shape[:2]

    res = cv2.matchTemplate(img_edge,template_edge,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    # loc = np.where( res >= threshold)
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    # cv2.imshow('res.png',img_rgb)
    # cv2.waitKey(0)
    return img_rgb, max_val

def IsInt(str):
    global intLet
    intLet = 0
    try:
        int(str)
        # print(str + ' is Int')
        return True
    except:
        # print(str + ' is not Int')
        return False

boardHeight = 504
pieceHeight = 504/8
pieceWidth = 504/8

templateList = []
for file in os.listdir(SAVE_PATH + "AllPieces"):
    filename = os.fsdecode(file)
    if filename.endswith(".png"):
        templateList.append(filename)

enginePath = 'C:\\Users\\aisae\\Desktop\\Hold\\Engines\\'

# engine = chess.uci.popen_engine(enginePath + 'stockfish-8-win/Windows/stockfish_8_x64.exe')
# engine = chess.uci.popen_engine(enginePath + 'Rybkav2.3.2a.mp.x64.exe')
# engine = chess.uci.popen_engine(enginePath + 'Spike/Spike1.4.exe')
engine = chess.uci.popen_engine(enginePath + 'naum.exe')

print('Engine opened')

engine.uci()
print('UCI loaded')
print(engine.name, 'Loaded')

player = input('Input 0 for white or 1 for black\n')

engine.setoption({'MultiPV': 3})

print("Initiated")

widthArray = [1, 2, 3, 4, 5, 6, 7, 8]
lengthArray = widthArray

#Offset for resize 126 : 25
#Suggest changing 660 to 685 for higher consistency
#Old value was (157, 156, 685, 660)
box = (157, 156,  685, 660)

crop_img = np.array(ImageGrab.grab(bbox = box))
resized_crop_img = imutils.resize(crop_img, width = 126)
boardDim = resized_crop_img.shape[0]
pieceDim = resized_crop_img.shape[0]/8

canCastleQueenWhite = True
canCastleKingWhite = True

canCastleQueenBlack = True
canCastleKingBlack = True

movecount = int(input("Enter movecount\n"))
fastMode = int(input("Enter 0 or 1 accurate or fast\n"))
difficulty = int(input("Enter 0 to 1 difficulty\n"))

noChangePosition = 0

def clickDown(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)

def clickUp(x,y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)



try:
    while True:

        startTime = time.time()
        # ImageGrab.grab(bbox=(535, 105, 600, 140)).save(SAVE_PATH + 'croppedBlack.jpg')
        # ImageGrab.grab(bbox=(535, 670, 600, 710)).save(SAVE_PATH + 'croppedWhite.jpg')
        cropped_color_black = np.array(ImageGrab.grab(bbox = (535, 105, 600, 140)))
        # cropped_color_black = cv2.imread(SAVE_PATH + 'croppedBlack.jpg')
        # cv2.imshow('Cropped', cropped_color_black)
        # cv2.waitKey(0)
        cropped_color_white = np.array(ImageGrab.grab(bbox = (535, 670, 600, 710)))
        # cropped_color_white = cv2.imread(SAVE_PATH + 'croppedWhite.jpg')
        # cv2.imshow('Cropped', cropped_color_white)
        # cv2.waitKey(0)

        resized_crop_black = imutils.resize(cropped_color_black, width=27)
        # cv2.imshow('Resized Cropped Black', resized_crop_black)
        # cv2.waitKey(0)
        # Image.fromarray(resized_crop_black, 'RGB').save(SAVE_PATH + 'croppedBlack.jpg')

        resized_crop_white = imutils.resize(cropped_color_white, width=27)
        # cv2.imshow('Resized Cropped White', resized_crop_white)
        # cv2.waitKey(0)
        # Image.fromarray(resized_crop_white, 'RGB').save(SAVE_PATH + 'croppedWhite.jpg')

        returnBlack = rgbImgTM(resized_crop_black, SAVE_PATH + 'BlackTimer.jpg')
        returnWhite = rgbImgTM(resized_crop_white, SAVE_PATH + 'WhiteTimer.jpg')

        # print("Time before color match", time.time() - startTime)
        # returnBlack = rgbImgTM(SAVE_PATH + 'croppedBlack.jpg', SAVE_PATH + 'BlackTimer.jpg')
        # returnWhite = rgbImgTM(SAVE_PATH + 'croppedWhite.jpg', SAVE_PATH + 'WhiteTimer.jpg')
        # print("Time after color match", time.time() - startTime)

        toMove = ''

        if returnBlack > returnWhite:
            if returnBlack < 0.9:
                toMove = 'w'
                # print("Detected RED timer for WHITE")
            else:
                # print("Black to Move with", round(returnBlack * 100, 2), "% confidence")
                toMove = 'b'
        elif returnWhite > returnBlack:
            if returnWhite < 0.9:
                toMove = 'b'
                # print("Detected RED timer for BLACK")
            else:
                # print("White to Move with", round(returnWhite * 100, 2), "% confidence")
                toMove = 'w'
        else:
            toMove = 'w'

        if toMove == 'b' and player == '0':
            noChangePosition = 0
            continue
        if toMove == 'w' and player == '1':
            noChangePosition = 0
            continue

        noChangePosition += 1
        if noChangePosition >= 5:
            print("NO CHANGE IN POSITION")
            break

        time.sleep(0.1)

        # print("Time before Slice", time.time() - startTime)

        crop_img = np.array(ImageGrab.grab(bbox = box), dtype = np.uint8)
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        resized_crop_img = imutils.resize(crop_img, width = 126)

        # cv2.imshow('image', resized_crop_img)
        # cv2.waitKey(0)

        # Image.fromarray(resized_crop_img, 'RGB').save(SAVE_PATH + 'croppedBoard.png')
        # cv2.imshow('Cropped', crop_img)
        # cv2.waitKey(0)
        # tiles = image_slicer.slice(SAVE_PATH + 'croppedBoard.png', 64, save=False)
        # image_slicer.save_tiles(tiles, directory=SAVE_PATH + 'Slices')

        # print("Time after Slice", time.time() - startTime)

        global max_Val
        # time.sleep(random.randint(1, 2))
        FEN = ''
        MTnum = 0
        fileList = []
        squareCount = 0
        slashCounter = 0
        templateTime = time.time()

        for row in lengthArray:
            for column in widthArray:
                image = resized_crop_img[int(pieceDim * (row - 1)): int(pieceDim * row),int(pieceDim * (column - 1)): int(pieceDim * column)]

                big = imutils.resize(image, width=126)
                # cv2.imshow('Image', big)
                # cv2.waitKey(0)

                if squareCount % 8 == 0 and MTnum != 0 and squareCount != 0:
                    FEN += str(MTnum)

                    MTnum = 0
                    if slashCounter >= 8:
                        slashCounter -= 8
                        FEN += '/'

                if fastMode == 1:
                    rgbTemplateMatch(SAVE_PATH + 'AllPieces/BPawnB.PNG', image)
                    if max_Val < 0.8:
                        rgbTemplateMatch(SAVE_PATH + 'AllPieces/BPawnW.PNG', image)
                        if max_Val < 0.8:
                            rgbTemplateMatch(SAVE_PATH + 'AllPieces/WPawnB.PNG', image)
                            if max_Val < 0.8:
                                rgbTemplateMatch(SAVE_PATH + 'AllPieces/WPawnW.PNG', image)
                                if max_Val < 0.8:
                                    rgbTemplateMatch(SAVE_PATH + 'AllPieces/BRookB.PNG', image)
                                    if max_Val < 0.79:
                                        rgbTemplateMatch(SAVE_PATH + 'AllPieces/BRookW.PNG', image)
                                        if max_Val < 0.79:
                                            rgbTemplateMatch(SAVE_PATH + 'AllPieces/WRookB.PNG', image)
                                            if max_Val < 0.8:
                                                rgbTemplateMatch(SAVE_PATH + 'AllPieces/WRookW.PNG', image)
                                                if max_Val < 0.8:
                                                    rgbTemplateMatch(SAVE_PATH + 'AllPieces/BBishopB.PNG', image)
                                                    if max_Val < 0.8:
                                                        rgbTemplateMatch(SAVE_PATH + 'AllPieces/BBishopW.PNG', image)
                                                        if max_Val < 0.8:
                                                            rgbTemplateMatch(SAVE_PATH + 'AllPieces/WBishopB.PNG', image)
                                                            if max_Val < 0.8:
                                                                rgbTemplateMatch(SAVE_PATH + 'AllPieces/WBishopW.PNG', image)
                                                                if max_Val < 0.8:
                                                                    rgbTemplateMatch(SAVE_PATH + 'AllPieces/BKnightB.PNG', image)
                                                                    if max_Val < 0.8:
                                                                        rgbTemplateMatch(SAVE_PATH + 'AllPieces/BKnightW.PNG', image)
                                                                        if max_Val < 0.8:
                                                                            rgbTemplateMatch(SAVE_PATH + 'AllPieces/WKnightB.PNG', image)
                                                                            if max_Val < 0.8:
                                                                                rgbTemplateMatch(SAVE_PATH + 'AllPieces/WKnightW.PNG', image)
                                                                                if max_Val < 0.8:
                                                                                    rgbTemplateMatch(SAVE_PATH + 'AllPieces/BKingB.PNG',image)
                                                                                    if max_Val < 0.8:
                                                                                        rgbTemplateMatch(SAVE_PATH + 'AllPieces/BKingW.PNG',image)
                                                                                        if max_Val < 0.8:
                                                                                            rgbTemplateMatch(SAVE_PATH + 'AllPieces/WKingB.PNG',image)
                                                                                            if max_Val < 0.8:
                                                                                                rgbTemplateMatch(SAVE_PATH + 'AllPieces/WKingW.PNG',image)
                                                                                                if max_Val < 0.8:
                                                                                                    rgbTemplateMatch(SAVE_PATH + 'AllPieces/BQueenB.PNG',image)
                                                                                                    if max_Val < 0.9:
                                                                                                        rgbTemplateMatch(SAVE_PATH + 'AllPieces/BQueenW.PNG',image)
                                                                                                        if max_Val < 0.9:
                                                                                                            rgbTemplateMatch(SAVE_PATH + 'AllPieces/WQueenB.PNG',image)
                                                                                                            if max_Val < 0.7:
                                                                                                                rgbTemplateMatch(SAVE_PATH + 'AllPieces/WQueenW.PNG',image)
                                                                                                                if max_Val < 0.7:
                                                                                                                    if MTnum <= 6:
                                                                                                                        slashCounter += 1
                                                                                                                        MTnum += 1
                                                                                                                        if slashCounter >= 8:
                                                                                                                            FEN += str(MTnum)
                                                                                                                            FEN += '/'
                                                                                                                            slashCounter -= 8
                                                                                                                            MTnum = 0
                                                                                                                        elif squareCount == 64:
                                                                                                                            FEN += str(MTnum)
                                                                                                                    else:
                                                                                                                        FEN += str(8)
                                                                                                                        MTnum = 0
                                                                                                                        slashCounter = 0
                                                                                                                        if squareCount != 64:
                                                                                                                            FEN += '/'
                                                                                                                else:
                                                                                                                    if MTnum != 0:
                                                                                                                        FEN += str(
                                                                                                                            MTnum)

                                                                                                                        MTnum = 0
                                                                                                                    FEN += 'Q'
                                                                                                                    slashCounter += 1
                                                                                                                    if slashCounter >= 8:
                                                                                                                        slashCounter -= 8
                                                                                                                        FEN += '/'
                                                                                                            else:
                                                                                                                if MTnum != 0:
                                                                                                                    FEN += str(
                                                                                                                        MTnum)

                                                                                                                    MTnum = 0
                                                                                                                FEN += 'Q'
                                                                                                                slashCounter += 1
                                                                                                                if slashCounter >= 8:
                                                                                                                    slashCounter -= 8
                                                                                                                    FEN += '/'
                                                                                                        else:
                                                                                                            if MTnum != 0:
                                                                                                                FEN += str(
                                                                                                                    MTnum)

                                                                                                                MTnum = 0
                                                                                                            FEN += 'q'
                                                                                                            slashCounter += 1
                                                                                                            if slashCounter >= 8:
                                                                                                                slashCounter -= 8
                                                                                                                FEN += '/'
                                                                                                    else:
                                                                                                        if MTnum != 0:
                                                                                                            FEN += str(
                                                                                                                MTnum)

                                                                                                            MTnum = 0
                                                                                                        FEN += 'q'
                                                                                                        slashCounter += 1
                                                                                                        if slashCounter >= 8:
                                                                                                            slashCounter -= 8
                                                                                                            FEN += '/'
                                                                                                else:
                                                                                                    if MTnum != 0:
                                                                                                        FEN += str(MTnum)

                                                                                                        MTnum = 0
                                                                                                    FEN += 'K'
                                                                                                    slashCounter += 1
                                                                                                    if slashCounter >= 8:
                                                                                                        slashCounter -= 8
                                                                                                        FEN += '/'
                                                                                            else:
                                                                                                if MTnum != 0:
                                                                                                    FEN += str(MTnum)

                                                                                                    MTnum = 0
                                                                                                FEN += 'K'
                                                                                                slashCounter += 1
                                                                                                if slashCounter >= 8:
                                                                                                    slashCounter -= 8
                                                                                                    FEN += '/'

                                                                                        else:
                                                                                            if MTnum != 0:
                                                                                                FEN += str(MTnum)

                                                                                                MTnum = 0
                                                                                            FEN += 'k'
                                                                                            slashCounter += 1
                                                                                            if slashCounter >= 8:
                                                                                                slashCounter -= 8
                                                                                                FEN += '/'

                                                                                    else:
                                                                                        if MTnum != 0:
                                                                                            FEN += str(MTnum)

                                                                                            MTnum = 0
                                                                                        FEN += 'k'
                                                                                        slashCounter += 1
                                                                                        if slashCounter >= 8:
                                                                                            slashCounter -= 8
                                                                                            FEN += '/'
                                                                                else:
                                                                                    if MTnum != 0:
                                                                                        FEN += str(MTnum)

                                                                                        MTnum = 0
                                                                                    FEN += 'N'
                                                                                    slashCounter += 1
                                                                                    if slashCounter >= 8:
                                                                                        slashCounter -= 8
                                                                                        FEN += '/'

                                                                            else:
                                                                                if MTnum != 0:
                                                                                    FEN += str(MTnum)

                                                                                    MTnum = 0
                                                                                FEN += 'N'
                                                                                slashCounter += 1
                                                                                if slashCounter >= 8:
                                                                                    slashCounter -= 8
                                                                                    FEN += '/'

                                                                        else:
                                                                            if MTnum != 0:
                                                                                FEN += str(MTnum)

                                                                                MTnum = 0
                                                                            FEN += 'n'
                                                                            slashCounter += 1
                                                                            if slashCounter >= 8:
                                                                                slashCounter -= 8
                                                                                FEN += '/'

                                                                    else:
                                                                        if MTnum != 0:
                                                                            FEN += str(MTnum)

                                                                            MTnum = 0
                                                                        FEN += 'n'
                                                                        slashCounter += 1
                                                                        if slashCounter >= 8:
                                                                            slashCounter -= 8
                                                                            FEN += '/'

                                                                else:
                                                                    if MTnum != 0:
                                                                        FEN += str(MTnum)

                                                                        MTnum = 0
                                                                    FEN += 'B'
                                                                    slashCounter += 1
                                                                    if slashCounter >= 8:
                                                                        slashCounter -= 8
                                                                        FEN += '/'

                                                            else:
                                                                if MTnum != 0:
                                                                    FEN += str(MTnum)

                                                                    MTnum = 0
                                                                FEN += 'B'
                                                                slashCounter += 1
                                                                if slashCounter >= 8:
                                                                    slashCounter -= 8
                                                                    FEN += '/'

                                                        else:
                                                            if MTnum != 0:
                                                                FEN += str(MTnum)

                                                                MTnum = 0
                                                            FEN += 'b'
                                                            slashCounter += 1
                                                            if slashCounter >= 8:
                                                                slashCounter -= 8
                                                                FEN += '/'
                                                    else:
                                                        if MTnum != 0:
                                                            FEN += str(MTnum)

                                                            MTnum = 0
                                                        FEN += 'b'
                                                        slashCounter += 1
                                                        if slashCounter >= 8:
                                                            slashCounter -= 8
                                                            FEN += '/'
                                                else:
                                                    if MTnum != 0:
                                                        FEN += str(MTnum)

                                                        MTnum = 0
                                                    FEN += 'R'
                                                    slashCounter += 1
                                                    if slashCounter >= 8:
                                                        slashCounter -= 8
                                                        FEN += '/'
                                            else:
                                                if MTnum != 0:
                                                    FEN += str(MTnum)

                                                    MTnum = 0
                                                FEN += 'R'
                                                slashCounter += 1
                                                if slashCounter >= 8:
                                                    slashCounter -= 8
                                                    FEN += '/'
                                        else:
                                            if MTnum != 0:
                                                FEN += str(MTnum)

                                                MTnum = 0
                                            FEN += 'r'
                                            slashCounter += 1
                                            if slashCounter >= 8:
                                                slashCounter -= 8
                                                FEN += '/'
                                    else:
                                        if MTnum != 0:
                                            FEN += str(MTnum)

                                            MTnum = 0
                                        FEN += 'r'
                                        slashCounter += 1
                                        if slashCounter >= 8:
                                            slashCounter -= 8
                                            FEN += '/'
                                else:
                                    if MTnum != 0:
                                        FEN += str(MTnum)

                                        MTnum = 0
                                    FEN += 'P'
                                    slashCounter += 1
                                    if slashCounter >= 8:
                                        slashCounter -= 8
                                        FEN += '/'
                            else:
                                if MTnum != 0:
                                    FEN += str(MTnum)

                                    MTnum = 0
                                FEN += 'P'
                                slashCounter += 1
                                if slashCounter >= 8:
                                    slashCounter -= 8
                                    FEN += '/'
                        else:
                            if MTnum != 0:
                                FEN += str(MTnum)

                                MTnum = 0
                            FEN += 'p'
                            slashCounter += 1
                            if slashCounter >= 8:
                                slashCounter -= 8
                                FEN += '/'
                    else:
                        if MTnum != 0:
                            FEN += str(MTnum)

                            MTnum = 0
                        FEN += 'p'
                        slashCounter += 1
                        if slashCounter >= 8:
                            slashCounter -= 8
                            FEN += '/'
                else:
                    similarList = []

                    for file in os.listdir(SAVE_PATH + "AllPieces"):
                        filename = os.fsdecode(file)
                        if filename.endswith(".png"):
                            rgbTemplateMatch(SAVE_PATH + "AllPieces/" + filename, image)
                            similarList.append(max_Val)

                    maxIndex = similarList.index(max(similarList))
                    if max(similarList) > 0.5:
                        foundTemplate = templateList[maxIndex]
                        # print(templateList[maxIndex], similarList[maxIndex], maxIndex)
                        if MTnum != 0:
                            FEN += str(MTnum)
                            MTnum = 0

                        if foundTemplate[0] == 'B':
                            FEN += foundTemplate[1].lower()
                        else:
                            FEN += foundTemplate[1]

                        slashCounter += 1
                        if slashCounter >= 8:
                            slashCounter -= 8
                            FEN += '/'
                    else:
                        slashCounter += 1
                        MTnum += 1
                        if slashCounter >= 8:
                            FEN += str(MTnum)
                            FEN += '/'
                            slashCounter -= 8
                            MTnum = 0
                        elif squareCount == 64:
                            FEN += str(MTnum)


        # print("TIME TO TEMPLATE MATCH", time.time() - templateTime)
        # print("TIME AFTER TEMPLATE MATCH", time.time() - startTime)
        # divideCount = 7
        # indexPlace = 0

        # print("Before FEN: " + FEN)
        # print("FEN LENGTH: ", len(FEN))
        # FENList = list(FEN)
        # print("FENList", FENList)
        # totalValue = 0
        # for letter in FENList:
        #     isInt = IsInt(letter)
        #     if isInt == False:
        #         # print("totalValue increased by 1")
        #         totalValue += 1
        #     elif isInt == True:
        #         # print("totalValue increased by", int(letter))
        #         totalValue += int(letter)
        #
        # for letter in FENList:
        #     if letter == '/':
        #         continue
        #     # print(letter),
        #     indexPlace += 1
        #     # print("indexPlace", indexPlace)
        #     # print("Divide Count is", divideCount),
        #
        #     isInt = IsInt(letter)
        #
        #     if isInt == False:
        #         divideCount -= 1
        #     elif isInt == True:
        #         # print("SUBTRACTED", int(letter))
        #         divideCount -= int(letter)
        #     if divideCount < 0:
        #         # print("SLASHING"),
        #         divideCount = 8
        #         FENList.insert(indexPlace, '/')
        #         continue
        #
        # FEN = ''.join(FENList)

        if FEN.endswith('/'):
            FEN = FEN[:-1]

        castleAvailability = ''
        if canCastleKingWhite == True:
            castleAvailability += 'K'
        if canCastleQueenWhite == True:
            castleAvailability += 'Q'
        if canCastleKingBlack == True:
            castleAvailability += 'k'
        if canCastleQueenBlack == True:
            castleAvailability += 'q'

        if castleAvailability == '':
            castleAvailability = '-'

        fixedfen = FEN + ' ' + toMove + ' ' + castleAvailability + ' - ' + '0 0'
        print("FEN: " + fixedfen)
        # print("TIME TO CREATE FEN:", time.time() - startTime)

        board = chess.Board(fixedfen)
        print(board)

        handler = chess.uci.InfoHandler()

        # break

        engine.info_handlers.append(handler)
        engine.position(board)
        # Depth = engine.go(movetime = 1)
        Depth = engine.go(depth = random.randint(6, 8))
        bestMove = str(Depth[0])
        print('Best Move', bestMove)

        # continue

        if difficulty == 1:
            try:
                move2 = str(handler.info['pv'][2][0])
                move3 = str(handler.info['pv'][3][0])

                score = (handler.info['score'][1].cp)
                score2 = (handler.info['score'][2].cp)
                score3 = (handler.info['score'][3].cp)

                moveChoose = random.randint(1, 3)

                print("Move1:", bestMove, "Move2:", move2, "Move3:", move3)
                print("Score1:", score, "Score2:", score2, "Score3:", score3)

                if abs(abs(score) - abs(score2)) >= 100 or abs(abs(score2) - abs(score3)) >= 100:
                    print("Found Obvious Move")
                else:
                    if 10 < movecount < 30:
                        time.sleep(random.randint(0, 500)/100)
                    if moveChoose == 2:
                        bestMove = move2
                    elif moveChoose == 3:
                        bestMove = move3

                    print("Chose move", moveChoose)
            except:
                pass
        else:
            if 10 < movecount < 30:
                time.sleep(random.randint(0, 500) / 100)
            elif 10 >= movecount:
                time.sleep(random.randint(0, 100) / 100)

        print("Search depth:", handler.info['depth'])

        # continue

        if 'e1' in bestMove:
            canCastleKingWhite = False
            canCastleQueenWhite = False
        if 'a1' in bestMove:
            canCastleQueenWhite = False
        if 'h1' in bestMove:
            canCastleKingWhite = False

        if 'e8' in bestMove:
            canCastleKingBlack = False
            canCastleQueenBlack = False
        if 'a8' in bestMove:
            canCastleQueenBlack = False
        if 'h8' in bestMove:
            canCastleKingBlack = False

        HalfOne = bestMove[:2]
        HalfTwo = bestMove[2:4]

        pinkTop = 155 + (boardHeight - pieceHeight * int(HalfOne[1])) + 25
        pinkLeft = 167 + pieceWidth * (ord(HalfOne[0]) - 97) + 25

        print(pinkLeft, pinkTop)

        greenTop = 155 + (boardHeight - pieceHeight * int(HalfTwo[1])) + 25
        greenLeft = 167 + pieceWidth * (ord(HalfTwo[0]) - 97) + 25

        # print(greenLeft, greenTop)
        print("Time to calculate move:", time.time() - startTime)
        # pyautogui.moveTo(pinkLeft, pinkTop, 0.001)
        # time.sleep(0.1)

        # pyautogui.mouseDown(x=pinkLeft, y=pinkTop)

        clickDown(int(pinkLeft), int(pinkTop))

        # time.sleep(0.1)
        # pyautogui.moveTo(greenLeft,greenTop,0.001)
        time.sleep(0.25)

        clickUp(int(greenLeft), int(greenTop))

        # pyautogui.mouseUp(x=greenLeft, y=greenTop)

        # pyautogui.moveTo(5,5, 0.001)
        win32api.SetCursorPos((5,5))
        movecount += 1
        print("TIME TO RUN", time.time() - startTime)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("EXITING")
