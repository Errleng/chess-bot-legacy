from selenium import webdriver
from selenium.common.exceptions import TimeoutException
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


def seleniumCreateBoardCanvas(driver):
    try:
        chessboard = driver.find_element_by_class_name("chessboard-container")
    except Exception as exception:
        print("Failed to draw move")
        print(exception)
        return
    board_side = chessboard.size.get("width")
    piece_side = board_side // 8
    str_board_side = str(board_side)
    board_x = chessboard.location.get("x")
    board_y = chessboard.location.get("y")
    print("Board Dim: " + str_board_side, "Board X: " + str(board_x), "Board Y: " + str(board_y))
    driver.execute_script("window.canvas1 = document.createElement('canvas');"
                           "canvas1.width = window.innerWidth; canvas1.height = window.innerHeight;"
                           "canvas1.style.width = '100%'; canvas1.style.height = '100%';"
                           "canvas1.style.position =  'absolute';"
                           "canvas1.style.left = 0; canvas1.style.top = 0;"
                           "canvas1.style.zIndex = 100000;"
                           "canvas1.style.pointerEvents = 'none';"
                           "document.body.appendChild(canvas1);"
                           "window.context1 = canvas1.getContext('2d');"
                           "context1.globalAlpha = 0.3;"
    
                           "window.canvas2 = document.createElement('canvas');"
                           "canvas2.width = window.innerWidth; canvas2.height = window.innerHeight;"
                           "canvas2.style.width = '100%'; canvas2.style.height = '100%';"
                           "canvas2.style.position =  'absolute';"
                           "canvas2.style.left = 0; canvas2.style.top = 0;"
                           "canvas2.style.zIndex = 100000;"
                           "canvas2.style.pointerEvents = 'none';"
                           "document.body.appendChild(canvas2);"
                           "window.context2 = canvas2.getContext('2d');"
                           "context2.globalAlpha = 0.3;"
                           , chessboard)
    driver.execute_script("window.canvas_arrow = function (context, fromx, fromy, tox, toy){"
                          "var headlen = 20;"
                          "var angle = Math.atan2(toy - fromy, tox - fromx);"
                          "context.beginPath();"
                          "context.lineWidth = 5;"
                          "context.moveTo(fromx, fromy);"
                          "context.lineTo(tox, toy);"
                          "context.moveTo(tox, toy);"
                          "context.lineTo(tox - headlen * Math.cos(angle - Math.PI / 7), toy-headlen * Math.sin(angle - Math.PI / 7));"
                          "context.lineTo(tox - headlen * Math.cos(angle + Math.PI / 7), toy-headlen * Math.sin(angle + Math.PI / 7));"
                          "context.lineTo(tox, toy);"
                          "context.lineTo(tox - headlen * Math.cos(angle - Math.PI / 7), toy-headlen * Math.sin(angle - Math.PI / 7));"
                          "context.stroke();"
                          "context.fillStyle = 'black';"
                          "context.fill();"
                          "}"
                          , chessboard)


def seleniumDrawMove(driver, move, side, colour):
    first_half_move = move[:2]
    second_half_move = move[2:4]
    try:
        chessboard = driver.find_element_by_class_name("chessboard-container")
    except Exception as exception:
        print("Failed to draw move")
        print(exception)
        return
    board_side = chessboard.size.get("width")
    piece_side = board_side // 8
    board_x = chessboard.location.get("x")
    board_y = chessboard.location.get("y")

    if side == "white":
        first_top = (board_side - piece_side * int(first_half_move[1]))
        first_left = piece_side * (ord(first_half_move[0]) - 97)

        second_top = (board_side - piece_side * int(second_half_move[1]))
        second_left = piece_side * (ord(second_half_move[0]) - 97)
    else:
        first_top = (board_side - piece_side * (9 - int(first_half_move[1])))
        first_left = piece_side * (7 - (ord(first_half_move[0]) - 97))

        second_top = (board_side - piece_side * (9 - int(second_half_move[1])))
        second_left = piece_side * (7 - (ord(second_half_move[0]) - 97))

    driver.execute_script("context1.clearRect(0, 0, canvas1.width, canvas1.height);"
                          "canvas1.style.visibility = 'visible';"
                          "context1.globalAlpha = 0.3;"
                          "context1.fillStyle = " + colour + ";"
                          "context1.fillRect(" + str(board_x + first_left) + ", " + str(board_y + first_top) + ", " + str(piece_side) + ", " + str(piece_side) + ");"
                          "context1.fillRect(" + str(board_x + second_left) + ", " + str(board_y + second_top) + ", " + str(piece_side) + ", " + str(piece_side) + ");"
                          , chessboard)


