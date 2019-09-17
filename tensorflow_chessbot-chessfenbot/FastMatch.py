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
import os

SAVE_PATH = "D:/Screenshots/"
enginePath = 'C:/Users/Recursor/Desktop/BACKUP/Engines/'
engine = chess.uci.popen_engine(enginePath + 'stockfish-8-win/Windows/stockfish_8_x64.exe')
engine.uci()

def clickDown(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)

def clickUp(x,y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def rgbImgTM(imagePath, templatePath):
    global maximum_Val
    img = cv2.imread(imagePath)
    # img = imagePath
    temp = cv2.imread(templatePath)
    # temp = templatePath
    w, h = temp.shape[:-1]

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


crop_img = np.array(ImageGrab.grab(bbox=(283, 156, 1099, 972)))
resized = imutils.resize(crop_img, height = 200)

print('Dimensions', resized.shape)
boardDim = resized.shape[0]
pieceDim = resized.shape[0]/8
print(boardDim)
print(pieceDim)

widthArray = [1, 2, 3, 4, 5, 6, 7, 8]
lengthArray = widthArray

lower = np.array([0, 0, 0])
upper = np.array([50, 50, 50])

chessBoard = np.zeros((8,8), dtype=int)
prevBoard = chessBoard

Image.fromarray(resized, 'RGB').save(SAVE_PATH + 'Pieces/croppedBoard.png')
os.system('D:/Applications/Anaconda3-4.4.0/envs/tensorflow/python.exe tensorflow_chessbot.py --filepath D:/Screenshots/Pieces/croppedBoard.png')

file = open("C:/Users/Recursor/Desktop/BACKUP/FEN/fen.txt", 'r')
fen = file.read()
file.close()

cropped_color_black = np.array(ImageGrab.grab(bbox=(895, 105, 945, 146)))
cropped_color_white = np.array(ImageGrab.grab(bbox=(895, 984, 950, 1026)))


resized_crop_black = imutils.resize(cropped_color_black, width=52)
resized_crop_white = imutils.resize(cropped_color_white, width=52)

Image.fromarray(resized_crop_black, 'RGB').save(SAVE_PATH + 'croppedBlack.jpg')
Image.fromarray(resized_crop_white, 'RGB').save(SAVE_PATH + 'croppedWhite.jpg')

returnBlack = rgbImgTM(SAVE_PATH + 'croppedBlack.jpg', 'D:/Screenshots/Back/BlackTimerGo.jpg')
returnWhite = rgbImgTM(SAVE_PATH + 'croppedWhite.jpg', 'D:/Screenshots/Back/WhiteTimerGo.jpg')

toMove = ''
if returnBlack > returnWhite:
    if returnBlack < 0.9:
        toMove = 'w'
    print("Black to Move with", round(returnBlack * 100, 2), "% confidence")
    toMove = 'b'
elif returnWhite > returnBlack:
    if returnWhite < 0.9:
        toMove = 'b'
    print("White to Move with", round(returnWhite * 100, 2), "% confidence")
    toMove = 'w'
else:
    toMove = 'w'

fen += ' ' + toMove + ' - - 0 0'
print('final', fen)
board = chess.Board()
board.set_fen(fen)
print(board)

player = input('Enter player here: ')
runOnce = 0
prevColor = ''

engine.position(board)
bestMove = engine.go(movetime=100)
print(bestMove)
bestMove = str(bestMove[0])


HalfOne = bestMove[:2]
HalfTwo = bestMove[2:]

boardHeight = 816
pieceHeight = 816/8
pieceWidth = 816/8

pinkTop = 155 + (boardHeight - pieceHeight * int(HalfOne[1])) + 75
pinkLeft = 285 + pieceWidth * (ord(HalfOne[0]) - 97) + 2

greenTop = 155 + (boardHeight - pieceHeight * int(HalfTwo[1])) + 75
greenLeft = 285 + pieceWidth * (ord(HalfTwo[0]) - 97) + 2

clickDown(int(pinkLeft), int(pinkTop))

time.sleep(1)

clickUp(int(greenLeft), int(greenTop))

time.sleep(1)

win32api.SetCursorPos((5, 5))

while True:
    print("BEGIN")
    startTime = time.time()

    cropped_color_black = np.array(ImageGrab.grab(bbox=(895, 105, 945, 146)))
    cropped_color_white = np.array(ImageGrab.grab(bbox=(895, 984, 950, 1026)))

    resized_crop_black = imutils.resize(cropped_color_black, width=52)
    resized_crop_white = imutils.resize(cropped_color_white, width=52)

    Image.fromarray(resized_crop_black, 'RGB').save(SAVE_PATH + 'croppedBlack.jpg')
    Image.fromarray(resized_crop_white, 'RGB').save(SAVE_PATH + 'croppedWhite.jpg')

    returnBlack = rgbImgTM(SAVE_PATH + 'croppedBlack.jpg', 'D:/Screenshots/Back/BlackTimerGo.jpg')
    returnWhite = rgbImgTM(SAVE_PATH + 'croppedWhite.jpg', 'D:/Screenshots/Back/WhiteTimerGo.jpg')

    if returnBlack > returnWhite:
        if returnBlack < 0.9:
            toMove = 'w'
        print("Black to Move with", round(returnBlack * 100, 2), "% confidence")
        toMove = 'b'
    elif returnWhite > returnBlack:
        if returnWhite < 0.9:
            toMove = 'b'
        print("White to Move with", round(returnWhite * 100, 2), "% confidence")
        toMove = 'w'

    if toMove == 'b' and player == '0' and runOnce != 0 and prevColor == toMove:
        continue
    if toMove == 'w' and player == '1' and runOnce != 0 and prevColor == toMove:
        continue

    if prevColor != toMove and runOnce != 0:
        print("PAUSING")
        time.sleep(1)
        prevColor = toMove

    crop_img = np.array(ImageGrab.grab(bbox=(283, 156, 1099, 972)))
    resized = imutils.resize(crop_img, height=200)


    chessBoard = np.zeros((8, 8), dtype=int)

    for row in lengthArray:
        for column in widthArray:
            # print(int(pieceDim*(row-1)), int(pieceDim*row), int(pieceDim*(column-1)), int(pieceDim*column))
            img = resized[int(pieceDim*(row-1)): int(pieceDim*row), int(pieceDim*(column-1)): int(pieceDim*column)]

            mask = cv2.inRange(img, lower, upper)
            res = cv2.bitwise_and(img, img, mask = mask)
            # cv2.imshow('img', np.hstack([img, res]))
            # cv2.waitKey(0)
            # cv2.imshow('mask', mask)
            # cv2.waitKey(0)
            detect = cv2.countNonZero(mask)
            if detect > 0:
                # print(detect)
                chessBoard[row-1][column-1] = 1

    print('current\n', chessBoard)
    print('previous\n', prevBoard)
    diffboard = chessBoard - prevBoard
    print('difference\n', chessBoard - prevBoard)
    firstMove = np.where(diffboard == -1)
    secondMove = np.where(diffboard == 1)
    if runOnce == 0:
        runOnce = 1
        prevBoard = chessBoard
    print('Startpos', firstMove[0], firstMove[1])
    print('Finalpos', secondMove[0], secondMove[1])
    # if np.prod(firstMove[0].shape) > 1 or np.prod(secondMove[0].shape) > 1:
    #     continue
    if np.any(firstMove) and np.any(secondMove):
        firstHalf = (chr(firstMove[1] + 97)) + (' '.join(map(str, abs(firstMove[0]-8))))
        secondHalf = (chr(secondMove[1] + 97)) + (' '.join(map(str, abs(secondMove[0] - 8))))
        combined = firstHalf + secondHalf
        print('ToMoves', combined)
        print(board)

        print('before', board.turn)
        if toMove == 'w':
            print('Turn swapped to Black')
            board.turn = False
        elif toMove == 'b':
            print('Turn swapped to White')
            board.turn = True

        print('after', board.turn)
        print(board.fen())
        board.set_fen(board.fen())

        board.push(chess.Move.from_uci(combined))

        print(board.turn)
        print(board.fen())
        print(board)
        # board.set_fen(board.fen())

        engine.position(board)
        bestMove = engine.go(movetime=100)
        print(bestMove)

        bestMove = str(bestMove[0])
        HalfOne = bestMove[:2]
        HalfTwo = bestMove[2:]

        pinkTop = 155 + (boardHeight - pieceHeight * int(HalfOne[1])) + 75
        pinkLeft = 285 + pieceWidth * (ord(HalfOne[0]) - 97) + 2

        greenTop = 155 + (boardHeight - pieceHeight * int(HalfTwo[1])) + 75
        greenLeft = 285 + pieceWidth * (ord(HalfTwo[0]) - 97) + 2
        print("Time to calculate move:", time.time() - startTime)

        clickDown(int(pinkLeft), int(pinkTop))

        time.sleep(0.05)

        clickUp(int(greenLeft), int(greenTop))

        win32api.SetCursorPos((5, 5))
        time.sleep(1)

        # if prevBoard.all() != chessBoard.all():
        print("PREVBOARD")
        prevBoard = chessBoard
    print('RUNTIME:', time.time() - startTime)