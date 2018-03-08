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
        first_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * int(first_half_move[1])) + PIECE_DIM//2
        first_left = LEFT_OFFSET + PIECE_DIM * (ord(first_half_move[0]) - 97) + PIECE_DIM//2

        second_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * int(second_half_move[1])) + PIECE_DIM//2
        second_left = LEFT_OFFSET + PIECE_DIM * (ord(second_half_move[0]) - 97) + PIECE_DIM//2
    else:
        first_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * (9 - int(first_half_move[1]))) + PIECE_DIM//2
        first_left = LEFT_OFFSET + PIECE_DIM * (7 - (ord(first_half_move[0]) - 97)) + PIECE_DIM//2

        second_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * (9 - int(second_half_move[1]))) + PIECE_DIM//2
        second_left = LEFT_OFFSET + PIECE_DIM * (7 - (ord(second_half_move[0]) - 97)) + PIECE_DIM//2

    clickDown(int(first_left), int(first_top))

    time.sleep(0.1)

    clickUp(int(second_left), int(second_top))


def seleniumMakeMove(driver, move, side):
    first_half_move = move[:2]
    second_half_move = move[2:4]
    try:
        chessboard = driver.find_element_by_class_name("chessboard-container")
    except Exception as exception:
        print("Failed to make move")
        print(exception)
        return

    action = webdriver.ActionChains(driver)
    board_side = chessboard.size.get("width")
    piece_side = board_side//8

    if side == "white":
        first_top = (board_side - piece_side * int(first_half_move[1])) + piece_side//2
        first_left = piece_side * (ord(first_half_move[0]) - 97) + piece_side//2

        second_top = (board_side - piece_side * int(second_half_move[1])) + piece_side//2
        second_left = piece_side * (ord(second_half_move[0]) - 97) + piece_side//2
    else:
        first_top = (board_side - piece_side * (9 - int(first_half_move[1]))) + piece_side//2
        first_left = piece_side * (7 - (ord(first_half_move[0]) - 97)) + piece_side//2

        second_top = (board_side - piece_side * (9 - int(second_half_move[1]))) + piece_side//2
        second_left = piece_side * (7 - (ord(second_half_move[0]) - 97)) + piece_side//2

    action.move_to_element_with_offset(chessboard, first_left, first_top)
    action.click()
    action.move_to_element_with_offset(chessboard, second_left, second_top)
    action.click()
    action.perform()


def login(driver, username, password):
    name = driver.find_element_by_id("username")
    passwd = driver.find_element_by_id("password")

    name.send_keys(username)
    passwd.send_keys(password)

    driver.find_element_by_name("login").click()
    print("Login complete")


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
# ENGINE_NAME = "Rybkav2.3.2a.mp.x64.exe"

engine = chess.uci.popen_engine(ENGINE_PATH + ENGINE_NAME)
engine.uci()

handler = chess.uci.InfoHandler()
engine.info_handlers.append(handler)

print("Loaded", engine.name)

engine.setoption({"MultiPV": 3})

if ENGINE_NAME == "stockfish_9_x64.exe":
    engine.setoption({"Skill Level": 7})
# else:
#     engine.setoption({"UCI_LimitStrength": True})
#     engine.setoption({"UCI_ELO": 1600})

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

login(browser, "breachFirst", "foamfathom")

browser.get("https://www.chess.com/live")

# browser = webdriver.Firefox(executable_path = r"D:/Applications/geckodriver/geckodriver.exe")

target_element_name = "pgn"
target_class_name = "gotomove"

move_str = "1. "
starting_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# delay = float(input("Enter speed in seconds: ")) * 100
player = input("Enter player color: ").lower()

BLACK = "black"
WHITE = "white"

move_count = 1
moves = []
last_move_time = time.time()

while True:
    time.sleep(0.5)

    got_target = True

    request_time = time.time()

    # print("Current URL in Firefox:", browser.current_url, "Target URL: ", target_url)
    # print("Getting Source")
    source = browser.page_source

    TURN_BLACK = False

    while True:
        try:
            # target_element = browser.find_elements_by_class_name(target_class_name)
            # moves = target_element.get_attribute("value")
            # target_element_content = [elem.text for elem in target_element]
            element_str = "[id$=gotomoveid_0_" + str(move_count) + "]"
            target_element = browser.find_element_by_css_selector(element_str)
            target_element_content = target_element.text

            # if got_target:
            if target_element_content != "":
                moves.append(target_element_content)
                move_count += 1
            else:
                TURN_BLACK = True
                break

            # print("GOT VALUE")
            # print
            # print(moves)
            # print(type(moves))
            # print
        except Exception as e:
            # print(e)
            # got_target = False
            break

    # print("Time to get page:", time.time() - request_time)

    # print(source)
    process_start = time.time()
    if len(moves) > 0 and (moves[-1] != "1-0" and moves[-1] != "0-1" and moves[-1] != "1/2-1/2") or len(moves) == 0 and player == WHITE:
        if not move_only:
            if TURN_BLACK and player == WHITE:
                continue
            elif not TURN_BLACK and player == BLACK:
                continue

        # print("Moves")
        # print(moves)

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
        depth = engine.go(depth = 8)
        best_move = str(depth[0])

        succeed_multiPV = True
        obvious_move = False
        try:
            handler.multipv(2)
            second_move = str(handler.info["pv"][2][0])
            third_move = str(handler.info["pv"][3][0])

            first_score = handler.info["score"][1].cp
            second_score = handler.info["score"][2].cp
            third_score = handler.info["score"][3].cp

            if abs(first_score - second_score) >= 80:
                print("OBVIOUS MOVE 1")
                obvious_move = True
            if abs(second_score - third_score) >= 80:
                print("OBVIOUS MOVE 2")
                best_move = second_move
                obvious_move = True
        except Exception as e:
            print("Exception:", e)
            print(handler.info)
            succeed_multiPV = False
            pass

        if len(moves) > 1:
            # if succeed_multiPV and not obvious_move:
            if len(moves) < 10:
                time.sleep(random.uniform(0.1, 1))
            else:
                time_diff = abs(time.time() - last_move_time - 1)
                print("Last move time:", time_diff)
                if time_diff > 15:
                    time_diff = 15
                sleep_time = random.uniform(time_diff / 5, time_diff / 2)
                time.sleep(sleep_time)
            # else:
                # time.sleep(random.uniform(0.1, 2))

        # print("Time to calculate move:", time.time() - calculate_move)
        print("BEST MOVE:", best_move)

        if not move_only:
            # makeMove(best_move, player)

            seleniumMakeMove(browser, best_move, player)

        last_move_time = time.time()
    else:
        print("Failed to find any moves")
        # delay = float(input("Enter speed in seconds: ")) * 100
        player = input("Enter player color: ").lower()
        move_count = 1
        moves = []

        print("Duration of processing:", time.time() - process_start)
