import os
import time
import chess
import chess.uci
from PIL import ImageGrab
from PIL import Image

SAVE_PATH = "D:/Screenshots/"
engine = chess.uci.popen_engine('C:/Users/Recursor/Desktop/BACKUP/Engines/Rybkav2.3.2a.mp.x64.exe')
while True:
    ImageGrab.grab().save(SAVE_PATH + "chessScreenshot.jpg", "JPEG")
    print("SAVED SCREENSHOT")
    img = Image.open(SAVE_PATH + "chessScreenshot.jpg")
    print("SCREENSHOTTED")
    os.system(
        'D:/Applications/Anaconda3-4.4.0/envs/tensorflow/python.exe C:/Users/Recursor/Desktop/BACKUP/tensorflow_chessbot-chessfenbot/tensorflow_chessbot.py --filepath D:/Screenshots/chessScreenshot.jpg')

    file = open("C:/Users/Recursor/Desktop/BACKUP/FEN/fen.txt", 'r')
    fen = file.read()
    file.close()

    fixedfen = fen + ' b' + ' -' + ' - ' + '0 0'
    print("FIXED FEN\n" + fixedfen)

    board = chess.Board(fixedfen)
    handler = chess.uci.InfoHandler()
    try:
        engine.info_handlers.append(handler)
        engine.position(board)

        voke = engine.go(ponder=False, movetime = 500)
        pronk = str(voke[0])
        print("Best move: " + pronk)
    except:
        pass



# while True:
#     try:
#         time.sleep(1)
#         os.system("D:\Applications\Python2.7\python.exe screenshot.py")
#
#         file = open('C:/Users/Recursor/Desktop/BACKUP/chesspy-master/fen.txt', 'r')
#         fen = file.read()
#         file.close()
#
#         engine = chess.uci.popen_engine('C:/Users/Recursor/Desktop/BACKUP/Engines/Rybkav2.3.2a.mp.x64.exe')
#         board = chess.Board(fen)
#         handler = chess.uci.InfoHandler()
#
#         engine.info_handlers.append(handler)
#         engine.position(board)
#         voke = engine.go(ponder=False, movetime=500)
#         pronk = str(voke[0])
#         print("Best move: " + pronk)
#         time.sleep(1)
#     except:
#         time.sleep(1)
#         pass
