import io
import abc
import copy
import enum
import base64
from itertools import product

import pygame as pg

from . import resources

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
        print("It's a draw!")

    def ann_won(self):
        print("Player %s has won!" % self.ANN_ICON)

    def bob_won(self):
        print("Player %s has won!" % self.BOB_ICON)

    def display_help(self, pos, board):
        pass

    def clear_help(self, pos, board):
        pass


class GUI(UI):

    class Color(enum.Enum):
        text = (0, 153, 255)
        background = (0, 0, 0)

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((700, 700), pg.SRCALPHA)
        pg.display.set_caption("Isolation!")

        self._load_objects()
        self.font = pg.font.SysFont("arial", 100)

        self._last_board = None

    def display(self, board):
        pg.mouse.set_cursor(*self.default_cursor)
        board_size = board.size()
        if self._last_board is None:
            self.screen.fill(self.Color.background.value)
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
        self._display_msg("Draw!")

    def ann_won(self):
        self._display_msg("Ann won!")

    def bob_won(self):
        self._display_msg("Bob won!")

    @property
    def size(self):
        return self.screen.get_size()

    def get_cell_size(self, board_size):
        screen_size = self.size
        w = screen_size[0] // board_size
        h = screen_size[1] // board_size
        return w, h

    def draw_cell(self, img, pos, board_size):
        cell_size = self.get_cell_size(board_size)
        scaled_image = pg.transform.scale(img, cell_size)
        screen_pos = self.board2screen(pos, board_size)
        self.screen.blit(scaled_image, screen_pos)

    def display_help(self, pos, board):
        self.clear_help(pos, board)
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
            if not board.is_empty(i, j):
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
        help = io.BytesIO(base64.b64decode(resources.help))

        self._ann = pg.image.load(avatar1)
        self._bob = pg.image.load(avatar2)
        self._block = pg.image.load(block)
        self._empty = pg.image.load(hole)
        self._help = pg.image.load(help)

        data = resources.hammer.split('\n')
        masks = pg.cursors.compile(data, 'X', '.')
        self.remove_cursor = ((32, 24), (3, 7)) + masks
        self.default_cursor = pg.cursors.arrow

    def _display_msg(self, msg):
        screen_size = self.size
        text = self.font.render(msg, True, self.Color.text.value)
        rect = text.get_rect()
        rect.center = screen_size[0] // 2, screen_size[1] // 2
        self.screen.blit(text, rect)
        pg.display.update()
        self._finalize()

    def _finalize(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    break
            else:
                continue
            break
