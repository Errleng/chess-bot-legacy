import os
import requests
import chess
import chess.uci
import ftplib
import pyautogui
import pgntofen
from PIL import ImageGrab
from PIL import Image
import numpy as np
import time
import importlib
import random

Go = True
def cmpT(t1, t2):
  return sorted(t1) == sorted(t2)
get1 = requests.get("https://echecservice.000webhostapp.com/color.txt",  headers={'User-Agent':'test'})
read1 = get1.text
SAVE_PATH = "D:/Screenshots/"
safeSleep = random.randint(0, 0)
x = None

if read1 == "WHITE":
    print("Player is: " + read1)
    x = 0
elif read1 == "BLACK":
    print("Player is: " +  read1)
    x = 1

def cmpT(t1, t2):
  return sorted(t1) == sorted(t2)

prevFIRSTX = 0
prevFIRSTY = 0
playSpeed = random.randint(0,1)
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
print("BEGIN")

prevColor = str
prevMoveLen = None

while True:
    get1 = requests.get("https://echecservice.000webhostapp.com/color.txt")
    read1 = get1.text
    movetime = random.randint(250, 4000)
    print("GOT " + read1)
    toMove = None
    castleTrue = ""
    if read1 == "WHITE":
        toMove = ' w '
    elif read1 == "BLACK":
        toMove = ' b '
    importlib.reload(pgntofen)
    if x == 0:
        if read1 == 'WHITE':
            print("PLAYER IS WHITE")
            startTime = time.time()
            importlib.reload(pgntofen)
            pgnConverter = pgntofen.PgnToFen()
            getMoves = requests.get("https://echecservice.000webhostapp.com/moves.txt")

            print("GETMOVES: ", getMoves)
            while getMoves.text == '':
                print("RETURNED EMPTY")
                getMoves = requests.get("https://echecservice.000webhostapp.com/moves.txt")
            PGNMoves = getMoves.text.replace(',', ' ')
            print("MOVES: " + PGNMoves)

            pgnConverter.pgnToFen(PGNMoves.split())
            fen = pgnConverter.getFullFen() + " 0 0"
            # print(fen)
            board = chess.Board(fen)
            handler = chess.uci.InfoHandler()

            engine.info_handlers.append(handler)
            engine.position(board)

            if board.turn:
                print('White to move')

            else:
                print('Black to move')
                continue

            voke = engine.go(ponder=False, movetime=movetime)
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
            time.sleep(0.25)
            pyautogui.mouseDown()
            time.sleep(0.25)
            pyautogui.moveTo(greenLeft, greenTop)
            time.sleep(0.25)
            pyautogui.mouseUp()
        else:
            print("OPPONENT IS " + read1)
            # time.sleep(playSpeed)

    if x == 1:
        if read1 == 'BLACK':
            # print("PLAYER IS BLACK")
            startTime = time.time()
            importlib.reload(pgntofen)
            pgnConverter = pgntofen.PgnToFen()
            getMoves = requests.get("https://echecservice.000webhostapp.com/moves.txt")

            print("GETMOVES: ", getMoves)
            while getMoves.text == '':
                print("RETURNED EMPTY")
                getMoves = requests.get("https://echecservice.000webhostapp.com/moves.txt")
            PGNMoves = getMoves.text.replace(',', ' ')
            print("MOVES: " + getMoves.text)

            pgnConverter.pgnToFen(PGNMoves.split())
            fen = pgnConverter.getFullFen() + " 0 0"
            # print(fen)
            board = chess.Board(fen)
            handler = chess.uci.InfoHandler()


            engine.info_handlers.append(handler)
            engine.position(board)

            if board.turn:
                print('White to move')
                continue
            else:
                print('Black to move')

            voke = engine.go(ponder=False, movetime=movetime)
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
            time.sleep(0.25)
            pyautogui.mouseDown()
            time.sleep(0.25)
            pyautogui.moveTo(greenLeft, greenTop)
            time.sleep(0.25)
            pyautogui.mouseUp()
        else:
            print("OPPONENT IS " + read1)
            # time.sleep(playSpeed)
