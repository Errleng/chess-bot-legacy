import os
import time
import random
import numpy
import cv2
import imutils
import chess.uci
import win32api
import win32con

from PIL import Image
from PIL import ImageGrab

def rgbTemplateMatchMat(img, temp):
    res = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF_NORMED)

    _, max_Val, _, _ = cv2.minMaxLoc(res)

    return max_Val

def clickDown(x, y):
    win32api.SetCursorPos((x, y))
    # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(x/1920.0 * 65535.0), int(y/1080.0 * 65535.0))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def clickUp(x, y):
    win32api.SetCursorPos((x, y))
    # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(x/1920.0 * 65535.0), int(y/1080.0 * 65535.0))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def main():
    # Constants

    LAPTOP = False

    move_only = True
    new_board = False

    IMAGES_PATH, TEMPLATES_PATH, TIMERS_PATH, ENGINE_PATH = "", "", "", ""

    BOARD_DIM, PIECE_DIM, TIMER_RESIZE_WIDTH, BOARD_RESIZE_WIDTH, TIMER_SIMILARITY_THRESHOLD, PIECE_SIMILARITY_THRESHOLD = 0, 0, 0, 0, 0, 0
    BLACK_TIMER_BBOX, WHITE_TIMER_BBOX, BOARD_BBOX = 0, 0, 0
    
    BLACK = "black"
    WHITE = "white"

    if LAPTOP:
        IMAGES_PATH = "C:/Users/aisae/Documents/Sourcetree/ChessBot/Screenshots/Laptop/"
        SAVE_PATH = IMAGES_PATH + "TempIconOutput/"
        TEMPLATES_PATH = IMAGES_PATH + "AllPieces"
        TIMERS_PATH = IMAGES_PATH + "Timers/"
        ENGINE_PATH = "C:/Users/aisae/Desktop/Desktop/Hold/Engines/"

        BOARD_DIM = 504
        PIECE_DIM = BOARD_DIM//8

        BLACK_TIMER_BBOX = (540, 105, 575, 140)
        WHITE_TIMER_BBOX = (540, 670, 575, 710)

        BOARD_BBOX = (160, 155, 690, 660)

        TIMER_RESIZE_WIDTH = 27
        BOARD_RESIZE_WIDTH = 126
    else:
        IMAGES_PATH = "D:/Documents/SourceTree/ChessBot/Screenshots/Desktop/"
        SAVE_PATH = IMAGES_PATH + "TempIconOutput/"
        TEMPLATES_PATH = IMAGES_PATH + "Pieces"
        TIMERS_PATH = IMAGES_PATH + "Timers/"
        ENGINE_PATH = "D:/Documents/SourceTree/ChessBot/Engines/"

        BOARD_DIM = 808
        PIECE_DIM = BOARD_DIM//8

        BLACK_TIMER_BBOX = (895, 115, 925, 145)
        WHITE_TIMER_BBOX = (895, 985, 925, 1010)

        BOARD_BBOX = (284, 162, 1092 + (6), 970)

        # TIMER_RESIZE_WIDTH = 52
        BOARD_RESIZE_WIDTH = 202

    practical_board = numpy.array(ImageGrab.grab(BOARD_BBOX))
    practical_board = imutils.resize(practical_board, width = BOARD_RESIZE_WIDTH)

    # print("Resized Board Shape:", practical_board.shape)

    RESIZED_BOARD_DIM = practical_board.shape[0]
    RESIZED_PIECE_DIM = RESIZED_BOARD_DIM//8

    FILE_TYPE = ".png"

    WHITE_SQUARE_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8]
    BLACK_SQUARE_NUMBERS = [8, 7, 6, 5, 4, 3, 2, 1]

    SLEEP_DELAY = 0.1

    TM_METHOD = cv2.TM_CCOEFF_NORMED

    PIECE_SIMILARITY_THRESHOLD, TIMER_SIMILARITY_THRESHOLD = 0, 0

    if TM_METHOD == cv2.TM_CCOEFF_NORMED:
        TIMER_SIMILARITY_THRESHOLD = 0.9
        PIECE_SIMILARITY_THRESHOLD = 0.5
    elif TM_METHOD == cv2.TM_SQDIFF_NORMED:
        TIMER_SIMILARITY_THRESHOLD = 0.9
        PIECE_SIMILARITY_THRESHOLD = 0.5

    BLACK_TIMER_IMG_NAME = "BlackTimer.png"
    WHITE_TIMER_IMG_NAME = "WhiteTimer.png"

    # Initialize list of template images
    templates = []
    for file in os.listdir(TEMPLATES_PATH):
        file_name = os.fsdecode(file)
        if file_name.endswith(FILE_TYPE):
            templates.append(file_name)

    template_paths = []
    for file in os.listdir(TEMPLATES_PATH):
        file_name = os.fsdecode(file)
        if file_name.endswith(FILE_TYPE):
            template_paths.append(TEMPLATES_PATH + "/" + file_name)

    template_mats = []
    for template_path in template_paths:
        template_mats.append(cv2.imread(template_path))

    black_timer_template = cv2.imread(TIMERS_PATH + BLACK_TIMER_IMG_NAME)
    white_timer_template = cv2.imread(TIMERS_PATH + WHITE_TIMER_IMG_NAME)

    # Initialize UCI chess engine

    # ENGINE_NAME = "Rybkav2.3.2a.mp.x64.exe"
    # ENGINE_NAME = "stockfish_9_x64.exe"
    ENGINE_NAME = "DeepHiarcs14WCSC_AC4.exe"

    if ENGINE_NAME == "DeepHiarcs14WCSC_AC4.exe":
        chess_engine = chess.uci.popen_engine("C:/Users/Recursor/Desktop/BACKUP/Engines/" + ENGINE_NAME)
    else:
        chess_engine = chess.uci.popen_engine(ENGINE_PATH + ENGINE_NAME)
    chess_engine.uci()
    engine_handler = chess.uci.InfoHandler()
    chess_engine.info_handlers.append(engine_handler)

    # Chess moves and rules
    white_kingside, white_queenside, black_kingside, black_queenside = True, True, True, True

    if not new_board:
        player = input("Enter the player's side: ").lower()

        move_count = int(input("Enter the number moves so far in the game: ")) # How many moves have passed in the game
        speed_mode = 0 # How fast and accurate the program is
        difficulty = 1 # How strong the program plays

    if not new_board and difficulty == 0:
        if ENGINE_NAME == "Rybkav2.3.2a.mp.x64.exe":
            # elo = 1500
            # chess_engine.setoption({"UCI_LimitStrength": True})
            # chess_engine.setoption({"UCI_Elo": elo})
            chess_engine.setoption({"MultiPV": 3})
            print("Set Rybka's MultiPV to 3")
        elif ENGINE_NAME == "stockfish_9_x64.exe":
            chess_engine.setoption({"MultiPV": 3})
            print("Set Stockfish's MultiPV to 3")
    elif not new_board and difficulty == 1:
        if ENGINE_NAME == "Rybkav2.3.2a.mp.x64.exe":
            elo = 1700
            chess_engine.setoption({"UCI_LimitStrength": True})
            chess_engine.setoption({"UCI_Elo": elo})
            print("Set Rybka's ELO to", elo)
        elif ENGINE_NAME == "stockfish_9_x64.exe":
            chess_engine.setoption({"MultiPV": 3})
            print("Set Stockfish's MultiPV to 3")
        # elif ENGINE_NAME == "DeepHiarcs14WCSC_AC4.exe":
        #     elo = 1700
        #     chess_engine.setoption({"UCI_LimitStrength": True})
        #     chess_engine.setoption({"UCI_Elo": elo})

    if new_board:
        board_capture = numpy.array(ImageGrab.grab(BOARD_BBOX), dtype=numpy.uint8)
        board_capture = cv2.cvtColor(board_capture, cv2.COLOR_BGR2RGB)
        resized_board_capture = imutils.resize(board_capture, width=BOARD_RESIZE_WIDTH)

        TEMPLATE_NAMES = ["BrookW", "BnightB", "BbishopW", "BqueenB", "BkingW", "BbishopB", "BnightW", "BrookB", "BpawnB", "BpawnW", "WPawnW", "WPawnB", "WRookB", "WNightW", "WBishopB", "WQueenW", "WKingB", "WBishopW", "WNightB", "WRookW"]

        image_count = 0
        template_name_count = 0

        for row in WHITE_SQUARE_NUMBERS:
            for col in WHITE_SQUARE_NUMBERS:
                square_image = resized_board_capture[int(RESIZED_PIECE_DIM * (row-1)): int(RESIZED_PIECE_DIM * row), int(RESIZED_PIECE_DIM * (col-1)): int(RESIZED_PIECE_DIM * col)]
                image_count += 1

                file_name = str(image_count)
                if row == 1 or row == 2 and col < 3 or row == 7 and col < 3 or row == 8:
                    file_name = TEMPLATE_NAMES[template_name_count]
                    template_name_count += 1

                cv2.imwrite(SAVE_PATH + file_name + FILE_TYPE, square_image)
                cv2.imshow("Piece", square_image)
                cv2.waitKey(100)
    else:
        while True:
            start_time = time.time()

            black_timer_capture = numpy.array(ImageGrab.grab(BLACK_TIMER_BBOX))
            white_timer_capture = numpy.array(ImageGrab.grab(WHITE_TIMER_BBOX))

            if player == BLACK:
                black_timer_capture, white_timer_capture = white_timer_capture, black_timer_capture

            # cv2.imshow("black timer", black_timer_capture)
            # cv2.waitKey(1000)

            # Image.fromarray(black_timer_capture, "RGB").save(TIMERS_PATH + "BlackTimer.png")
            # Image.fromarray(white_timer_capture, "RGB").save(TIMERS_PATH + "WhiteTimer.png")

            # resized_black_timer_capture = imutils.resize(black_timer_capture, width=TIMER_RESIZE_WIDTH)
            # resized_white_timer_capture = imutils.resize(white_timer_capture, width=TIMER_RESIZE_WIDTH)

            # Image.fromarray(resized_black_timer_capture, "RGB").save(TIMERS_PATH + "BlackTimer.png")
            # Image.fromarray(resized_black_timer_capture, "RGB").save(TIMERS_PATH + "WhiteTimer.png")

            # black_timer_similarity = rgbTemplateMatchMat(resized_black_timer_capture, black_timer_template)
            # white_timer_similarity = rgbTemplateMatchMat(resized_white_timer_capture, black_white_template)

            # cv_black_timer_capture = black_timer_capture.astype(numpy.uint8)
            # cv_white_timer_capture = white_timer_capture.astype(numpy.uint8)

            # print("capture type:", type(cv_black_timer_capture), "template type:", type(black_timer_template))

            black_timer_similarity = rgbTemplateMatchMat(black_timer_capture, black_timer_template)
            white_timer_similarity = rgbTemplateMatchMat(white_timer_capture, white_timer_template)

            moving_side = ""
            if black_timer_similarity > white_timer_similarity:
                if black_timer_similarity < TIMER_SIMILARITY_THRESHOLD:
                    print("Detected RED TIMER for BLACK")
                    moving_side = "w" # Detected White has a red timer
                else:
                    moving_side = "b" # Detected Black to move
            elif black_timer_similarity < white_timer_similarity:
                if white_timer_similarity < TIMER_SIMILARITY_THRESHOLD:
                    print("Detected RED TIMER for WHITE")
                    moving_side = "b"
                else:
                    moving_side = "w"
            else:
                moving_side = player[0]
                print("Timer similarities are the same!")

            # print("Moving side:", moving_side, black_timer_similarity, white_timer_similarity)

            if moving_side == "b" and player == WHITE:
                time.sleep(SLEEP_DELAY)
                continue
            if moving_side == "w" and player == BLACK:
                time.sleep(SLEEP_DELAY)
                continue

            time.sleep(SLEEP_DELAY * 5)

            board_capture = numpy.array(ImageGrab.grab(BOARD_BBOX), dtype = numpy.uint8)
            board_capture = cv2.cvtColor(board_capture, cv2.COLOR_BGR2RGB)
            resized_board_capture = imutils.resize(board_capture, width = BOARD_RESIZE_WIDTH)

            FEN = ""
            empty_square_count = 0
            total_square_count = 0
            row_slash_count = 0

            start_template_time = time.time()

            # print("Time to determine moving side:", start_template_time - start_time)

            # Start board template match
            if player == WHITE:
                for row in WHITE_SQUARE_NUMBERS:
                    for col in WHITE_SQUARE_NUMBERS:
                        square_image = resized_board_capture[int(RESIZED_PIECE_DIM * (row-1)): int(RESIZED_PIECE_DIM * row), int(RESIZED_PIECE_DIM * (col-1)): int(RESIZED_PIECE_DIM * col)]

                        similarity_list = []
                        for mat in template_mats:
                            similarity = rgbTemplateMatchMat(square_image, mat)
                            similarity_list.append(similarity)

                        best_match = max(similarity_list)
                        best_match_index = similarity_list.index(best_match)

                        # print(best_match)
                        # if 0.5 < best_match < 0.9:
                        #     cv2.imshow("Piece", square_image)
                        #     cv2.waitKey(0)

                        if best_match > PIECE_SIMILARITY_THRESHOLD:
                            best_template = templates[best_match_index]
                            if empty_square_count != 0:
                                FEN += str(empty_square_count)
                                empty_square_count = 0

                            # if best_template[0] == "B":
                                # FEN += best_template[1].lower()
                            # else:
                            #     FEN += best_template[1]
                            FEN += best_template[1]

                            row_slash_count += 1
                            if row_slash_count >= 8:
                                row_slash_count -= 8
                                FEN += "/"
                        else:
                            row_slash_count += 1
                            empty_square_count += 1
                            if row_slash_count >= 8:
                                FEN += str(empty_square_count)
                                FEN += "/"
                                row_slash_count -= 8
                                empty_square_count = 0
            elif player == BLACK:
                for row in BLACK_SQUARE_NUMBERS:
                    for col in BLACK_SQUARE_NUMBERS:
                        square_image = resized_board_capture[int(RESIZED_PIECE_DIM * (row - 1)): int(RESIZED_PIECE_DIM * row), int(RESIZED_PIECE_DIM * (col - 1)): int(RESIZED_PIECE_DIM * col)]

                        similarity_list = []
                        for mat in template_mats:
                            similarity = rgbTemplateMatchMat(square_image, mat)
                            similarity_list.append(similarity)

                        best_match = max(similarity_list)
                        best_match_index = similarity_list.index(best_match)

                        # print(best_match)
                        # if 0.5 < best_match < 0.9:
                        #     cv2.imshow("Piece", square_image)
                        #     cv2.waitKey(0)

                        if best_match > PIECE_SIMILARITY_THRESHOLD:
                            best_template = templates[best_match_index]
                            if empty_square_count != 0:
                                FEN += str(empty_square_count)
                                empty_square_count = 0

                                # if best_template[0] == "B":
                                # FEN += best_template[1].lower()
                            # else:
                            #     FEN += best_template[1]
                            FEN += best_template[1]

                            row_slash_count += 1
                            if row_slash_count >= 8:
                                row_slash_count -= 8
                                FEN += "/"
                        else:
                            row_slash_count += 1
                            empty_square_count += 1
                            if row_slash_count >= 8:
                                FEN += str(empty_square_count)
                                FEN += "/"
                                row_slash_count -= 8
                                empty_square_count = 0

            # Finish board template match

            end_template_time = time.time()

            # print("Time to template match:", end_template_time - start_template_time)

            if FEN.endswith("/"):
                FEN = FEN[:-1]

            castle_availability = ""
            if white_kingside:
                castle_availability += "K"
            if white_queenside:
                castle_availability += "Q"
            if black_kingside:
                castle_availability += "k"
            if black_queenside:
                castle_availability += "q"

            if castle_availability == "":
                castle_availability = "-"

            formatted_FEN = FEN + " " + moving_side + " " + castle_availability + " - " + "0 0"

            # print("Formatted FEN:", formatted_FEN)

            # Move calculation with chess engine
            board = chess.Board(formatted_FEN)
            chess_engine.position(board)

            # print(board)

            search_depth = 8
            if difficulty == 0:
                search_depth = random.randint(4, 7)

            depth = chess_engine.go(depth = search_depth)
            best_move = str(depth[0])

            if difficulty == 0:
                try:
                    engine_handler.multipv(2)
                    second_move = str(engine_handler.info["pv"][2][0])
                    third_move = str(engine_handler.info["pv"][3][0])

                    first_score = engine_handler.info["score"][1].cp
                    second_score = engine_handler.info["score"][2].cp
                    third_score = engine_handler.info["score"][3].cp
                    print("Move 1:", best_move, "Score:", first_score)
                    print("Move 2:", second_move, "Score:", second_score)
                    print("Move 3:", third_move, "Score:", third_score)

                    if abs(first_score - second_score) >= 80:
                        print("OBVIOUS MOVE 1")
                        time.sleep(random.randint(0, 1))
                    elif abs(second_score - third_score) >= 80:
                        print("OBVIOUS MOVe 2")
                        time.sleep(random.randint(0, 1))
                        best_move = second_move
                    else:
                        time.sleep(random.randint(0, 1))
                        move_chosen = random.randint(1, 3)
                        if move_chosen == 2:
                            best_move = second_move
                        elif move_chosen == 3:
                            best_move = third_move

                        if 10 <= move_count <= 30:
                            print("MIDDLEGAME")
                            time.sleep(random.randint(1, 5))
                        else:
                            time.sleep(random.randint(1, 150)/100.0)
                except:
                    print("Best Move:", best_move)
                    print(engine_handler.info)
            else:
                print("Best Move:", best_move)

            end_move_time = time.time()

            # print("Time to calculate move:", end_move_time - end_template_time)

            # print("Search Depth:", search_depth)

            if move_only:
                if player == BLACK:
                    first_half_move = best_move[:2]
                    second_half_move = best_move[2:4]

                    first_top = (BOARD_DIM - PIECE_DIM * (9 - int(first_half_move[1]))) + PIECE_DIM // 2
                    first_left = PIECE_DIM * (7 - (ord(first_half_move[0]) - 97)) + PIECE_DIM // 2

                    second_top = (BOARD_DIM - PIECE_DIM * (9 - int(second_half_move[1]))) + PIECE_DIM // 2
                    second_left = PIECE_DIM * (7 - (ord(second_half_move[0]) - 97)) + PIECE_DIM // 2
                else:
                    first_half_move = best_move[:2]
                    second_half_move = best_move[2:4]

                    first_top = (BOARD_DIM - PIECE_DIM * int(first_half_move[1])) + PIECE_DIM // 2
                    first_left = PIECE_DIM * (ord(first_half_move[0]) - 97) + PIECE_DIM // 2

                    second_top = (BOARD_DIM - PIECE_DIM * int(second_half_move[1])) + PIECE_DIM // 2
                    second_left = PIECE_DIM * (ord(second_half_move[0]) - 97) + PIECE_DIM // 2

                cv2.arrowedLine(board_capture, (first_left, first_top), (second_left, second_top), (255, 0, 0), 5)
                cv2.imshow("Best move on board", board_capture)
                cv2.waitKey(2000)

            if move_only or best_move == "0000":
                continue

            if 'e1' in best_move:
                white_kingside = False
                white_queenside = False
            if 'a1' in best_move:
                white_queenside = False
            if 'h1' in best_move:
                white_kingside = False

            if 'e8' in best_move:
                black_kingside = False
                black_queenside = False
            if 'a8' in best_move:
                black_queenside = False
            if 'h8' in best_move:
                black_kingside = False

            if player == BLACK:
                first_half_move = best_move[:2]
                second_half_move = best_move[2:4]

                first_top = 160 + (BOARD_DIM - PIECE_DIM * (9 - int(first_half_move[1]))) + 50
                first_left = 285 + PIECE_DIM * (7 - (ord(first_half_move[0]) - 97)) + 50

                second_top = 160 + (BOARD_DIM - PIECE_DIM * (9 - int(second_half_move[1]))) + 50
                second_left = 285 + PIECE_DIM * (7 - (ord(second_half_move[0]) - 97)) + 50
            else:
                first_half_move = best_move[:2]
                second_half_move = best_move[2:4]

                first_top = 160 + (BOARD_DIM - PIECE_DIM * int(first_half_move[1])) + 50
                first_left = 285 + PIECE_DIM * (ord(first_half_move[0]) - 97) + 50

                second_top = 160 + (BOARD_DIM - PIECE_DIM * int(second_half_move[1])) + 50
                second_left = 285 + PIECE_DIM * (ord(second_half_move[0]) - 97) + 50

            # print(first_left, first_top)

            clickDown(int(first_left), int(first_top))

            time.sleep(SLEEP_DELAY)

            clickUp(int(second_left), int(second_top))

            time.sleep(SLEEP_DELAY)

            win32api.SetCursorPos((5, 5))

            move_count += 1

            # print("Time to loop:", time.time() - start_time)

            time.sleep(SLEEP_DELAY)
main()