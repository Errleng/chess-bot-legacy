from selenium import webdriver
import time
import random
import win32api
import win32con

import chess.uci

global BOARD_DIM, PIECE_DIM

def clickDown(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def clickUp(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def makeMove(move, side):
    first_half_move = move[:2]
    second_half_move = move[2:4]

    if side == "white":
        first_top = 160 + (BOARD_DIM - PIECE_DIM * int(first_half_move[1])) + 50
        first_left = 285 + PIECE_DIM * (ord(first_half_move[0]) - 97) + 50

        second_top = 160 + (BOARD_DIM - PIECE_DIM * int(second_half_move[1])) + 50
        second_left = 285 + PIECE_DIM * (ord(second_half_move[0]) - 97) + 50
    else:
        first_top = 160 + (BOARD_DIM - PIECE_DIM * (9 - int(first_half_move[1]))) + 50
        first_left = 285 + PIECE_DIM * (7 - (ord(first_half_move[0]) - 97)) + 50

        second_top = 160 + (BOARD_DIM - PIECE_DIM * (9 - int(second_half_move[1]))) + 50
        second_left = 285 + PIECE_DIM * (7 - (ord(second_half_move[0]) - 97)) + 50

    clickDown(int(first_left), int(first_top))

    time.sleep(0.1)

    clickUp(int(second_left), int(second_top))

LAPTOP = False

if LAPTOP:
    BOARD_DIM = 498
    PIECE_DIM = BOARD_DIM // 8
else:
    BOARD_DIM = 808
    PIECE_DIM = BOARD_DIM // 8


start_time = time.time()

ENGINE_PATH = "D:/Documents/SourceTree/ChessBot/Engines/"
ENGINE_NAME = "stockfish_9_x64.exe"

engine = chess.uci.popen_engine(ENGINE_PATH + ENGINE_NAME)
engine.uci()

handler = chess.uci.InfoHandler()
engine.info_handlers.append(handler)

browser = webdriver.Firefox(executable_path = r"D:/Applications/geckodriver/geckodriver.exe")
target_url = "https://www.chess.com/live#g=2656348923"
start_url = "https://www.chess.com/"
browser.get(start_url)
target_element_name = "pgn"
target_class_name = "gotomove"

move_str = "1. "
starting_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

player = input("Enter player color: ").lower()

BLACK = "black"
WHITE = "white"

while True:
    time.sleep(0.25)

    got_target = True

    # print("Current URL in Firefox:", browser.current_url, "Target URL: ", target_url)
    # print("Getting Source")
    source = browser.page_source
    try:
        target_element = browser.find_elements_by_class_name(target_class_name)
        # target_element_content = target_element.get_attribute("value")
        target_element_content = [elem.text for elem in target_element]
    except Exception as e:
        print(e)
        got_target = False
        pass

    # print(source)

    if got_target:
        process_start = time.time()

        # print("GOT VALUE")
        # print
        print(target_element_content)
        # print(type(target_element_content))
        # print

        # index = -1

        # for i in range(len(target_element_content)):
        #     if i + len(move_str) < len(target_element_content):
        #         start_str = ""
        #         for j in range(len(move_str)):
        #             start_str += (target_element_content[i + j])
        #
        #         if start_str == move_str:
        #             # print("FOUND START STR:", start_str, "==", move_str)
        #             index = i + len(move_str)
        #             break

        if len(target_element_content) > 0:
            # move_section = target_element_content[index:]
            #
            # move_section = move_section.replace("\n", " ")
            # # cut_element = cut_element.replace(r"\\", "")
            #
            # # print("Moves Section")
            # # print(move_section)
            #
            # list_moves = move_section.split(" ")
            #
            # for i in range(len(list_moves) - 1, -1, -1):
            #     if list_moves[i].count(".") > 0:
            #         del list_moves[i]
            #
            # del list_moves[-1]

            # print("Moves!")
            # print(list_moves)
            # print("There are", len(list_moves), "moves")

            # if 10 <= len(target_element_content)//2 <= 30:
            #     time.sleep(random.randint(1, 200)/100.0)
            time.sleep(random.randint(0, 25)/100.0)

            if target_element_content[-1] == "1-0" or target_element_content[-1] == "0-1":
                player = input("Enter player color: ").lower()
                continue

            if not target_element_content[-1] == "" and player == BLACK:
                print("Opponent WHITE")
                continue

            if target_element_content[-1] == "" and player == BLACK:
                del target_element_content[-1]
            elif target_element_content[-1] == "" and player == WHITE:
                print("Opponent BLACK")
                continue

            board = chess.Board(starting_FEN)
            calculate_move = time.time()

            try:
                for move in target_element_content:
                    board.push_san(move)
            except Exception as e:
                print(e)
                continue

            print(board)

            engine.position(board)
            depth = engine.go(depth=5)
            best_move = str(depth[0])

            print("Time to calculate move:", time.time() - calculate_move)
            print("BEST MOVE:", best_move)

            makeMove(best_move, player)
        else:
            print("Failed to find any moves")
            player = input("Enter player color: ").lower()

        print("Duration of processing:", time.time() - process_start)

# mesmerFULL
# zunoit
