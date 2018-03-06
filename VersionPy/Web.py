from selenium import webdriver
import time
import random
import win32api
import win32con

import chess.uci

global BOARD_DIM, PIECE_DIM, LEFT_OFFSET, TOP_OFFSET

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
        first_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * int(first_half_move[1])) + 50
        first_left = LEFT_OFFSET + PIECE_DIM * (ord(first_half_move[0]) - 97) + 50

        second_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * int(second_half_move[1])) + 50
        second_left = LEFT_OFFSET + PIECE_DIM * (ord(second_half_move[0]) - 97) + 50
    else:
        first_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * (9 - int(first_half_move[1]))) + 50
        first_left = LEFT_OFFSET + PIECE_DIM * (7 - (ord(first_half_move[0]) - 97)) + 50

        second_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * (9 - int(second_half_move[1]))) + 50
        second_left = LEFT_OFFSET + PIECE_DIM * (7 - (ord(second_half_move[0]) - 97)) + 50

    clickDown(int(first_left), int(first_top))

    time.sleep(0.1)

    clickUp(int(second_left), int(second_top))

LAPTOP = False

move_only = False

if LAPTOP:
    BOARD_DIM = 498
    PIECE_DIM = BOARD_DIM // 8
    TOP_OFFSET = 138
    LEFT_OFFSET = 162
    ENGINE_PATH = "C:/Users/aisae/Documents/Sourcetree/ChessBot/Engines/"
else:
    BOARD_DIM = 808
    PIECE_DIM = BOARD_DIM // 8
    TOP_OFFSET = 160
    LEFT_OFFSET = 285
    ENGINE_PATH = "D:/Documents/SourceTree/ChessBot/Engines/"

start_time = time.time()

ENGINE_NAME = "stockfish_9_x64.exe"

engine = chess.uci.popen_engine(ENGINE_PATH + ENGINE_NAME)
engine.uci()

handler = chess.uci.InfoHandler()
engine.info_handlers.append(handler)

# existing_instance = input("Existing browser instance?: ").lower()
start_url = "https://www.chess.com/login_and_go?returnUrl=https%3A//www.chess.com/register"

# if existing_instance == "yes":
#     with open("selenium_session.txt") as file:
#         file_content = file.readlines()
#     url = file_content[0]
#     session_id = file_content[1]
#     browser = webdriver.Remote(command_executor=url, desired_capabilities={})
#     browser.session_id = session_id
# else:
#     browser = webdriver.Firefox()
#     browser.get(start_url)
#     url = browser.command_executor._url
#     session_id = browser.session_id
#     open("selenium_session.txt", "w").close()
#     with open("selenium_session.txt", "a") as file:
#         file.write(url + "\n")
#         file.write(session_id)

browser = webdriver.Firefox()
browser.get(start_url)

# browser = webdriver.Firefox(executable_path = r"D:/Applications/geckodriver/geckodriver.exe")

target_element_name = "pgn"
target_class_name = "gotomove"

move_str = "1. "
starting_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

delay = float(input("Enter speed in seconds: ")) * 100
player = input("Enter player color: ").lower()

BLACK = "black"
WHITE = "white"

move_count = 1
moves = []

while True:
    time.sleep(1)

    got_target = True

    request_time = time.time()

    # print("Current URL in Firefox:", browser.current_url, "Target URL: ", target_url)
    # print("Getting Source")
    source = browser.page_source
    try:
        # target_element = browser.find_elements_by_class_name(target_class_name)
        # moves = target_element.get_attribute("value")
        # target_element_content = [elem.text for elem in target_element]
        element_str = "[id$=gotomoveid_0_" + str(move_count) + "]"
        target_element = browser.find_element_by_css_selector(element_str)
        target_element_content = target_element.text
    except Exception as e:
        print(e)
        got_target = False
        pass

    print("Time to get page:", time.time() - request_time)

    # print(source)

    if got_target:
        if target_element_content != "":
            moves.append(target_element_content)
            move_count += 1

        # print("GOT VALUE")
        # print
        print(moves)
        # print(type(moves))
        # print

    process_start = time.time()

    if len(moves) > 0 and (moves[-1] != "1-0" and moves[-1] != "0-1" and moves[-1] != "1/2-1/2"):
        time.sleep(random.randint(0, delay)/100.0)

        if len(moves) % 2 == 1 and player == WHITE:
            print("Opponent is Black")
            continue
        elif len(moves) % 2 == 0 and player == BLACK:
            print("Opponent is White")
            continue

        board = chess.Board(starting_FEN)
        calculate_move = time.time()

        try:
            for move in moves:
                board.push_san(move)
        except Exception as e:
            print(e)
            continue

        print(board)

        engine.position(board)
        depth = engine.go(depth=4)
        best_move = str(depth[0])

        print("Time to calculate move:", time.time() - calculate_move)
        print("BEST MOVE:", best_move)

        if not move_only:
            makeMove(best_move, player)
    else:
        print("Failed to find any moves")
        delay = float(input("Enter speed in seconds: ")) * 100
        player = input("Enter player color: ").lower()
        move_count = 1
        moves = []

    print("Duration of processing:", time.time() - process_start)