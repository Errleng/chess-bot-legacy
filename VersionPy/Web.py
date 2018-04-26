from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import random
import win32api
import win32con

import chess.uci
import traceback

global BOARD_DIM, PIECE_DIM, LEFT_OFFSET, TOP_OFFSET
global engine, handler


def ClickDown(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def ClickUp(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def MakeMove(self, move, side):
    first_half_move = move[:2]
    second_half_move = move[2:4]

    if side == "white":
        first_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * int(first_half_move[1])) + PIECE_DIM // 2
        first_left = LEFT_OFFSET + PIECE_DIM * (ord(first_half_move[0]) - 97) + PIECE_DIM // 2

        second_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * int(second_half_move[1])) + PIECE_DIM // 2
        second_left = LEFT_OFFSET + PIECE_DIM * (ord(second_half_move[0]) - 97) + PIECE_DIM // 2
    else:
        first_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * (9 - int(first_half_move[1]))) + PIECE_DIM // 2
        first_left = LEFT_OFFSET + PIECE_DIM * (7 - (ord(first_half_move[0]) - 97)) + PIECE_DIM // 2

        second_top = TOP_OFFSET + (BOARD_DIM - PIECE_DIM * (9 - int(second_half_move[1]))) + PIECE_DIM // 2
        second_left = LEFT_OFFSET + PIECE_DIM * (7 - (ord(second_half_move[0]) - 97)) + PIECE_DIM // 2

    ClickDown(int(first_left), int(first_top))

    time.sleep(0.1)

    ClickUp(int(second_left), int(second_top))

