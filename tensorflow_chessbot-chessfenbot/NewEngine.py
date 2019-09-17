import os
import requests
import chess
import chess.uci
import ftplib
from git import Repo, remote
import time
import random
import numpy as np
from PIL import ImageGrab
from PIL import Image
import pyautogui
import pgntofen

pgnConverter = pgntofen.PgnToFen()
Go = True

get1 = requests.get("https://echecservice.000webhostapp.com/color.txt")
read1 = get1.text

x = None

# session = ftplib.FTP('ftp.spicewebpro.com', 'MOVE@spicewebpro.com', 'Beth1177')

# ftp = ftplib.FTP()
#
# file = open("C:/Users/Recursor/Desktop/BACKUP/Github/index.txt", 'rb')
#
# port = 21
# server = "files.000webhost.com"
# username = 'echecservice'
# password = 'fallacy123'
#
# ftp_connection = ftplib.FTP(server, username, password)
# ftp_connection.cwd("/public_html/")
# ftp_connection.storlines('STOR index.txt', file)
# print("UPDATED")
# file.close()

if read1 == "WHITE":
    print("Player is: " + read1)
    x = 0
elif read1 == "BLACK":
    print("Player is: " +  read1)
    x = 1

SAVE_PATH = "D:/Screenshots/"

playSpeed = random.randint(1, 1)

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

boardDimensions = requests.get('https://echecservice.000webhostapp.com/dimensions.txt')
splitDims = boardDimensions.text.split()
boardWidth = int(splitDims[0])
boardHeight = int(splitDims[1])
pieceHeight = int(boardHeight/8)
pieceWidth = int(boardWidth/8)

move = 'b1c3'
boardOffsets = requests.get('https://echecservice.000webhostapp.com/offset.txt')

Offsets = boardOffsets.text.split()
boardLeftOff = int(Offsets[0])
boardTopOff = int(Offsets[1])

HalfOne = move[:2]
HalfTwo = move[2:]


pinkTop = boardTopOff + (boardHeight - pieceHeight * int(HalfOne[1])) + 100
pinkLeft = boardLeftOff + pieceWidth * (ord(HalfOne[0]) - 97)

print(pinkTop)
print(pinkLeft)


greenTop = boardTopOff + (boardHeight - pieceHeight * int(HalfTwo[1])) + 100
greenLeft = boardLeftOff + pieceWidth * (ord(HalfTwo[0]) - 97)

print(greenTop)
print(greenLeft)

pyautogui.moveTo(pinkLeft, pinkTop)
pyautogui.mouseDown()
time.sleep(1)
pyautogui.moveTo(greenLeft, greenTop)
pyautogui.mouseUp()

# ImageGrab.grab().save(SAVE_PATH + "chessScreenshot.jpg", "JPEG")
# print("SAVED SCREENSHOT")
# img = Image.open(SAVE_PATH + "chessScreenshot.jpg")
# rgb_img = img.convert('RGB')
# r, g, b = rgb_img.getpixel((367, 948))
# print(r, g, b)
#
# check = (79, 113, 151)
#
# if (r, g, b) == check:
#     print("PLAYER IS WHITE")
#     x = 0
# elif (r, g, b) != check:
#     print("PLAYER IS BLACK")
#     x = 1
canCastleKing = True
canCastleQueen = True

engine = chess.uci.popen_engine('C:/Users/Recursor/Desktop/BACKUP/Engines/Rybkav2.3.2a.mp.x64.exe')