def seleniumDrawMultipleMoves(driver, moves, side, colours, selected_canvas):
    try:
        chessboard = driver.find_element_by_class_name("chessboard-container")
    except Exception as exception:
        print("Failed to draw move")
        print(exception)
        return
    board_side = chessboard.size.get("width")
    piece_side = board_side // 8
    board_x = chessboard.location.get("x")
    board_y = chessboard.location.get("y")

    # coords = []
    arrow_coords = []

    for i in range(len(moves)):
        first_half_move = moves[i][:2]
        second_half_move = moves[i][2:4]

        if side == "white":
            first_top = (board_side - piece_side * int(first_half_move[1]))
            first_left = piece_side * (ord(first_half_move[0]) - 97)

            second_top = (board_side - piece_side * int(second_half_move[1]))
            second_left = piece_side * (ord(second_half_move[0]) - 97)
        else:
            first_top = (board_side - piece_side * (9 - int(first_half_move[1])))
            first_left = piece_side * (7 - (ord(first_half_move[0]) - 97))

            second_top = (board_side - piece_side * (9 - int(second_half_move[1])))
            second_left = piece_side * (7 - (ord(second_half_move[0]) - 97))

        arrow_left1 = str(board_x + first_left + piece_side // 2)
        arrow_top1 = str(board_y + first_top + piece_side // 2)
        arrow_left2 = str(board_x + second_left + piece_side // 2)
        arrow_top2 = str(board_y + second_top + piece_side // 2)

        # first_left = str(board_x + first_left)
        # first_top = str(board_y + first_top)
        # second_left = str(board_x + second_left)
        # second_top = str(board_y + second_top)
        #
        # coords.append((first_left, first_top, second_left, second_top))
        arrow_coords.append((arrow_left1, arrow_top1, arrow_left2, arrow_top2))

    piece_side = str(piece_side)
    current_canvas = selected_canvas
    current_context = current_canvas
    str_current_canvas, str_current_context = str(current_canvas), str(current_context)

    # for i in range(len(coords)):
        # move_coords = coords[i]
        # driver.execute_script("context" + str_current_context + ".fillStyle = " + colours[i] + ";"
        #                       "context" + str_current_context + ".fillRect(" + move_coords[0] + ", " + move_coords[1] + ", " + piece_side + ", " + piece_side + ");"
        #                       "context" + str_current_context + ".fillRect(" + move_coords[2] + ", " + move_coords[3] + ", " + piece_side + ", " + piece_side + ");"
        #                       , chessboard)
    for i in range(len(arrow_coords)):
        move_coords = arrow_coords[i]
        driver.execute_script("context" + str_current_context + ".globalAlpha = " + str(1 - i * 0.3) + ";"
                              "canvas_arrow(context" + str_current_context + ", " + move_coords[0] + ", " + move_coords[1] + ", " + move_coords[2] + ", " + move_coords[3] + ");"
                              , chessboard)
    if selected_canvas == 1:
        driver.execute_script("context2.clearRect(0, 0, canvas2.width, canvas2.height);"
                              "canvas2.style.visibility = 'hidden';"
                              "canvas1.style.visibility = 'visible';"
                              , chessboard)
    elif selected_canvas == 2:
        driver.execute_script("context1.clearRect(0, 0, canvas2.width, canvas2.height);"
                              "canvas1.style.visibility = 'hidden';"
                              "canvas2.style.visibility = 'visible';"
                              , chessboard)
    if selected_canvas == 1:
        return 2
    elif selected_canvas == 2:
        return 1


def seleniumClearCanvas(driver, selected_canvas):
    try:
        chessboard = driver.find_element_by_class_name("chessboard-container")
    except Exception as exception:
        print("Failed to draw move")
        print(exception)
        return
    if selected_canvas == 1:
        driver.execute_script("context1.clearRect(0, 0, canvas1.width, canvas1.height);", chessboard)
    elif selected_canvas == 2:
        driver.execute_script("context2.clearRect(0, 0, canvas2.width, canvas2.height);", chessboard)


def login(driver, username, password):
    name = driver.find_element_by_id("username")
    passwd = driver.find_element_by_id("password")

    name.send_keys(username)
    passwd.send_keys(password)

    driver.find_element_by_name("login").click()
    print("Login complete")


def seleniumFindPlayerColor(driver):
    try:
        driver.find_element_by_css_selector("div[class='board-player bottom white']")
    except:
        return "black"
    return "white"


LAPTOP = False

move_only = True

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


# ENGINE_NAME = "stockfish_9_x64.exe"
# ENGINE_NAME = "Rybkav2.3.2a.mp.x64.exe"

# ENGINE_PATH = r"D:\Documents\SourceTree\ChessBot\Engines\Rodent III"
# ENGINE_NAME = "/rodent_III_x64.exe"

# ENGINE_PATH += "Rodent III - Strangler/"
# ENGINE_NAME = "rodent_III_x64.exe"

ENGINE_PATH += "OpenTal/"
ENGINE_NAME = "opental_x64plain.exe"

engine = chess.uci.popen_engine(ENGINE_PATH + ENGINE_NAME)
engine.uci()
handler = chess.uci.InfoHandler()
engine.info_handlers.append(handler)
print("Loaded", engine.name)


if ENGINE_NAME == "stockfish_9_x64.exe":
    engine.setoption({"Skill Level": 7})
# else:
#     engine.setoption({"UCI_LimitStrength": True})
#     engine.setoption({"UCI_ELO": 1600})


start_url = "https://www.chess.com/login_and_go?returnUrl=https%3A//www.chess.com/register"

browser = webdriver.Firefox()
# browser.set_page_load_timeout(10)

browser.maximize_window()

try:
    browser.get(start_url)
except TimeoutException:
    browser.execute_script("window.stop();")


# username, password = "shortbr", "malifeinc"
# username, password = "rimkill", "failure"
username, password = "breachFirst", "foamfathom"
login(browser, username, password)


try:
    browser.get("https://www.chess.com/live")
except TimeoutException:
    browser.execute_script("window.stop();")


target_element_name = "pgn"
target_class_name = "gotomove"


move_str = "1. "
starting_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# delay = float(input("Enter speed in seconds: ")) * 100
if not move_only:
    player = input("Enter player color: ").lower()
else:
    player = "white"

difficulty = 1
canvas_number = 1

BLACK = "black"
WHITE = "white"

move_count = 1
moves = []
last_move_time = time.time()

# engine.setoption({"MultiPV": 3})
multiPV_available = False

multiPV_move_colours = ["'blue'", "'green'", "'red'"]

seleniumCreateBoardCanvas(browser)

new_position = 2

while True:
    try:
        time.sleep(0.25)
        # player = seleniumFindPlayerColor(browser)
        print("Player is", player)

        got_target = True

        request_time = time.time()

        # print("Current URL in Firefox:", browser.current_url, "Target URL: ", target_url)
        # print("Getting Source")
        # source = browser.page_source

        TURN_BLACK = False
        found_first_move = True
        player = seleniumFindPlayerColor(browser)
        try:
            ending_str = "[id$=gotomoveid_0_1]"
            start_move = browser.find_element_by_css_selector(ending_str)
        except:
            print("Could not get first move")
            found_first_move = False
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
                    new_position = 2
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

        process_start = time.time()
        if found_first_move and len(moves) > 0 and (moves[-1] != "1-0" and moves[-1] != "0-1" and moves[-1] != "1/2-1/2") or len(moves) == 0 and player == WHITE:
            if new_position >= 5:
                print("Position has not changed")
                continue
            else:
                new_position += 1

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
            depth = engine.go(depth=new_position * 2)
            best_move = str(depth[0])
            print("Depth:", new_position * 2)

            if multiPV_available:
                succeed_multiPV = True
                obvious_move = False
                if difficulty == 0:
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
                        elif abs(second_score - third_score) >= 80:
                            print("OBVIOUS MOVE 2")
                            best_move = second_move
                            obvious_move = True
                        else:
                            move_chosen = random.randint(1, 3)
                            if move_chosen == 2:
                                best_move = second_move
                            elif move_chosen == 3:
                                best_move = third_move
                    except Exception as e:
                        print("MultiPV exception:", e)
                        print(handler.info)
                        succeed_multiPV = False
                        pass

            if not move_only and len(moves) > 1:
                if len(moves) < 10:
                    time.sleep(random.uniform(0.1, 1))
                else:
                    time_diff = abs(time.time() - last_move_time - 1)
                    print("Last move time:", time_diff)
                    if time_diff > 15:
                        time_diff = 15
                    sleep_time = random.uniform(time_diff / 5, time_diff / 2)
                    time.sleep(sleep_time)

            # print("Time to calculate move:", time.time() - calculate_move)

            if not move_only:
                # makeMove(best_move, player)
                print("Best Move:", best_move)
                try:
                    print("Evaluation:", handler.info["score"][1].cp)
                except Exception as e:
                    print("Evaluation exception:", e)
                seleniumMakeMove(browser, best_move, player)
            else:
                if multiPV_available:
                    try:
                        handler.multipv(2)
                        multiPV_moves = []
                        multiPV_moves.append(best_move)
                        multiPV_moves.append(str(handler.info["pv"][2][0]))
                        multiPV_moves.append(str(handler.info["pv"][3][0]))

                        print("Moves")
                        for move in multiPV_moves:
                            print(move, end=" ")
                        print()

                        scores = []
                        for i in range(1, 4):
                            scores.append(handler.info["score"][i].cp)
                        print("Scores")
                        for score in scores:
                            print(score, end=" ")
                        print()
                        canvas_number = seleniumDrawMultipleMoves(browser, multiPV_moves, player, multiPV_move_colours, canvas_number)
                    except Exception as e:
                        seleniumDrawMove(browser, best_move, player, "'blue'")
                        print("MultiPV failed for move_only")
                        print(e)
                else:
                    seleniumDrawMove(browser, best_move, player, "'blue'")
            last_move_time = time.time()
        else:
            print("Failed to find any moves")
            # delay = float(input("Enter speed in seconds: ")) * 100
            if not move_only:
                player = input("Enter player color: ").lower()
            else:
                player = seleniumFindPlayerColor(browser)
            print("Player is", player)
            move_count = 1
            moves = []

            print("Duration of processing:", time.time() - process_start)
    except Exception as exception:
        print("Loop Exception:", exception)
        print("Moves:", moves)
        move_count = 1
        moves = []