class SeleniumChess(object):
    def __init__(self, driver=None):
        self.driver = driver

    def GetElements(self):
        if self.driver is not None:
            try:
                self.chessboard = self.driver.find_element_by_class_name("chessboard-container")
            except Exception as e:
                print("Error when finding chessboard:", e)
                return

            # Initialize ActionChains
            self.action_chains = webdriver.ActionChains(self.driver)
            self.board_dim = self.chessboard.size.get("width")
            self.piece_dim = self.board_dim // 8
            self.board_x = self.chessboard.location.get("x")
            self.board_y = self.chessboard.location.get("y")
        else:
            print("No browser driver")

    def CreateBoardCanvas(self):
        print("Board Dim: " + str(self.board_dim), "Board X: " + str(self.board_x), "Board Y: " + str(self.board_y))
        self.driver.execute_script("window.canvas1 = document.createElement('canvas');"
                              "canvas1.width = window.innerWidth; canvas1.height = window.innerHeight;"
                              "canvas1.style.width = '100%'; canvas1.style.height = '100%';"
                              "canvas1.style.position =  'absolute';"
                              "canvas1.style.left = 0; canvas1.style.top = 0;"
                              "canvas1.style.zIndex = 100000;"
                              "canvas1.style.pointerEvents = 'none';"
                              "document.body.appendChild(canvas1);"
                              "window.context1 = canvas1.getContext('2d');"
                              "context1.globalAlpha = 0.3;"
                              "context1.font = '30px Arial';"

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
                              "context2.font = '30px Arial';"
                              "window.canvas3 = document.createElement('canvas');"
                              "canvas3.width = window.innerWidth; canvas3.height = window.innerHeight;"
                              "canvas3.style.width = '100%'; canvas3.style.height = '100%';"
                              "canvas3.style.position =  'absolute';"
                              "canvas3.style.left = 0; canvas3.style.top = 0;"
                              "canvas3.style.zIndex = 100000;"
                              "canvas3.style.pointerEvents = 'none';"
                              "document.body.appendChild(canvas3);"
                              "window.context3 = canvas3.getContext('2d');"
                              "context3.font = '20px Arial';"
                              "context3.fillStyle = 'white';"
                              , self.chessboard)
        self.driver.execute_script("window.canvas_arrow = function (context, fromx, fromy, tox, toy){"
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
                              , self.chessboard)

    def ClearCanvas(self, canvas_number):
        str_canvas = "canvas" + str(canvas_number)
        str_context = "context" + str(canvas_number)
        self.driver.execute_script(str_context + ".clearRect(0, 0, " + str_canvas + ".width, " + str_canvas + ".height);")

    def Login(self, username, password):
        name = self.driver.find_element_by_id("username")
        passwd = self.driver.find_element_by_id("password")
        name.send_keys(username)
        passwd.send_keys(password)
        self.driver.find_element_by_name("login").click()
        print("Login complete")

    def DrawText(self, subTexts, superTexts):
        subtext_x = self.board_x + 300
        subtext_y = self.board_y - 10
        supertext_x = self.board_x + 300
        supertext_y = self.board_y - 40

        self.driver.execute_script("context3.clearRect(0, 0, canvas3.width, canvas3.height);")
        for i in range(len(subTexts)):
            self.driver.execute_script("context3.fillText('" + str(subTexts[i]) + "', " + str(subtext_x + (i * 100)) + ", " + str(subtext_y) + ");"
                , self.chessboard)
        for i in range(len(superTexts)):
            self.driver.execute_script("context3.fillText('" + str(superTexts[i]) + "', " + str(subtext_x + (i * 100)) + ", " + str(supertext_y) + ");"
                , self.chessboard)

    def FindPlayerColor(self):
        try:
            self.driver.find_element_by_css_selector("div[class='board-player bottom white']")
        except:
            return "black"
        return "white"

    def MakeMove(self, move, side):
        first_half_move = move[:2]
        second_half_move = move[2:4]
        if side == "white":
            first_top = (self.board_dim - self.piece_dim * int(first_half_move[1])) + self.piece_dim // 2
            first_left = self.piece_dim * (ord(first_half_move[0]) - 97) + self.piece_dim // 2

            second_top = (self.board_dim - self.piece_dim * int(second_half_move[1])) + self.piece_dim//2
            second_left = self.piece_dim * (ord(second_half_move[0]) - 97) + self.piece_dim // 2
        else:
            first_top = (self.board_dim - self.piece_dim * (9 - int(first_half_move[1]))) + self.piece_dim // 2
            first_left = self.piece_dim * (7 - (ord(first_half_move[0]) - 97)) + self.piece_dim // 2

            second_top = (self.board_dim - self.piece_dim * (9 - int(second_half_move[1]))) + self.piece_dim // 2
            second_left = self.piece_dim * (7 - (ord(second_half_move[0]) - 97)) + self.piece_dim // 2

        self.action_chains.move_to_element_with_offset(self.chessboard, first_left, first_top)
        self.action_chains.click()
        self.action_chains.move_to_element_with_offset(self.chessboard, second_left, second_top)
        self.action_chains.click()
        self.action_chains.perform()

    def DrawMove(self, move, side, colour):
        first_half_move = move[:2]
        second_half_move = move[2:4]
    
        if side == "white":
            first_top = (self.board_dim - self.piece_dim * int(first_half_move[1]))
            first_left = self.piece_dim * (ord(first_half_move[0]) - 97)
    
            second_top = (self.board_dim - self.piece_dim * int(second_half_move[1]))
            second_left = self.piece_dim * (ord(second_half_move[0]) - 97)
        else:
            first_top = (self.board_dim - self.piece_dim * (9 - int(first_half_move[1])))
            first_left = self.piece_dim * (7 - (ord(first_half_move[0]) - 97))
    
            second_top = (self.board_dim - self.piece_dim * (9 - int(second_half_move[1])))
            second_left = self.piece_dim * (7 - (ord(second_half_move[0]) - 97))
    
        self.driver.execute_script("context1.clearRect(0, 0, canvas1.width, canvas1.height);"
                              "canvas1.style.visibility = 'visible';"
                              "context1.globalAlpha = 0.3;"
                              "context1.fillStyle = " + colour + ";"
                              "context1.fillRect(" + str(self.board_x + first_left) + ", " + str(self.board_y + first_top) + ", " + str(self.piece_dim) + ", " + str(self.piece_dim) + ");"
                              "context1.fillRect(" + str(self.board_x + second_left) + ", " + str(self.board_y + second_top) + ", " + str(self.piece_dim) + ", " + str(self.piece_dim) + ");"
                              , self.chessboard)

    def DrawMultipleMoves(self, selected_canvas, moves, side, colours):
        arrow_coords = []
        for i in range(len(moves)):
            first_half_move = moves[i][:2]
            second_half_move = moves[i][2:4]
    
            if side == "white":
                first_top = (self.board_dim - self.piece_dim * int(first_half_move[1]))
                first_left = self.piece_dim * (ord(first_half_move[0]) - 97)
    
                second_top = (self.board_dim - self.piece_dim * int(second_half_move[1]))
                second_left = self.piece_dim * (ord(second_half_move[0]) - 97)
            else:
                first_top = (self.board_dim - self.piece_dim * (9 - int(first_half_move[1])))
                first_left = self.piece_dim * (7 - (ord(first_half_move[0]) - 97))
    
                second_top = (self.board_dim - self.piece_dim * (9 - int(second_half_move[1])))
                second_left = self.piece_dim * (7 - (ord(second_half_move[0]) - 97))
    
            arrow_left1 = str(self.board_x + first_left + self.piece_dim // 2)
            arrow_top1 = str(self.board_y + first_top + self.piece_dim // 2)
            arrow_left2 = str(self.board_x + second_left + self.piece_dim // 2)
            arrow_top2 = str(self.board_y + second_top + self.piece_dim // 2)
            arrow_coords.append((arrow_left1, arrow_top1, arrow_left2, arrow_top2))
            
        for i in range(len(arrow_coords)):
            move_coords = arrow_coords[i]
            self.driver.execute_script("context" + str(selected_canvas) + ".globalAlpha = " + str(1 - i * 0.3) + ";"
                                  "canvas_arrow(context" + str(selected_canvas) + ", " + move_coords[0] + ", " + move_coords[1] + ", " + move_coords[2] + ", " + move_coords[3] + ");"
                                  , self.chessboard)
        if selected_canvas == 1:
            self.driver.execute_script("context2.clearRect(0, 0, canvas2.width, canvas2.height);"
                                  "canvas2.style.visibility = 'hidden';"
                                  "canvas1.style.visibility = 'visible';"
                                  , self.chessboard)
        elif selected_canvas == 2:
            self.driver.execute_script("context1.clearRect(0, 0, canvas2.width, canvas2.height);"
                                  "canvas1.style.visibility = 'hidden';"
                                  "canvas2.style.visibility = 'visible';"
                                  , self.chessboard)
        if selected_canvas == 1:
            return 2
        elif selected_canvas == 2:
            return 1

    def EvaluateMoves(self, side):
        try:
            arrow = self.driver.find_element_by_class_name("chessBoardArrow")
        except Exception as e:
            return None
        arrow_x1 = arrow.location.get("x")
        arrow_y1 = arrow.location.get("y")
        arrow_x2 = arrow.size.get("width") + arrow_x1 - self.piece_dim
        arrow_y2 = arrow.size.get("height") + arrow_y1 - self.piece_dim
        if side == 'white':
            starting_square = chr(int((arrow_x1 - self.board_x) / self.piece_dim) + 97) + str(8 - int((arrow_y1 - self.board_y) / self.piece_dim))
            ending_square = chr(int((arrow_x2 - self.board_x) / self.piece_dim) + 97) + str(8 - int((arrow_y2 - self.board_y) / self.piece_dim))

            starting_square2 = chr(int((arrow_x1 - self.board_x) / self.piece_dim) + 97) + str(8 - int((arrow_y2 - self.board_y) / self.piece_dim))
            ending_square2 = chr(int((arrow_x2 - self.board_x) / self.piece_dim) + 97) + str(8 - int((arrow_y1 - self.board_y) / self.piece_dim))
        elif side == 'black':
            starting_square = chr(7 - int((arrow_x1 - self.board_x) / self.piece_dim) + 97) + str(1 + int((arrow_y1 - self.board_y) / self.piece_dim))
            ending_square = chr(7 - int((arrow_x2 - self.board_x) / self.piece_dim) + 97) + str(1 + int((arrow_y2 - self.board_y) / self.piece_dim))

            starting_square2 = chr(7 - int((arrow_x1 - self.board_x) / self.piece_dim) + 97) + str(1 + int((arrow_y2 - self.board_y) / self.piece_dim))
            ending_square2 = chr(7 - int((arrow_x2 - self.board_x) / self.piece_dim) + 97) + str(1 + int((arrow_y1 - self.board_y) / self.piece_dim))
        else:
            print("Side is invalid")
            return

        possible_moves = []
        legal_moves = []
        possible_moves.append(chess.Move.from_uci(starting_square + ending_square))
        possible_moves.append(chess.Move.from_uci(ending_square + starting_square))
        possible_moves.append(chess.Move.from_uci(starting_square2 + ending_square2))
        possible_moves.append(chess.Move.from_uci(ending_square2 + starting_square2))

        print("Possible moves", [str(x) for x in possible_moves])

        possible_moves = set(possible_moves)
        for move in possible_moves:
            if move in board.legal_moves:
                legal_moves.append(move)
        if len(legal_moves) > 0:
            return legal_moves
        print("All are illegal moves", ', '.join(map(str, possible_moves)))
        return None

def evaluate_position(position, depth):
    global engine, handler
    engine.position(position)
    try:
        position_evaluation = engine.go(depth=depth)
        eval = handler.info["score"][1].cp/100.0
    except Exception as e:
        print("Exception in evaluate_position:", e)
        eval = 100
        return eval
    # print(position)
    return eval


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

multiPV_available = False

engine = chess.uci.popen_engine(ENGINE_PATH + ENGINE_NAME)
engine.uci()
handler = chess.uci.InfoHandler()
engine.info_handlers.append(handler)
print("Loaded", engine.name)


if ENGINE_NAME == "stockfish_9_x64.exe":
    engine.setoption({"Skill Level": 8})
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

SeleniumI = SeleniumChess(browser)

# username, password = "shortbr", "malifeinc"
# username, password = "rimkill", "failure"
# username, password = "breachFirst", "foamfathom"
username, password = "acolade", "rammification"

SeleniumI.Login(username, password)


try:
    browser.get("https://www.chess.com/live")
except TimeoutException:
    browser.execute_script("window.stop();")


target_element_name = "pgn"
target_class_name = "gotomove"


move_str = "1. "
starting_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

player = "white"

difficulty = 1
canvas_number = 1

BLACK = "black"
WHITE = "white"

move_count = 1
moves = []
last_move_time = time.time()

if multiPV_available:
    engine.setoption({"MultiPV": 3})

multiPV_move_colours = ["'blue'", "'green'", "'red'"]

SeleniumI.GetElements()
SeleniumI.CreateBoardCanvas()

new_position = 2

while True:
    try:
        time.sleep(0.1)

        got_target = True
        turn_black = False
        found_first_move = True
        
        player = SeleniumI.FindPlayerColor()

        try:
            ending_str = "[id$=gotomoveid_0_1]"
            start_move = browser.find_element_by_css_selector(ending_str)
        except:
            found_first_move = False

        while True:
            try:
                element_str = "[id$=gotomoveid_0_" + str(move_count) + "]"
                target_element = browser.find_element_by_css_selector(element_str)
                target_element_content = target_element.text

                # if got_target:
                if target_element_content != "":
                    moves.append(target_element_content)
                    move_count += 1
                    new_position = 2
                else:
                    turn_black = True
                    break
            except Exception as e:
                # print(e)
                # got_target = False
                break

        if found_first_move and len(moves) > 0 and (moves[-1] != "1-0" and moves[-1] != "0-1" and moves[-1] != "1/2-1/2") or len(moves) == 0 and player == WHITE:

            if not move_only:
                if turn_black and player == WHITE:
                    continue
                elif not turn_black and player == BLACK:
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

            # if new_position >= 5:
            #     # print("Position has not changed")
            #     continue
            # else:
            #     new_position += 1

            search_depth = 8
            engine.position(board)
            current_evaluation = engine.go(depth=search_depth)
            best_move = str(current_evaluation[0])

            if board.turn:
                turn = "White"
                predicted_turn = "Black"
            else:
                turn = "Black"
                predicted_turn = "White"

            if 1 in handler.info["score"]:
                current_score = handler.info["score"][1].cp
            else:
                current_score = None
            if current_score is None:
                current_score = 100000
            current_score /= 100.0
            # print("Current evaluation with " + turn + ":", current_score)

            evaluations = [current_score]
            legal_moves = (SeleniumI.EvaluateMoves(player))
            if legal_moves is not None:
                for move in legal_moves:
                    board.push(move)
                    predicted_score = evaluate_position(board, 8)
                    # print("Predicted evaluation for " + str(move) + " with " + predicted_turn + ":", predicted_score)
                    evaluations.append(-predicted_score)
                    board.pop()
            else:
                legal_moves = []
            legal_moves.insert(0, turn)

            SeleniumI.DrawText(evaluations, legal_moves)

            obvious_move = False

            if multiPV_available:
                if difficulty == 0:
                    try:
                        handler.multipv(2)
                        with handler as info:
                            second_move = str(info["pv"][2][0])
                            third_move = str(info["pv"][3][0])
                            first_score = info["score"][1].cp
                            second_score = info["score"][2].cp
                            third_score = handler.info["score"][3].cp

                        if abs(first_score - second_score) >= 80:
                            # print("OBVIOUS MOVE 1")
                            obvious_move = True
                        elif abs(second_score - third_score) >= 80:
                            # print("OBVIOUS MOVE 2")
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
                        pass

            if not move_only and len(moves) > 1:
                if len(moves) < 10 or obvious_move:
                    time.sleep(random.uniform(0.1, 1))
                else:
                    time_diff = abs(time.time() - last_move_time - 1)
                    # print("Last move time:", time_diff)
                    if time_diff > 15:
                        time_diff = 15
                    sleep_time = random.uniform(time_diff / 5, time_diff / 2)
                    time.sleep(sleep_time)

            if not move_only:
                # makeMove(best_move, player)
                # print("Best Move:", best_move)
                # try:
                #     print("Evaluation:", handler.info["score"][1].cp/100.0)
                # except Exception as e:
                #     print("Evaluation exception:", e)
                SeleniumI.MakeMove(best_move, player)
            else:
                if multiPV_available:
                    try:
                        handler.multipv(2)
                        multiPV_moves = []
                        multiPV_moves.append(best_move)
                        multiPV_moves.append(str(handler.info["pv"][2][0]))
                        multiPV_moves.append(str(handler.info["pv"][3][0]))

                        # print("Moves")
                        # for move in multiPV_moves:
                        #     print(move, end=" ")
                        # print()

                        scores = []
                        for i in range(1, 4):
                            scores.append(handler.info["score"][i].cp/100.0)
                        # print("Scores")
                        for score in scores:
                            print(score, end=" ")
                        # print()
                        canvas_number = SeleniumI.DrawMultipleMoves(canvas_number, multiPV_moves, player, multiPV_move_colours)
                    except Exception as e:
                        SeleniumI.DrawMove(best_move, player, "'blue'")
                        print("MultiPV failed for move_only")
                        print(e)
                else:
                    SeleniumI.DrawMove(best_move, player, "'blue'")
            last_move_time = time.time()
        else:
            print("Failed to find any moves")
            # delay = float(input("Enter speed in seconds: ")) * 100
            player = SeleniumI.FindPlayerColor()
            print("Player is", player)
            move_count = 1
            moves = []
    except Exception as exception:
        print("Loop Exception:", exception)
        print("Moves:", moves)
        print("Engine handler info:", handler.info)
        move_count = 1
        moves = []
        print(traceback.print_exc())
