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
import chess
import chess.uci
import glob
import imutils
import image_slicer

SAVE_PATH = "D:/Screenshots/"

# ImageGrab.grab().save(SAVE_PATH + "ChessShot.jpg", "JPEG")
# print("SAVED SCREENSHOT")

splitCoordTopLeft = (282, 154)
splitCoordBottomRight = (1099, 971)

img = Image.open(SAVE_PATH + "ChessShot.jpg")

prevPt = (0, 0)

def rgbImgTM_PATHLESS(imagePath, temp):
    global maximum_Val
    img = cv2.imread(imagePath)

    res = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF_NORMED)
    # print(cv2.minMaxLoc(res))
    min_val, maximum_Val, min_loc, max_loc = cv2.minMaxLoc(res)

    return maximum_Val

def rgbImgTM(imagePath, templatePath):
    global maximum_Val
    img = cv2.imread(imagePath)

    temp = cv2.imread(templatePath)

    # w, h = temp.shape[:-1]


    res = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF_NORMED)
    # print(cv2.minMaxLoc(res))
    min_val, maximum_Val, min_loc, max_loc = cv2.minMaxLoc(res)

    return maximum_Val

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
    # w, h = templater.shape[:2]

    res = cv2.matchTemplate(img_edge,template_edge,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    # loc = np.where( res >= threshold)
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    _min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
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

boardHeight = 816
pieceHeight = 816/8
pieceWidth = 816/8

enginePath = 'C:/Users/Recursor/Desktop/BACKUP/Engines/'

# engine = chess.uci.popen_engine(enginePath + 'stockfish-8-win/Windows/stockfish_8_x64.exe')
# engine = chess.uci.popen_engine(enginePath + 'Rybkav2.3.2a.mp.x64.exe')
# engine = chess.uci.popen_engine(enginePath + 'Spike/Spike1.4.exe')
# engine = chess.uci.popen_engine(enginePath + 'naum.exe')
engine = chess.uci.popen_engine(enginePath + 'DeepHiarcs14WCSC_AC4.exe')
# engine = chess.uci.popen_engine(enginePath + 'da-165/DisasterArea-1.65w64.exe')
print('Engine opened')

engine.uci()
print('UCI loaded')
print(engine.name, 'Loaded')

player = input('Input 0 for white or 1 for black\n')
handler = chess.uci.InfoHandler()
engine.info_handlers.append(handler)
engine.setoption({'MultiPV': 3})
print("Initiated")

canCastleQueenWhite = True
canCastleKingWhite = True

canCastleQueenBlack = True
canCastleKingBlack = True
movecount = int(input('Enter movecount\n'))


# engine.setoption({'PawnStruct': 150})
# engine.setoption({'Passers': 150})
# engine.setoption({'King_Safety': 150})
# engine.setoption({'Mobility': 90})
# engine.setoption({'CenterControl': 150})
# engine.setoption({'PSQT': 200})
# engine.setoption({'King_Attacks': 150})
engine.setoption({'Playing Style': 'Solid'})

def clickDown(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)

def clickUp(x,y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

widthArray = [1, 2, 3, 4, 5, 6, 7, 8]
lengthArray = widthArray

crop_img = np.array(ImageGrab.grab(bbox=(283, 157, 1114, 972)))
resized = imutils.resize(crop_img, width=204, height=204)
print('Dimensions', resized.shape)
boardDim = resized.shape[0]
pieceDim = resized.shape[0]/8

try:
    while True:
        startTime = time.time()

        cropped_color_black = np.array(ImageGrab.grab(bbox = (895, 105, 945, 146)))
        # cropped_color_black = cv2.imread(SAVE_PATH + 'croppedBlack.jpg')
        # cv2.imshow('Cropped', cropped_color_black)
        # cv2.waitKey(0)
        cropped_color_white = np.array(ImageGrab.grab(bbox = (895, 984, 950, 1026)))
        # cropped_color_white = cv2.imread(SAVE_PATH + 'croppedWhite.jpg')
        # cv2.imshow('Cropped', cropped_color_white)
        # cv2.waitKey(0)

        resized_crop_black = imutils.resize(cropped_color_black, width=52)
        # cv2.imshow('Resized Cropped Black', resized_crop_black)
        # cv2.waitKey(0)
        Image.fromarray(resized_crop_black, 'RGB').save(SAVE_PATH + 'croppedBlack.jpg')

        resized_crop_white = imutils.resize(cropped_color_white, width=52)
        # cv2.imshow('Resized Cropped White', resized_crop_white)
        # cv2.waitKey(0)
        Image.fromarray(resized_crop_white, 'RGB').save(SAVE_PATH + 'croppedWhite.jpg')

        returnBlack = rgbImgTM(SAVE_PATH + 'croppedBlack.jpg', 'D:/Screenshots/Back/BlackTimerGo.jpg')
        returnWhite = rgbImgTM(SAVE_PATH + 'croppedWhite.jpg', 'D:/Screenshots/Back/WhiteTimerGo.jpg')

        toMove = ''
        if returnBlack > returnWhite:
            if returnBlack < 0.9:
                toMove = 'w'
            # print("Black to Move with", round(returnBlack * 100, 2), "% confidence")
            toMove = 'b'
        elif returnWhite > returnBlack:
            if returnWhite < 0.9:
                toMove = 'b'
            # print("White to Move with", round(returnWhite * 100, 2), "% confidence")
            toMove = 'w'
        else:
            toMove = 'w'

        if toMove == 'b' and player == '0':
            continue
        if toMove == 'w' and player == '1':
            continue

        time.sleep(0.1)

        print("Time before Slice", time.time() - startTime)

        Image.fromarray(resized, 'RGB').save(SAVE_PATH + 'Pieces/croppedBoard.png')
        # cv2.imshow('Cropped', resized_crop_img)
        # cv2.waitKey(0)
        tiles = image_slicer.slice(SAVE_PATH + 'Pieces/croppedBoard.png', 64, save=False)
        image_slicer.save_tiles(tiles, directory='D:/Screenshots/Pieces/Sliced')
        print('SLICED')
        crop_img = np.array(ImageGrab.grab(bbox=(283, 157, 1114, 972)))
        resized = imutils.resize(crop_img, width=204, height=204)
        print('Dimensions', resized.shape)

        print("Time after Slice", time.time() - startTime)

        global maximum_Val
        # time.sleep(random.randint(1, 2))
        FEN = ''
        MTnum = 0
        fileList = []
        squareCount = 0
        templateTime = time.time()
        slashCounter = 0
        for row in lengthArray:
            for column in widthArray:
                image = resized[int(pieceDim * (row - 1)): int(pieceDim * row), int(pieceDim * (column - 1)): int(pieceDim * column)]

                if squareCount % 8 == 0 and MTnum != 0 and squareCount != 0:
                    FEN += str(MTnum)
                    slashCounter += MTnum
                    MTnum = 0
                    if slashCounter >= 8:
                        slashCounter -= 8
                        FEN += '/'

                squareCount += 1
                rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BPawnB.PNG', image)
                if maximum_Val < 0.8:
                    rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BPawnW.PNG', image)
                    if maximum_Val < 0.8:
                        rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/WPawnB.PNG', image)
                        if maximum_Val < 0.8:
                            rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/WPawnW.PNG', image)
                            if maximum_Val < 0.8:
                                rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BRookB.PNG', image)
                                if maximum_Val < 0.8:
                                    rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BRookW.PNG', image)
                                    if maximum_Val < 0.8:
                                        rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/WRookB.PNG', image)
                                        if maximum_Val < 0.7:
                                            rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/WRookW.PNG', image)
                                            if maximum_Val < 0.7:
                                                rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BBishopB.PNG', image)
                                                if maximum_Val < 0.8:
                                                    rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BBishopW.PNG', image)
                                                    if maximum_Val < 0.8:
                                                        rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/WBishopB.PNG', image)
                                                        if maximum_Val < 0.8:
                                                            rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/WBishopW.PNG', image)
                                                            if maximum_Val < 0.8:
                                                                rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BKnightB.PNG', image)
                                                                if maximum_Val < 0.8:
                                                                    rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BKnightW.PNG', image)
                                                                    if maximum_Val < 0.8:
                                                                        rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/WKnightB.PNG', image)
                                                                        if maximum_Val < 0.8:
                                                                            rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/WKnightW.PNG',image)
                                                                            if maximum_Val < 0.8:
                                                                                rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BKingB.PNG', image)
                                                                                if maximum_Val < 0.8:
                                                                                    rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BKingW.PNG', image)
                                                                                    if maximum_Val < 0.8:
                                                                                        rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/WKingB.PNG', image)
                                                                                        if maximum_Val < 0.8:
                                                                                            rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/WKingW.PNG', image)
                                                                                            if maximum_Val < 0.8:
                                                                                                rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BQueenB.PNG', image)
                                                                                                if maximum_Val < 0.8:
                                                                                                    rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/BQueenW.PNG', image)
                                                                                                    if maximum_Val < 0.8:
                                                                                                        rgbImgTM_PATHLESS(SAVE_PATH + 'WhitePieces/Smaller/WQueenB.PNG', image)
                                                                                                        if maximum_Val < 0.6:
                                                                                                            templateMatch(SAVE_PATH + 'WhitePieces/Smaller/WQueenW.PNG', image)
                                                                                                            if max_val < 0.6:
                                                                                                                if MTnum <= 6:
                                                                                                                    MTnum += 1
                                                                                                                    if squareCount == 64:
                                                                                                                        FEN += str(MTnum)
                                                                                                                else:
                                                                                                                    FEN += str(8)
                                                                                                                    MTnum = 0
                                                                                                                    if squareCount != 64:
                                                                                                                      FEN += '/'
                                                                                                            else:
                                                                                                                if MTnum != 0:
                                                                                                                    FEN += str(MTnum)
                                                                                                                    slashCounter += MTnum
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
                                                                                                                slashCounter += MTnum
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
                                                                                                            slashCounter += MTnum
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
                                                                                                        slashCounter += MTnum
                                                                                                        MTnum = 0
                                                                                                    FEN += 'q'
                                                                                                    slashCounter += 1
                                                                                                    if slashCounter >= 8:
                                                                                                        slashCounter -= 8
                                                                                                        FEN += '/'
                                                                                            else:
                                                                                                if MTnum != 0:
                                                                                                    FEN += str(MTnum)
                                                                                                    slashCounter += MTnum
                                                                                                    MTnum = 0
                                                                                                FEN += 'K'
                                                                                                slashCounter += 1
                                                                                                if slashCounter >= 8:
                                                                                                    slashCounter -= 8
                                                                                                    FEN += '/'
                                                                                        else:
                                                                                            if MTnum != 0:
                                                                                                FEN += str(MTnum)
                                                                                                slashCounter += MTnum
                                                                                                MTnum = 0
                                                                                            FEN += 'K'
                                                                                            slashCounter += 1
                                                                                            if slashCounter >= 8:
                                                                                                slashCounter -= 8
                                                                                                FEN += '/'
                                                                                    else:
                                                                                        if MTnum != 0:
                                                                                            FEN += str(MTnum)
                                                                                            slashCounter += MTnum
                                                                                            MTnum = 0
                                                                                        FEN += 'k'
                                                                                        slashCounter += 1
                                                                                        if slashCounter >= 8:
                                                                                            slashCounter -= 8
                                                                                            FEN += '/'
                                                                                else:
                                                                                    if MTnum != 0:
                                                                                        FEN += str(MTnum)
                                                                                        slashCounter += MTnum
                                                                                        MTnum = 0
                                                                                    FEN += 'k'
                                                                                    slashCounter += 1
                                                                                    if slashCounter >= 8:
                                                                                        slashCounter -= 8
                                                                                        FEN += '/'
                                                                            else:
                                                                                if MTnum != 0:
                                                                                    FEN += str(MTnum)
                                                                                    slashCounter += MTnum
                                                                                    MTnum = 0
                                                                                FEN += 'N'
                                                                                slashCounter += 1
                                                                                if slashCounter >= 8:
                                                                                    slashCounter -= 8
                                                                                    FEN += '/'
                                                                        else:
                                                                            if MTnum != 0:
                                                                                FEN += str(MTnum)
                                                                                slashCounter += MTnum
                                                                                MTnum = 0
                                                                            FEN += 'N'
                                                                            slashCounter += 1
                                                                            if slashCounter >= 8:
                                                                                slashCounter -= 8
                                                                                FEN += '/'
                                                                    else:
                                                                        if MTnum != 0:
                                                                            FEN += str(MTnum)
                                                                            slashCounter += MTnum
                                                                            MTnum = 0
                                                                        FEN += 'n'
                                                                        slashCounter += 1
                                                                        if slashCounter >= 8:
                                                                            slashCounter -= 8
                                                                            FEN += '/'
                                                                else:
                                                                    if MTnum != 0:
                                                                        FEN += str(MTnum)
                                                                        slashCounter += MTnum
                                                                        MTnum = 0
                                                                    FEN += 'n'
                                                                    slashCounter += 1
                                                                    if slashCounter >= 8:
                                                                        slashCounter -= 8
                                                                        FEN += '/'
                                                            else:
                                                                if MTnum != 0:
                                                                    FEN += str(MTnum)
                                                                    slashCounter += MTnum
                                                                    MTnum = 0
                                                                FEN += 'B'
                                                                slashCounter += 1
                                                                if slashCounter >= 8:
                                                                    slashCounter -= 8
                                                                    FEN += '/'
                                                        else:
                                                            if MTnum != 0:
                                                                FEN += str(MTnum)
                                                                slashCounter += MTnum
                                                                MTnum = 0
                                                            FEN += 'B'
                                                            slashCounter += 1
                                                            if slashCounter >= 8:
                                                                slashCounter -= 8
                                                                FEN += '/'
                                                    else:
                                                        if MTnum != 0:
                                                            FEN += str(MTnum)
                                                            slashCounter += MTnum
                                                            MTnum = 0
                                                        FEN += 'b'
                                                        slashCounter += 1
                                                        if slashCounter >= 8:
                                                            slashCounter -= 8
                                                            FEN += '/'
                                                else:
                                                    if MTnum != 0:
                                                        FEN += str(MTnum)
                                                        slashCounter += MTnum
                                                        MTnum = 0
                                                    FEN += 'b'
                                                    slashCounter += 1
                                                    if slashCounter >= 8:
                                                        slashCounter -= 8
                                                        FEN += '/'
                                            else:
                                                if MTnum != 0:
                                                    FEN += str(MTnum)
                                                    slashCounter += MTnum
                                                    MTnum = 0
                                                FEN += 'R'
                                                slashCounter += 1
                                                if slashCounter >= 8:
                                                    slashCounter -= 8
                                                    FEN += '/'
                                        else:
                                            if MTnum != 0:
                                                FEN += str(MTnum)
                                                slashCounter += MTnum
                                                MTnum = 0
                                            FEN += 'R'
                                            slashCounter += 1
                                            if slashCounter >= 8:
                                                slashCounter -= 8
                                                FEN += '/'
                                    else:
                                        if MTnum != 0:
                                            FEN += str(MTnum)
                                            slashCounter += MTnum
                                            MTnum = 0
                                        FEN += 'r'
                                        slashCounter += 1
                                        if slashCounter >= 8:
                                            slashCounter -= 8
                                            FEN += '/'
                                else:
                                    if MTnum != 0:
                                        FEN += str(MTnum)
                                        slashCounter += MTnum
                                        MTnum = 0
                                    FEN += 'r'
                                    slashCounter += 1
                                    if slashCounter >= 8:
                                        slashCounter -= 8
                                        FEN += '/'
                            else:
                                if MTnum != 0:
                                    FEN += str(MTnum)
                                    slashCounter += MTnum
                                    MTnum = 0
                                FEN += 'P'
                                slashCounter += 1
                                if slashCounter >= 8:
                                    slashCounter -= 8
                                    FEN += '/'
                        else:
                            if MTnum != 0:
                                FEN += str(MTnum)
                                slashCounter += MTnum
                                MTnum = 0
                            FEN += 'P'
                            slashCounter += 1
                            if slashCounter >= 8:
                                slashCounter -= 8
                                FEN += '/'
                    else:
                        if MTnum != 0:
                            FEN += str(MTnum)
                            slashCounter += MTnum
                            MTnum = 0
                        FEN += 'p'
                        slashCounter += 1
                        if slashCounter >= 8:
                            slashCounter -= 8
                            FEN += '/'
                else:
                    if MTnum != 0:
                        FEN += str(MTnum)
                        slashCounter += MTnum
                        MTnum = 0
                    FEN += 'p'
                    slashCounter += 1
                    if slashCounter >= 8:
                        slashCounter -= 8
                        FEN += '/'

                # templateMatch('D:/Screenshots/whitepieces/Smaller/BPawn.PNG', image)
                # if max_val < 0.65:
                #     templateMatch('D:/Screenshots/whitepieces/Smaller/WPawn.PNG', image)
                #     if max_val < 0.5:
                #         templateMatch('D:/Screenshots/whitepieces/Smaller/BRook.PNG', image)
                #         if max_val < 0.55:
                #             templateMatch('D:/Screenshots/whitepieces/Smaller/WRook.PNG', image)
                #             if max_val < 0.26:
                #                 templateMatch('D:/Screenshots/whitepieces/Smaller/WKnight.PNG', image)
                #                 if max_val < 0.4:
                #                     templateMatch('D:/Screenshots/whitepieces/Smaller/BKnight.PNG', image)
                #                     if max_val < 0.55:
                #                         templateMatch('D:/Screenshots/whitepieces/Smaller/BBishop.PNG', image)
                #                         if max_val < 0.65:
                #                             templateMatch('D:/Screenshots/whitepieces/Smaller/WBishop.PNG', image)
                #                             if max_val < 0.25:
                #                                 templateMatch('D:/Screenshots/whitepieces/Smaller/BKing.PNG', image)
                #                                 if max_val < 0.50:
                #                                     templateMatch('D:/Screenshots/whitepieces/Smaller/WKing.PNG', image)
                #                                     if max_val < 0.45:
                #                                         templateMatch('D:/Screenshots/whitepieces/Smaller/WQueen.PNG', image)
                #                                         if max_val < 0.45:
                #                                             templateMatch('D:/Screenshots/whitepieces/Smaller/BQueen.PNG', image)
                #                                             if max_val < 0.65:
                #                                                 # print('No match, likely Empty Square (1-8)')
                #                                                 # print("MTnum", MTnum, 'SquareCount', squareCount)
                #                                                 if MTnum <= 6:
                #                                                     MTnum += 1
                #                                                     if squareCount == 64:
                #                                                         FEN += str(MTnum)
                #                                                 else:
                #                                                     FEN += str(8)
                #                                                     MTnum = 0
                #                                                     if squareCount != 64:
                #                                                       FEN += '/'
                #                                             else:
                #                                                 if MTnum != 0:
                #                                                     FEN += str(MTnum)
                #                                                     slashCounter += MTnum
                #                                                     MTnum = 0
                #                                                 FEN += 'q'
                #                                                 slashCounter += 1
                #                                                 if slashCounter >= 8:
                #                                                     slashCounter -= 8
                #                                                     FEN += '/'
                #                                         else:
                #                                             if MTnum != 0:
                #                                                 FEN += str(MTnum)
                #                                                 slashCounter += MTnum
                #                                                 MTnum = 0
                #                                             FEN += 'Q'
                #                                             slashCounter += 1
                #                                             if slashCounter >= 8:
                #                                                 slashCounter -= 8
                #                                                 FEN += '/'
                #                                     else:
                #                                         if MTnum != 0:
                #                                             FEN += str(MTnum)
                #                                             slashCounter += MTnum
                #                                             MTnum = 0
                #                                         FEN += 'K'
                #                                         slashCounter += 1
                #                                         if slashCounter >= 8:
                #                                             slashCounter -= 8
                #                                             FEN += '/'
                #                                 else:
                #                                     if MTnum != 0:
                #                                         FEN += str(MTnum)
                #                                         slashCounter += MTnum
                #                                         MTnum = 0
                #                                     FEN += 'k'
                #                                     slashCounter += 1
                #                                     if slashCounter >= 8:
                #                                         slashCounter -= 8
                #                                         FEN += '/'
                #                             else:
                #                                 if MTnum != 0:
                #                                     FEN += str(MTnum)
                #                                     slashCounter += MTnum
                #                                     MTnum = 0
                #                                 FEN += 'B'
                #                                 slashCounter += 1
                #                                 if slashCounter >= 8:
                #                                     slashCounter -= 8
                #                                     FEN += '/'
                #                         else:
                #                             if MTnum != 0:
                #                                 FEN += str(MTnum)
                #                                 slashCounter += MTnum
                #                                 MTnum = 0
                #                             FEN += 'b'
                #                             slashCounter += 1
                #                             if slashCounter >= 8:
                #                                 slashCounter -= 8
                #                                 FEN += '/'
                #                     else:
                #                         if MTnum != 0:
                #                             FEN += str(MTnum)
                #                             slashCounter += MTnum
                #                             MTnum = 0
                #                         FEN += 'n'
                #                         slashCounter += 1
                #                         if slashCounter >= 8:
                #                             slashCounter -= 8
                #                             FEN += '/'
                #                 else:
                #                     if MTnum != 0:
                #                         FEN += str(MTnum)
                #                         slashCounter += MTnum
                #                         MTnum = 0
                #                     FEN += 'N'
                #                     slashCounter += 1
                #                     if slashCounter >= 8:
                #                         slashCounter -= 8
                #                         FEN += '/'
                #             else:
                #                 if MTnum != 0:
                #                     FEN += str(MTnum)
                #                     slashCounter += MTnum
                #                     MTnum = 0
                #                 FEN += 'R'
                #                 slashCounter += 1
                #                 if slashCounter >= 8:
                #                     slashCounter -= 8
                #                     FEN += '/'
                #         else:
                #             if MTnum != 0:
                #                 FEN += str(MTnum)
                #                 slashCounter += MTnum
                #                 MTnum = 0
                #             FEN += 'r'
                #             slashCounter += 1
                #             if slashCounter >= 8:
                #                 slashCounter -= 8
                #                 FEN += '/'
                #     else:
                #         if MTnum != 0:
                #             FEN += str(MTnum)
                #             slashCounter += MTnum
                #             MTnum = 0
                #         FEN += 'P'
                #         slashCounter += 1
                #         if slashCounter >= 8:
                #             slashCounter -= 8
                #             FEN += '/'
                # else:
                #     if MTnum != 0:
                #         FEN += str(MTnum)
                #         slashCounter += MTnum
                #         MTnum = 0
                #     FEN += 'p'
                #     slashCounter += 1
                #     if slashCounter >= 8:
                #         slashCounter -= 8
                #         FEN += '/'

        print("TIME TO TEMPLATE MATCH", time.time() - templateTime)
        print("TIME AFTER TEMPLATE MATCH", time.time() - startTime)
        # divideCount = 7
        # indexPlace = 0

        # print("Before FEN: " + FEN)
        # print("FEN LENGTH: ", len(FEN))
        # FENList = list(FEN)
        # print("FENList", FENList)
        totalValue = 0
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
        print("TIME TO CREATE FEN:", time.time() - startTime)

        print("Total", totalValue)

        board = chess.Board(fixedfen)

        # break


        engine.position(board)

        # Depth = engine.go(movetime = 50)
        Depth = engine.go(depth = random.randint(6, 8))
        bestMove = str(Depth[0])
        try:
            handler.multipv(2)
            # try:
            move2 = str(handler.info['pv'][2][0])
            move3 = str(handler.info['pv'][3][0])
            print('Best Move', bestMove)
            print('Move 2:', move2)
            print('Move 3:', move3)
            score = handler.info["score"][1].cp
            score2 = handler.info["score"][2].cp
            score3 = handler.info["score"][3].cp
            print('Mainline score:', score, 'Move 2 score:', score2, 'Move 3 score', score3)


            if abs(abs(score) - abs(score2)) >= 80 or abs(abs(score2) - abs(score3)) >= 80:
                time.sleep(random.randint(0, 100) / 100)
                bestMove = bestMove
                print("OBVIOUS MOVE")
            else:
                time.sleep(random.randint(0, 100)/100)
                if 10 <= movecount <= 30:
                    print("Middlegame")
                    time.sleep(random.randint(0, 5))
                moveChoose = random.randint(1, 3)
                if moveChoose == 2:
                    bestMove = move2
                elif moveChoose == 3:
                    bestMove = move3
        except:
            pass
            # if score > 2:
        # except Exception as e:
        #     print('FAILURE:', e)
        #     pass

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
        HalfTwo = bestMove[2:]

        pinkTop = 155 + (boardHeight - pieceHeight * int(HalfOne[1])) + 75
        pinkLeft = 285 + pieceWidth * (ord(HalfOne[0]) - 97) + 2

        # print(pinkLeft, pinkTop)

        greenTop = 155 + (boardHeight - pieceHeight * int(HalfTwo[1])) + 75
        greenLeft = 285 + pieceWidth * (ord(HalfTwo[0]) - 97) + 2

        # print(greenLeft, greenTop)
        print("Time to calculate move:", time.time() - startTime)
        # pyautogui.moveTo(pinkLeft, pinkTop, 0.001)
        # time.sleep(0.1)

        # pyautogui.mouseDown(x=pinkLeft, y=pinkTop)

        clickDown(int(pinkLeft), int(pinkTop))

        # time.sleep(0.1)
        # pyautogui.moveTo(greenLeft,greenTop,0.001)
        time.sleep(0.05)

        clickUp(int(greenLeft), int(greenTop))

        # pyautogui.mouseUp(x=greenLeft, y=greenTop)

        # pyautogui.moveTo(5,5, 0.001)
        win32api.SetCursorPos((5,5))
        movecount += 1
        print("TIME TO RUN", time.time() - startTime)
        print("MoveCount", movecount)
        print('Engine chose', bestMove)
        print('Mainline search depth:', handler.info["depth"])
        print(board)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("EXITING")