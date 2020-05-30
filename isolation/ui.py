"""
Module UI implements different types of user interface
"""

import io
import abc
import copy
import base64
from itertools import product

import pygame as pg

from . import resources
from . import config
from .localization import Msg, _


class UI(abc.ABC):

    @abc.abstractmethod
    def display(self, board):
        pass

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def ann_won(self):
        pass

    @abc.abstractmethod
    def bob_won(self):
        pass

    @abc.abstractmethod
    def display_help(self, pos, board):
        pass

    @abc.abstractmethod
    def clear_help(self, pos, board):
        pass


class TUI(UI):
    BOARD_DIGITS_GRID = "  0123456"
    ANN_ICON = "◍"
    BOB_ICON = "◆"

    def display(self, board):
        print("\n"*80, end="")
        n = board.size()
        ann_pos = board.get_ann_pos()
        bob_pos = board.get_bob_pos()
        ch = ["A", "B", "C", "D", "E", "F", "G"]
        print(self.BOARD_DIGITS_GRID)
        for i in range(n):
            print(ch[i] + " ", end="")
            for j in range(n):
                if (i, j) == ann_pos:
                    print(self.ANN_ICON, end="")
                    continue
                if (i, j) == bob_pos:
                    print(self.BOB_ICON, end="")
                    continue
                if not board.is_empty(i, j):
                    print("◻", end="")
                    continue
                print(" ", end="")

            print(" " + ch[i])
        print(self.BOARD_DIGITS_GRID)

    def draw(self):
        print(_(Msg.DRAW))

    def ann_won(self):
        print(_(Msg.PLAYER_X_WON) % self.ANN_ICON)

    def bob_won(self):
        print(_(Msg.PLAYER_X_WON) % self.BOB_ICON)

    def display_help(self, pos, board):
        pass

    def clear_help(self, pos, board):
        pass


