"""
Module player implements different types of players
"""

import abc
import sys
import pygame as pg

from . import connection_utils
from . import ai
from .ui import TUI, GUI


class Player(abc.ABC):
    @abc.abstractmethod
    def get_move(self, my_position, board):
        pass

    @abc.abstractmethod
    def get_remove(self, board):
        pass


class UserControlledPlayer(Player):

    def __init__(self, ui, icon):
        self.ui = ui
        self.icon = icon

    def _get_choice(self, msg, board, cursor=False):
        if isinstance(self.ui, TUI):
            s = input(self._with_identifier(msg))
            for i, c in enumerate(("A", "B", "C", "D", "E", "F", "G")):
                for j, k in enumerate(("0", "1", "2", "3", "4", "5", "6")):
                    if s.lower() == f"{c}{k}".lower():
                        return i, j
        else:
            self.ui.display_info_img(self.icon)
            self.ui.display_info_text("Your move")
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

    def _with_identifier(self, s):
        return "Player %s! %s" % (self.icon, s)

    def get_move(self, my_position, board):
        self.ui.display_help(my_position, board)
        move = self._get_choice("Enter your move (ex. A3):", board)
        self.ui.clear_help(my_position, board)
        return move

    def get_remove(self, board):
        return self._get_choice("Enter a cell to remove (ex. B3): ", board, cursor=True)


class LocalUserControlledPlayer(UserControlledPlayer):
    def __init__(self, ui, icon, socket=None):
        super().__init__(ui, icon)
        self.socket = socket

    def get_move(self, my_position, board):
        move = super().get_move(my_position, board)
        connection_utils.send_coords(self.socket, move)
        return move

    def get_remove(self, board):
        remove = super().get_remove(board)
        connection_utils.send_coords(self.socket, remove)
        return remove


class RemoteUserControlledPlayer(UserControlledPlayer):
    def __init__(self, ui, icon, socket=None):
        super().__init__(ui, icon)
        self.socket = socket

    def get_move(self, my_position, board):
        if isinstance(self.ui, GUI):
            self.ui.display_info_text("Wait")
            self.ui.display_info_img(self.ui.WAIT_ICON)
        return connection_utils.receive_one_digit_coords(self.socket)

    def get_remove(self, board):
        if isinstance(self.ui, GUI):
            self.ui.display_info_text("Wait")
            self.ui.display_info_img(self.ui.WAIT_ICON)
        return connection_utils.receive_one_digit_coords(self.socket)


class RobotControlledPlayer(Player):

    def __init__(self, ui, difficulty, maxdepth=3, maxscatter=2):
        self.difficulty = difficulty
        self.remove_x = None
        self.remove_y = None
        self.ui = ui

    def get_move(self, my_position, board):
        if isinstance(self.ui, GUI):
            self.ui.display_info_text("Wait")
            self.ui.display_info_img(self.ui.WAIT_ICON)

        _, turn = ai.minimax(board, self.difficulty)
        self.remove_x = turn.remove_x
        self.remove_y = turn.remove_y
        return turn.move_x, turn.move_y

    def get_remove(self, board):
        if isinstance(self.ui, GUI):
            self.ui.display_info_text("Wait")
            self.ui.display_info_img(self.ui.WAIT_ICON)
        return self.remove_x, self.remove_y