# while Go == True:
#     # time.sleep(playSpeed)
#     get1 = requests.get("https://echecservice.000webhostapp.com/color.txt")
#     read1 = get1.text
#
#     toMove = None
#
#     castleTrue = ""
#
#     if read1 == "WHITE":
#         toMove = ' w '
#     elif read1 == "BLACK":
#         toMove = ' b '
#
#
#
#     if read1 == 'WHITE':
#         if x == 0:
#
#
#             if canCastleQueen == True and canCastleKing == True:
#                 castleTrue = 'KQ'
#             elif canCastleQueen == True:
#                 castleTrue = 'Q'
#             elif canCastleKing == True:
#                 castleTrue = 'K'
#             else:
#                 castleTrue = '-'
#
#             print(castleTrue)
#
#             ImageGrab.grab().save(SAVE_PATH + "chessScreenshot.jpg", "JPEG")
#             print("SAVED SCREENSHOT")
#             img = Image.open(SAVE_PATH + "chessScreenshot.jpg")
#             print("SCREENSHOTTED")
#             os.system(
#                 'D:/Applications/Anaconda3-4.4.0/envs/tensorflow/python.exe tensorflow_chessbot.py --filepath D:/Screenshots/chessScreenshot.jpg')
#
#             file = open("C:/Users/Recursor/Desktop/BACKUP/FEN/fen.txt", 'r')
#             fen = file.read()
#             file.close()
#
#             # repo = Repo.clone_from('https://github.com/JayEffKayZed/JayEffKayZed.github.io.git', 'C:/Users/Recursor/Desktop/BACKUP/Github')
#
#             fixedfen = fen + toMove + castleTrue + ' - ' + '0 0'
#             print("FIXED FEN\n" + fixedfen)
#             board = chess.Board(fixedfen)
#             handler = chess.uci.InfoHandler()
#
#             engine.info_handlers.append(handler)
#             engine.position(board)
#
#             if board.turn:
#                 print('White to move')
#             else:
#                 print('Black to move')
#
#             voke = engine.go(ponder=False, depth=8)
#             pronk = str(voke[0])
#             FirstHalf = pronk[:2]
#             SecondHalf = pronk[2:]
#             print("Best Move: " + FirstHalf + " " + SecondHalf)
#
#             if "k" or "K" in FirstHalf:
#                 canCastleKing = False
#                 canCastleQueen = False
#
#             # if "k" or "K" in SecondHalf:
#             #     canCastleKing = False
#             #     canCastleQueen = False
#
#             if "rh" or "Rh" in FirstHalf:
#                 canCastleQueen = False
#
#             if "ra" or "Ra" in FirstHalf:
#                 canCastleKing = False
#
#             if pronk == "e1g1":
#                 canCastleKing = False
#             if pronk == "e1c1":
#                 canCastleQueen = False
#
#
#             changefile = open('C:/Users/Recursor/Desktop/BACKUP/Github/index.txt', 'w')
#             # changefile.write("<p>" + FirstHalf + " " + SecondHalf + "</p>")
#             changefile.write(pronk)
#             changefile.close()
#             #
#             # print("File updated")
#             #
#             # repo_dir = 'C:/Users/Recursor/Desktop/BACKUP/Github'
#             # repo = Repo(repo_dir)
#             # file_list = [
#             #     'index.txt',
#             # ]
#             # commit_message = 'Update1'
#             # repo.index.add(file_list)
#             # repo.index.commit(commit_message)
#             # origin = repo.remote('origin')
#             # origin.push()
#             #
#             # print("Pushed Update")
#
#             #######################################
#
#             # ftp = ftplib.FTP()
#             #
#             # file1 = open("C:/Users/Recursor/Desktop/BACKUP/Github/index.txt", 'rb')
#             #
#             # port = 21
#             # server = "files.000webhost.com"
#             # username = 'echecservice'
#             # password = 'fallacy123'
#             #
#             # ftp_connection = ftplib.FTP(server, username, password)
#             # ftp_connection.cwd("/public_html/")
#             # # ftp_connection.delete('index.txt')
#             # # print("DELETED")
#             # ftp_connection.storlines('STOR index.txt', file1)
#             # print("UPDATED")
#             # file1.close()
#
#             time.sleep(2)
#
#             ImageGrab.grab().save(SAVE_PATH + "chessScreenshot.jpg", "JPEG")
#             print("SAVED SCREENSHOT")
#             img = Image.open(SAVE_PATH + "chessScreenshot.jpg")
#             print("SCREENSHOTTED")
#
#             pinkzip = find_rgb(img, 238, 158, 147)
#             redzip = find_rgb(img, 160, 99, 117)
#             dgzip = find_rgb(img, 102, 180, 104)
#             lgzip = find_rgb(img, 181, 240, 134)
#
#             FIRST = None
#             SECOND = None
#
#             if pinkzip is None and redzip is not None:
#                 FIRSTX = redzip[0][0]
#                 FIRSTY = redzip[0][1]
#                 print("RED")
#                 # print(redzip)
#                 time.sleep(1)
#             elif redzip is None and pinkzip is not None:
#                 FIRSTX = pinkzip[0][0]
#                 FIRSTY = pinkzip[0][1]
#                 print("PINK")
#                 # print(pinkzip)
#                 time.sleep(1)
#             if dgzip is None and lgzip is not None:
#                 SECONDX = lgzip[0][0]
#                 SECONDY = lgzip[0][1]
#                 print("LG")
#                 # print(lgzip)
#                 time.sleep(1)
#             elif lgzip is None and dgzip is not None:
#                 SECONDX = dgzip[0][0]
#                 SECONDY = dgzip[0][1]
#                 print("DG")
#                 # print(dgzip)
#                 time.sleep(1)
#
#             print("FIRSTS", FIRSTX, FIRSTY)
#             print("SECONDS", SECONDX, SECONDY)
#
#             print("FIRST:", FIRST)
#             print("SECOND", SECOND)
#
#             pyautogui.moveTo(SECONDY, SECONDX)
#
#             pyautogui.mouseDown()
#             print("ONE")
#             time.sleep(0.5)
#             pyautogui.moveTo(FIRSTY, FIRSTX)
#             pyautogui.mouseUp()
#             print("TWO")
#             time.sleep(3)
#         else:
#             print("OPPONENT IS " + read1)
#             time.sleep(playSpeed)
#
#     if read1 == "BLACK":
#         if x == 1:
#
#             if canCastleQueen == True and canCastleKing == True:
#                 castleTrue = 'kq'
#             elif canCastleQueen == True:
#                 castleTrue = 'q'
#             elif canCastleKing == True:
#                 castleTrue = 'k'
#             else:
#                 castleTrue = '-'
#
#             print(castleTrue)
#
#
#             ImageGrab.grab().save(SAVE_PATH + "chessScreenshot.jpg", "JPEG")
#             print("SAVED SCREENSHOT")
#             img = Image.open(SAVE_PATH + "chessScreenshot.jpg")
#             print("SCREENSHOTTED")
#             os.system(
#                 'D:/Applications/Anaconda3-4.4.0/envs/tensorflow/python.exe tensorflow_chessbot.py --filepath D:/Screenshots/chessScreenshot.jpg')
#
#             file = open("C:/Users/Recursor/Desktop/BACKUP/FEN/fen.txt", 'r')
#             fen = file.read()
#             file.close()
#
#             # repo = Repo.clone_from('https://github.com/JayEffKayZed/JayEffKayZed.github.io.git', 'C:/Users/Recursor/Desktop/BACKUP/Github')
#
#             fixedfen = fen + toMove + castleTrue +  ' - ' + '0 0'
#             print("FIXED FEN\n" + fixedfen)
#             board = chess.Board(fixedfen)
#             handler = chess.uci.InfoHandler()
#
#
#             engine.info_handlers.append(handler)
#             engine.position(board)
#
#             if board.turn:
#                 print('White to move')
#             else:
#                 print('Black to move')
#
#             voke = engine.go(ponder=False, depth=8)
#             pronk = str(voke[0])
#             FirstHalf = pronk[:2]
#             SecondHalf = pronk[2:]
#             print("Best Move: " + FirstHalf + " " + SecondHalf)
#
#             if "k" or "K" in FirstHalf:
#                 canCastleKing = False
#                 canCastleQueen = False
#
#             # if "k" or "K" in SecondHalf:
#             #     canCastleKing = False
#             #     canCastleQueen = False
#
#             if "rh" or "Rh" in FirstHalf:
#                 canCastleKing = False
#
#             if "ra" or "Ra" in FirstHalf:
#                 canCastleQueen = False
#
#             if pronk == "e8g8":
#                 canCastleKing = False
#             if pronk == "e8c8":
#                 canCastleQueen = False
#
#             changefile = open('C:/Users/Recursor/Desktop/BACKUP/Github/index.txt', 'w')
#             # changefile.write("<p>" + FirstHalf + " " + SecondHalf + "</p>")
#             changefile.write(pronk)
#             changefile.close()
#             #
#             # print("File updated")
#             #
#             # repo_dir = 'C:/Users/Recursor/Desktop/BACKUP/Github'
#             # repo = Repo(repo_dir)
#             # file_list = [
#             #     'index.txt',
#             # ]
#             # commit_message = 'Update1'
#             # repo.index.add(file_list)
#             # repo.index.commit(commit_message)
#             # origin = repo.remote('origin')
#             # origin.push()
#             #
#             # print("Pushed Update")
#
#             #######################################
#
#             # ftp = ftplib.FTP()
#             #
#             # file1 = open("C:/Users/Recursor/Desktop/BACKUP/Github/index.txt", 'rb')
#             #
#             # port = 21
#             # server = "files.000webhost.com"
#             # username = 'echecservice'
#             # password = 'fallacy123'
#             #
#             # ftp_connection = ftplib.FTP(server, username, password)
#             # ftp_connection.cwd("/public_html/")
#             # # ftp_connection.delete('index.txt')
#             # # print("DELETED")
#             # ftp_connection.storlines('STOR index.txt', file1)
#             # print("UPDATED")
#             # file1.close()
#
#             time.sleep(2)
#
#             ImageGrab.grab().save(SAVE_PATH + "chessScreenshot.jpg", "JPEG")
#             print("SAVED SCREENSHOT")
#             img = Image.open(SAVE_PATH + "chessScreenshot.jpg")
#             print("SCREENSHOTTED")
#
#             pinkzip = find_rgb(img, 238, 158, 147)
#             redzip = find_rgb(img, 160, 99, 117)
#             dgzip = find_rgb(img, 102, 180, 104)
#             lgzip = find_rgb(img, 181, 240, 134)
#
#             FIRST = None
#             SECOND = None
#
#             if pinkzip is None and redzip is not None:
#                 FIRSTX = redzip[0][0]
#                 FIRSTY = redzip[0][1]
#                 print("RED")
#                 # print(redzip)
#                 time.sleep(1)
#             elif redzip is None and pinkzip is not None:
#                 FIRSTX = pinkzip[0][0]
#                 FIRSTY = pinkzip[0][1]
#                 print("PINK")
#                 # print(pinkzip)
#                 time.sleep(1)
#             if dgzip is None and lgzip is not None:
#                 SECONDX = lgzip[0][0]
#                 SECONDY = lgzip[0][1]
#                 print("LG")
#                 # print(lgzip)
#                 time.sleep(1)
#             elif lgzip is None and dgzip is not None:
#                 SECONDX = dgzip[0][0]
#                 SECONDY = dgzip[0][1]
#                 print("DG")
#                 # print(dgzip)
#                 time.sleep(1)
#
#             print("FIRSTS", FIRSTX, FIRSTY)
#             print("SECONDS", SECONDX, SECONDY)
#
#             print("FIRST:", FIRST)
#             print("SECOND", SECOND)
#
#             pyautogui.moveTo(SECONDY, SECONDX)
#
#             pyautogui.mouseDown()
#             print("ONE")
#             time.sleep(0.5)
#             pyautogui.moveTo(FIRSTY, FIRSTX)
#             pyautogui.mouseUp()
#             print("TWO")
#             time.sleep(3)
#         else:
#             print("OPPONENT IS " + read1)
#             time.sleep(playSpeed)