class GUI(UI):

    def __init__(self, window=None):
        if window is None:
            pg.init()
            self.window = pg.display.set_mode(config.WINDOW_SIZE, pg.SRCALPHA)
        else:
            self.window = window
        pg.display.set_caption("Isolation!")
        self.screen = self.window.subsurface(pg.Rect(0, 0, *config.SCREEN_SIZE))

        self.font = pg.font.SysFont("arial", 100)

        self.info = self.window.subsurface(pg.Rect(config.SCREEN_SIZE[0], 0, *config.INFO_SIZE))
        self.info.fill(config.INFO_BACKGROUND_COLOR)
        self.info_font = pg.font.SysFont("arial", 25)
        self.info_txt_top = 0
        self.info_img_top = self.info_font.get_height()

        self._ann = None
        self._bob = None
        self._block = None
        self._empty = None
        self._help = None

        self._load_objects()
        self._set_icons(self.info.get_width() // 2)

        self._last_board = None
        self.cell_size = None

    def display(self, board):
        pg.mouse.set_cursor(*self.default_cursor)
        self.reset_info()
        board_size = board.size()
        if self._last_board is None:
            self._resize_images(board_size)
            self.screen.fill(config.SCREEN_BACKGROUND_COLOR)
            for y in range(board_size):
                for x in range(board_size):
                    self.draw_cell(self._block, (y, x), board_size)
        else:
            self.draw_cell(self._block, self._last_board.get_bob_pos(), board_size)
            self.draw_cell(self._block, self._last_board.get_ann_pos(), board_size)
            for y in range(board_size):
                for x in range(board_size):
                    if board.is_empty(y, x) and not self._last_board.is_empty(y, x):
                        self.draw_cell(self._empty, (y, x), board_size)
        self.draw_cell(self._ann, board.get_ann_pos(), board_size)
        self.draw_cell(self._bob, board.get_bob_pos(), board_size)
        self._last_board = copy.deepcopy(board)
        pg.display.update()

    def draw(self):
        self._display_final_msg(_(Msg.DRAW))

    def ann_won(self):
        self._display_final_msg(_(Msg.ANN_WON))

    def bob_won(self):
        self._display_final_msg(_(Msg.BOB_WON))

    def display_info_img(self, img):
        x = max((self.info.get_width() - img.get_width()) // 2, 0)
        y = self.info_img_top
        self.info.blit(img, (x, y))
        pg.display.update()
        return x, y

    def display_info_text(self, msg):
        text = self.info_font.render(msg, True, config.TEXT_COLOR)
        rect = text.get_rect()
        rect.left = max((self.info.get_width() - rect.width) // 2, 0)
        rect.top = self.info_txt_top
        self.info.blit(text, rect)
        pg.display.update()
        return rect.x, rect.y

    def reset_info(self):
        self.info.fill(config.INFO_BACKGROUND_COLOR)
        # render line from bottom to top
        for i in range(1, len(self.rules) + 1):
            rule = self.rules[-i]
            rect = rule.get_rect()
            rect.left = max((self.info.get_width() - rect.width) // 2, 0)
            # count position for current line
            rect.bottom = self.info.get_height()- i * self.info_font.get_height()
            self.info.blit(rule, rect)

    @property
    def size(self):
        return self.screen.get_size()

    def draw_cell(self, img, pos, board_size):
        screen_pos = self.board2screen(pos, board_size)
        self.screen.blit(img, screen_pos)

    def display_help(self, pos, board):
        y, x = pos
        board_size = board.size()
        for dx, dy in product([-1, 0, 1], repeat=2):
            if dx == 0 and dy == 0:
                continue
            i, j = y + dy, x + dx
            if not board.is_busy(i, j):
                self.draw_cell(self._help, (i, j), board_size)
        pg.display.update()

    def clear_help(self, pos, board):
        y, x = pos
        board_size = board.size()
        for dx, dy in product([-1, 0, 1], repeat=2):
            if dx == 0 and dy == 0:
                continue
            i, j = y + dy, x + dx
            if not board.is_busy(i, j):
                self.draw_cell(self._block, (i, j), board_size)

    def display_cursor(self, board):
        cursor_pos = pg.mouse.get_pos()
        y, x = self.screen2board(cursor_pos, board.size())
        if not board.is_busy(y, x):
            pg.mouse.set_cursor(*self.remove_cursor)
        else:
            pg.mouse.set_cursor(*self.default_cursor)

    def board2screen(self, pos, board_size):
        x, y = pos
        screen_w, screen_h = self.size
        x *= screen_w // board_size
        y *= screen_h // board_size
        return y, x

    def screen2board(self, pos, board_size):
        x, y = pos
        screen_w, screen_h = self.size
        x //= screen_w // board_size
        y //= screen_h // board_size
        return y, x

    def _load_objects(self):
        avatar1 = io.BytesIO(base64.b64decode(resources.avatar1))
        avatar2 = io.BytesIO(base64.b64decode(resources.avatar2))
        block = io.BytesIO(base64.b64decode(resources.block))
        hole = io.BytesIO(base64.b64decode(resources.hole))
        help_ = io.BytesIO(base64.b64decode(resources.help_))
        wait = io.BytesIO(base64.b64decode(resources.wait))

        self._ann = pg.image.load(avatar1)
        self._bob = pg.image.load(avatar2)
        self._block = pg.image.load(block)
        self._empty = pg.image.load(hole)
        self._help = pg.image.load(help_)
        self._wait = pg.image.load(wait)

        data = resources.hammer.split('\n')
        masks = pg.cursors.compile(data, 'X', '.')
        self.remove_cursor = ((32, 24), (3, 7)) + masks
        self.default_cursor = pg.cursors.arrow

        rules = _(Msg.RULES)
        self.rules = []
        for rule in rules.splitlines():
            self.rules.append(self.info_font.render(rule, True, config.TEXT_COLOR))

    def _set_icons(self, size):
        self.ANN_ICON = pg.transform.scale(self._ann, (size, size))
        self.BOB_ICON = pg.transform.scale(self._bob, (size, size))
        self.WAIT_ICON = pg.transform.scale(self._wait, (size, size))

    def _resize_images(self, board_size):
        screen_size = self.size
        w = screen_size[0] // board_size
        h = screen_size[1] // board_size
        self.cell_size = w, h
        self._ann = pg.transform.scale(self._ann, self.cell_size)
        self._bob = pg.transform.scale(self._bob, self.cell_size)
        self._block = pg.transform.scale(self._block, self.cell_size)
        self._empty = pg.transform.scale(self._empty, self.cell_size)
        self._help = pg.transform.scale(self._help, self.cell_size)

    def _display_final_msg(self, msg):
        screen_size = self.size
        text = self.font.render(msg, True, config.TEXT_COLOR)
        rect = text.get_rect()
        rect.center = screen_size[0] // 2, screen_size[1] // 2
        self.screen.blit(text, rect)
        pg.display.update()

        # finalize gui
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    break
            else:
                continue
            break
