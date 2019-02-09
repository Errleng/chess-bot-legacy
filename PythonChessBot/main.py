import time
import chess.uci
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from constants import *
from selenium_chess import SeleniumChess


def login(driver, username, password):
    name = driver.find_element_by_id("username")
    pw = driver.find_element_by_id("password")
    name.send_keys(username)
    pw.send_keys(password)
    driver.find_element_by_name("login").click()


def game_end(move):
    return move == '1-0' or move == '0-1' or move == '1/2-1/2'


def can_play(player, move_list):
    return len(move_list) > 0 and not game_end(move_list[-1]) or len(move_list) == 0 and player == Side.WHITE


def board_from_moves(move_list):
    board = chess.Board(START_POS_FEN)
    try:
        for move in move_list:
            board.push_san(move)
    except Exception as e:
        print("Exception in pushing moves onto board: {0}".format(e))
        print(board)
        return None
    return board


def test():  # Logging and printing
    engine = chess.uci.popen_engine(ENGINE_RELATIVE_DIRECTORY + '/' + ENGINE_NAME)
    engine.uci()
    if USE_MULTIPV:
        engine.setoption({'MultiPV': MULTIPV_MOVE_COUNT + 1})

    handler = chess.uci.InfoHandler()
    engine.info_handlers.append(handler)

    browser = webdriver.Firefox()
    browser.maximize_window()
    browser.get(START_URL)
    login(browser, USERNAME, PASSWORD)
    browser.get(PLAY_CHESS_URL)

    interface = SeleniumChess(browser)

    first_cvs_name, first_ctx_name = 'first_cvs', 'first_ctx'
    interface.graphics.add_canvas_context(first_cvs_name, first_ctx_name)

    while True:
        try:
            time.sleep(1)

            start_time = time.time()

            if not interface.try_set_elements():
                print('Cannot find chessboard')
                continue
            interface.update_variables()
            player = interface.find_player_colour()
            moves = interface.get_move_list()
            print('Player = {0}'.format(player))
            print('Moves = {0}'.format(moves))

            if not can_play(player, moves):
                print('Game has ended')
                continue

            board = board_from_moves(moves)

            if board is None:
                continue

            if board.turn:
                turn = Side.WHITE
            else:
                turn = Side.BLACK

            print(board)

            engine.position(board)
            evaluation = engine.go(depth=ENGINE_SEARCH_DEPTH)
            best_move = str(evaluation[0])
            score = handler.info['score'][1].cp
            print('Turn = {0}, score = {1}, best move = {2}'.format(board.turn, score, best_move))

            interface.graphics.clear_context(first_ctx_name)

            if DRAW_TYPE == 'square':
                interface.graphics.set_styles(first_ctx_name, fillStyle="'blue'", globalAlpha='0.3')
                interface.draw_move_squares(first_ctx_name, best_move, player)
            elif DRAW_TYPE == 'arrow':
                interface.graphics.set_styles(first_ctx_name, fillStyle="'black'", globalAlpha='0.9')
                interface.draw_move_arrows(first_ctx_name, best_move, player)

            if USE_MULTIPV:
                try:
                    handler.multipv(MULTIPV_MOVE_COUNT)
                    for i in range(2, MULTIPV_MOVE_COUNT + 1 + 1):
                        move_i, score_i = str(handler.info['pv'][i][0]), handler.info['score'][i].cp
                        print('move {0} = {1}, score {0} = {2}'.format(i, move_i, score_i))

                        if DRAW_TYPE == 'square':
                            interface.graphics.set_styles(first_ctx_name,
                                                          fillStyle=MULTIPV_MOVE_COLOURS[i - MULTIPV_MOVE_COUNT])
                            interface.draw_move_squares(first_ctx_name, move_i, player)
                        elif DRAW_TYPE == 'arrow':
                            interface.graphics.set_styles(first_ctx_name,
                                                          globalAlpha=str(1 - (i - MULTIPV_MOVE_COUNT + 1) * 0.3))
                            interface.draw_move_arrows(first_ctx_name, move_i, player)
                except Exception as e:
                    print('Exception during MultiPV: {0}'.format(e))

            end_time = time.time()
            print('Time elapsed = {0}s'.format(end_time - start_time))
        except StaleElementReferenceException:
            print("Stale elements. Retrying...")


def main():  # No output
    engine = chess.uci.popen_engine(ENGINE_RELATIVE_DIRECTORY + '/' + ENGINE_NAME)

    browser = webdriver.Firefox()
    browser.maximize_window()
    browser.get(START_URL)
    login(browser, USERNAME, PASSWORD)
    browser.get(PLAY_CHESS_URL)

    interface = SeleniumChess(browser)

    while True:
        time.sleep(1)
        player = interface.find_player_colour()

        if player == Side.NEITHER:
            continue

        moves = interface.get_move_list()
        if not can_play(player, moves):
            continue


test()
