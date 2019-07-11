from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from Vec2 import Vec2
from constants import Side
from selenium_canvas import SeleniumCanvas


class SeleniumChess:
    def __init__(self, driver):
        self.patterns = {
            'chessboard': 'game-board',
            'bottom_player_white': 'board-player-component board-player-bottom board-player-white undefined',
            'bottom_player_black': 'board-player-component board-player-bottom board-player-black undefined',
            'top_player_white': 'board-player-component board-player-top board-player-white undefined',
            'top_player_black': 'board-player-component board-player-top board-player-black undefined',
            'move': 'move-text-component vertical-move-list-clickable',
            'selected_move': 'move-text-component move-text-selected vertical-move-list-clickable',
        }

        self.driver = driver

        self.graphics = SeleniumCanvas(self.driver)

        self.board = None
        self.chains = None
        self.board_dim = None
        self.piece_dim = None
        self.board_pos = None

    def try_set_elements(self):
        try:
            self.board = self.driver.find_element_by_id(self.patterns['chessboard'])
        except NoSuchElementException:
            return False  # All elements must be found. No point in continuing if even one is missing
        return True

    def update_variables(self):
        self.chains = webdriver.ActionChains(self.driver)
        self.board_dim = self.board.size.get('width')  # Board is square; either dimension will do
        self.piece_dim = self.board_dim // 8
        self.board_pos = Vec2(self.board.location.get('x'), self.board.location.get('y'))

    def find_player_colour(self):
        try:
            self.driver.find_element_by_xpath("//div[@class='{0}']".format(self.patterns['bottom_player_white']))
            return Side.WHITE
        except NoSuchElementException:  # Not white
            try:
                self.driver.find_element_by_xpath("//div[@class='{0}']".format(self.patterns['bottom_player_black']))
                return Side.BLACK
            except NoSuchElementException:  # Not white or black
                return Side.NEITHER

    def get_selected_move(self):
        try:
            selected_move = self.driver.find_element_by_xpath(
                "//span[@class='{0}']".format(self.patterns['selected_move']))
            return selected_move.text
        except NoSuchElementException:
            print('Latest move not found')
        return None

    def get_move_list(self):
        moves = []
        try:
            moves = self.driver.find_elements_by_xpath("//span[@class='{0}']".format(self.patterns['move']))
        except NoSuchElementException:
            print('No move elements found')

        try:
            last_move = self.driver.find_element_by_xpath("//span[@class='{0}']".format(self.patterns['selected_move']))
            moves.append(last_move)
        except NoSuchElementException:
            print('Last/Selected move not found')

        try:
            move_list = [e.text for e in moves]
            return move_list
        except StaleElementReferenceException:
            return self.get_move_list()

    def notation_to_pos(self, ply, bottom_color):
        if bottom_color == Side.WHITE:
            pos = Vec2(self.piece_dim * (ord(ply[0]) - 97), self.board_dim - self.piece_dim * int(ply[1]))
        elif bottom_color == Side.BLACK:
            pos = Vec2(self.piece_dim * (7 - (ord(ply[0]) - 97)), self.board_dim - self.piece_dim * (9 - int(ply[1])))
        else:
            print('Side to move should not be Side.NEITHER')
            return
        pos.x += self.board_pos.x
        pos.y += self.board_pos.y
        return pos

    def draw_move_squares(self, context_name, move, bottom_color):
        start_ply = move[:2]
        end_ply = move[2:4]
        first_pos = self.notation_to_pos(start_ply, bottom_color)
        second_pos = self.notation_to_pos(end_ply, bottom_color)
        dims = Vec2(self.piece_dim, self.piece_dim)
        self.graphics.set_styles(context_name, visibility="'visible'")
        self.graphics.draw_filled_rect(context_name, first_pos, dims)
        self.graphics.draw_filled_rect(context_name, second_pos, dims)

    def draw_move_arrows(self, context_name, move, bottom_color):
        center_offset = self.piece_dim // 2
        start_ply = move[:2]
        end_ply = move[2:4]
        first_pos = self.notation_to_pos(start_ply, bottom_color)
        first_pos.x += center_offset
        first_pos.y += center_offset
        second_pos = self.notation_to_pos(end_ply, bottom_color)
        second_pos.x += center_offset
        second_pos.y += center_offset
        self.graphics.set_styles(context_name, visibility="'visible'")
        self.graphics.draw_arrow(context_name, first_pos, second_pos)
