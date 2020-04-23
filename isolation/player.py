import abc
import sys
import pygame as pg

from .ai import minimax
from .ui import TUI


class Player(abc.ABC):
    @abc.abstractmethod
    def get_move(self, my_position, board):
        pass

    @abc.abstractmethod
    def get_remove(self, board):
        pass


class UserControlledPlayer(Player):

    def __init__(self, ui):
        self.ui = ui

    def _get_choice(self, msg, board, cursor=False):
        if isinstance(self.ui, TUI):
            s = input(msg)
            for i, c in enumerate(("A", "B", "C", "D", "E", "F", "G")):
                for j, k in enumerate(("0", "1", "2", "3", "4", "5", "6")):
                    if s == f"{c}{k}":
                        return i, j
        else:
            pos = None
            while pos is None:
                for event in pg.event.get():
                    if cursor:
                        self.ui.display_cursor(board)

                    if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                        pos = event.pos
                        break
                    elif event.type == pg.QUIT:
                        pg.quit()
                        sys.exit(0)

            return self.ui.screen2board(pos, board.size())

    def get_move(self, my_position, board):
        self.ui.display_help(my_position, board)
        move = self._get_choice("Enter your move (ex. A3):", board)
        self.ui.clear_help(my_position, board)
        return move

    def get_remove(self, board):
        return self._get_choice("Enter a cell to remove (ex. B3):", board, cursor=True)


class RobotControlledPlayer(Player):

    def __init__(self, maxdepth=3, maxscatter=2):
        self.maxdepth = maxdepth
        self.maxscatter = maxscatter
        self.remove_x = None
        self.remove_y = None

    def get_move(self, my_position, board):
        _, turn = minimax(board, self.maxdepth, self.maxscatter)
        self.remove_x = turn.remove_x
        self.remove_y = turn.remove_y
        return turn.move_x, turn.move_y

    def get_remove(self, board):
        return self.remove_x, self.remove_y