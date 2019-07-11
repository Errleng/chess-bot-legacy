import time

import chess.engine
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

from constants import *
from selenium_chess import SeleniumChess


class Bot:
    def __init__(self):
        self.move_list = []
        self.cvs_ctx = []
        self.engine_moves = []
        self.engine_scores = []
        self.player = None
        self.board = None
        self.scrape_count = 0

        self.driver = webdriver.Firefox()
        self.engine = chess.engine.SimpleEngine.popen_uci(ENGINE_RELATIVE_DIRECTORY + '/' + ENGINE_NAME)
        self.interface = SeleniumChess(self.driver)

        self.setup_browser()
        self.setup_selenium_chess()

    def game_end(self, move):
        return move == '1-0' or move == '0-1' or move == '1/2-1/2'

    def login(self, username, password):
        name = self.driver.find_element_by_id("username")
        pw = self.driver.find_element_by_id("password")
        name.send_keys(username)
        pw.send_keys(password)
        self.driver.find_element_by_name("login").click()

    def can_play(self):
        return (len(self.move_list) > 0 and not self.game_end(self.move_list[-1])) or (len(
            self.move_list) == 0 and self.player == Side.WHITE)

    def setup_browser(self):
        self.driver.maximize_window()
        self.driver.get(START_URL)
        self.login(USERNAME, PASSWORD)
        self.driver.get(PLAY_CHESS_URL)

    def setup_selenium_chess(self):
        self.cvs_ctx.append(('first_cvs', 'first_ctx'))
        self.interface.graphics.add_canvas_context(self.cvs_ctx[0][0], self.cvs_ctx[0][1])

    def run(self):
        while True:
            try:
                time.sleep(0.25)

                start_time = time.time()

                if not self.interface.try_set_elements():
                    print('Cannot find chessboard')
                    continue

                self.interface.update_variables()
                self.player = self.interface.find_player_colour()
                self.scrape_move_list()

                print('Player = {0}'.format(self.player))
                print('Move list = {0}'.format(self.move_list))

                if not self.can_play():
                    print('Game has ended')
                    continue

                self.make_board()  # self.board is None if failed
                if self.board is None:
                    self.move_list = []  # rebuild move list if there's an error
                    continue

                if self.board.turn:
                    turn = Side.WHITE
                    turn_name = "WHITE"
                else:
                    turn = Side.BLACK
                    turn_name = "BLACK"

                print(self.board)
                self.engine_eval()

                print("{0} is playing".format(turn_name))
                for i in range(len(self.engine_moves)):
                    print("Move {0} = {1}, Score {0} = {2}".format(i, self.engine_moves[i], self.engine_scores[i]))

                self.display_moves()

                end_time = time.time()
                print('Time elapsed = {0}s'.format(end_time - start_time))
            except StaleElementReferenceException:
                print("Stale elements. Retrying...")

    def scrape_move_list(self):
        if len(self.move_list) > 0 and self.scrape_count <= FULL_SCRAPE_LIMIT:
            last_move = self.interface.get_selected_move()  # by default the latest move is selected
            if last_move != self.move_list[-1]:
                self.move_list.append(last_move)
        else:
            self.move_list = self.interface.get_move_list()
            self.scrape_count = 0
        self.scrape_count += 1

    def make_board(self):
        self.board = chess.Board(START_POS_FEN)
        try:
            for move in self.move_list:
                self.board.push_san(move)
        except Exception as e:
            self.board = None
            print("Exception in pushing moves onto board: {0}".format(e))
            print(self.board)

    def engine_eval(self):
        if USING_MULTIPV:
            evaluations = self.engine.analyse(board=self.board, limit=ENGINE_LIMIT, multipv=MULTIPV_MOVE_COUNT)
            self.engine_moves = []
            self.engine_scores = []
            for i in range(len(evaluations)):
                info = evaluations[i]
                move_i, score_i = str(info['pv'][0]), info['score']
                self.engine_moves.append(move_i)
                self.engine_scores.append(score_i)
        else:
            evaluation = self.engine.play(board=self.board, limit=ENGINE_LIMIT)
            self.engine_moves = [evaluation.move]
            self.engine_scores = [str(evaluation.info['score'])]

    def display_moves(self):
        main_ctx_name = self.cvs_ctx[0][1]
        self.interface.graphics.clear_context(main_ctx_name)
        if USING_MULTIPV:
            if DRAW_TYPE == 'square':
                for i in range(len(self.engine_moves)):
                    self.interface.graphics.set_styles(main_ctx_name,
                                                       fillStyle=MULTIPV_MOVE_COLOURS[i - MULTIPV_MOVE_COUNT])
                    self.interface.draw_move_squares(main_ctx_name, self.engine_moves[i], self.player)
            elif DRAW_TYPE == 'arrow':
                for i in range(len(self.engine_moves)):
                    alpha = (MULTIPV_MOVE_COUNT - i) * MULTIPV_ALPHA_STEP
                    self.interface.graphics.set_styles(main_ctx_name,
                                                       globalAlpha=str(alpha))
                    self.interface.draw_move_arrows(main_ctx_name, self.engine_moves[i], self.player)
        else:
            if DRAW_TYPE == 'square':
                self.interface.graphics.set_styles(main_ctx_name, fillStyle="'blue'", globalAlpha='0.25')
                self.interface.draw_move_squares(main_ctx_name, self.engine_moves[0], self.player)
            elif DRAW_TYPE == 'arrow':
                self.interface.graphics.set_styles(main_ctx_name, fillStyle="'black'", globalAlpha='1.0')
                self.interface.draw_move_arrows(main_ctx_name, self.engine_moves[0], self.player)
