import os
import requests
import chess
import chess.uci
import ftplib
import time
import random
import numpy as np
from PIL import ImageGrab
from PIL import Image
import pyautogui
import pgntofen
import pgntofen
import importlib

get1 = requests.get("https://echecservice.000webhostapp.com/color.txt")
read1 = get1.text

x = None

if read1 == "WHITE":
    print("Player is: " + read1)
    x = 0
elif read1 == "BLACK":
    print("Player is: " +  read1)
    x = 1

x = 0

SAVE_PATH = "D:/Screenshots/"

canCastleKing = True
canCastleQueen = True

playSpeed = random.randint(1, 1)
boardDimensions = requests.get('https://echecservice.000webhostapp.com/dimensions.txt')
engine = chess.uci.popen_engine('C:/Users/Recursor/Desktop/BACKUP/Engines/Rybkav2.3.2a.mp.x64.exe')
splitDims = boardDimensions.text.split()
boardWidth = int(splitDims[0])
boardHeight = int(splitDims[1])
pieceHeight = int(boardHeight / 8)
pieceWidth = int(boardWidth / 8)
boardOffsets = requests.get('https://echecservice.000webhostapp.com/offset.txt')
Offsets = boardOffsets.text.split()
boardLeftOff = int(Offsets[0])
boardTopOff = int(Offsets[1])
print(boardTopOff)
while True:
    # time.sleep(playSpeed)
    get1 = requests.get("https://echecservice.000webhostapp.com/color.txt")
    read1 = get1.text

    toMove = None

    castleTrue = ""

    if read1 == "WHITE":
        toMove = ' w '
    elif read1 == "BLACK":
        toMove = ' b '


    read1 = "WHITE"
    if read1 == 'WHITE':
        if x == 0:
            if canCastleQueen == True and canCastleKing == True:
                castleTrue = 'KQ'
            elif canCastleQueen == True:
                castleTrue = 'Q'
            elif canCastleKing == True:
                castleTrue = 'K'
            else:
                castleTrue = '-'

            print(castleTrue)

            ImageGrab.grab().save(SAVE_PATH + "chessScreenshot.jpg", "JPEG")
            print("SAVED SCREENSHOT")
            img = Image.open(SAVE_PATH + "chessScreenshot.jpg")
            print("SCREENSHOTTED")
            os.system(
                'D:/Applications/Anaconda3-4.4.0/envs/tensorflow/python.exe tensorflow_chessbot.py --filepath D:/Screenshots/chessScreenshot.jpg')

            file = open("C:/Users/Recursor/Desktop/BACKUP/FEN/fen.txt", 'r')
            fen = file.read()
            file.close()

            # repo = Repo.clone_from('https://github.com/JayEffKayZed/JayEffKayZed.github.io.git', 'C:/Users/Recursor/Desktop/BACKUP/Github')

            fixedfen = fen + toMove + castleTrue + ' - ' + '0 0'
            print("FIXED FEN\n" + fixedfen)
            board = chess.Board(fixedfen)
            handler = chess.uci.InfoHandler()

            engine.info_handlers.append(handler)
            engine.position(board)

            if board.turn:
                print('White to move')
            else:
                print('Black to move')
                continue

            voke = engine.go(ponder=False, movetime = 500)
            pronk = str(voke[0])
            print("Best move: " + pronk)



            move = pronk

            HalfOne = move[:2]
            HalfTwo = move[2:]

            pinkTop = boardTopOff + (boardHeight - pieceHeight * int(HalfOne[1])) + 100
            pinkLeft = boardLeftOff + pieceWidth * (ord(HalfOne[0]) - 97) + 2

            print(pinkTop)
            print(pinkLeft)

            greenTop = boardTopOff + (boardHeight - pieceHeight * int(HalfTwo[1])) + 100
            greenLeft = boardLeftOff + pieceWidth * (ord(HalfTwo[0]) - 97) + 2

            print(greenTop)
            print(greenLeft)

            pyautogui.moveTo(pinkLeft, pinkTop)
            time.sleep(0.2)
            pyautogui.mouseDown()
            time.sleep(0.2)
            pyautogui.moveTo(greenLeft, greenTop)
            time.sleep(0.2)
            pyautogui.mouseUp()
        else:
            print("OPPONENT IS " + read1)
            time.sleep(playSpeed)

    if read1 == 'BLACK':
        if x == 1:
            if canCastleQueen == True and canCastleKing == True:
                castleTrue = 'kq'
            elif canCastleQueen == True:
                castleTrue = 'q'
            elif canCastleKing == True:
                castleTrue = 'k'
            else:
                castleTrue = '-'

            print(castleTrue)

            ImageGrab.grab().save(SAVE_PATH + "chessScreenshot.jpg", "JPEG")
            print("SAVED SCREENSHOT")
            img = Image.open(SAVE_PATH + "chessScreenshot.jpg")
            print("SCREENSHOTTED")
            os.system(
                'D:/Applications/Anaconda3-4.4.0/envs/tensorflow/python.exe tensorflow_chessbot.py --filepath D:/Screenshots/chessScreenshot.jpg')

            file = open("C:/Users/Recursor/Desktop/BACKUP/FEN/fen.txt", 'r')
            fen = file.read()
            file.close()

            # repo = Repo.clone_from('https://github.com/JayEffKayZed/JayEffKayZed.github.io.git', 'C:/Users/Recursor/Desktop/BACKUP/Github')

            fixedfen = fen + toMove + castleTrue + ' - ' + '0 0'
            print("FIXED FEN\n" + fixedfen)
            board = chess.Board(fixedfen)
            handler = chess.uci.InfoHandler()

            engine.info_handlers.append(handler)
            engine.position(board)

            if board.turn:
                print('White to move')
                continue
            else:
                print('Black to move')

            voke = engine.go(ponder=False, movetime = 500)
            pronk = str(voke[0])
            print("Best move: " + pronk)

            splitDims = boardDimensions.text.split()
            boardWidth = int(splitDims[0])
            boardHeight = int(splitDims[1])
            pieceHeight = int(boardHeight / 8)
            pieceWidth = int(boardWidth / 8)

            move = pronk

            HalfOne = move[:2]
            HalfTwo = move[2:]

            pinkTop = boardTopOff + (boardHeight - pieceHeight * int(HalfOne[1])) + 100
            pinkLeft = boardLeftOff + pieceWidth * (ord(HalfOne[0]) - 97) + 2

            print(pinkTop)
            print(pinkLeft)

            greenTop = boardTopOff + (boardHeight - pieceHeight * int(HalfTwo[1])) + 100
            greenLeft = boardLeftOff + pieceWidth * (ord(HalfTwo[0]) - 97) + 2

            print(greenTop)
            print(greenLeft)

            pyautogui.moveTo(pinkLeft, pinkTop)
            pyautogui.mouseDown()
            time.sleep(1)
            pyautogui.moveTo(greenLeft, greenTop)
            pyautogui.mouseUp()
        else:
            print("OPPONENT IS " + read1)
            time.sleep(playSpeed)