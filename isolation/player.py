"""
Module player implements different types of players
"""

import abc
import sys
import pygame as pg

from . import conn
from . import ai
from .ui import GUI
from .localization import Msg, _


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
        if not isinstance(self.ui, GUI):
            s = input(self._with_identifier(msg))
            for i, c in enumerate(("A", "B", "C", "D", "E", "F", "G")):
                for j, k in enumerate(("0", "1", "2", "3", "4", "5", "6")):
                    if s.lower() == f"{c}{k}".lower():
                        return i, j
            return -1, -1

        self.ui.display_info_img(self.icon)
        self.ui.display_info_text(_(Msg.YOUR_MOVE))
        pos = None
        while pos is None:
            for event in pg.event.get():
                if cursor:
                    self.ui.display_cursor(board)

                if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                    pos = event.pos
                    break

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)

        return self.ui.screen2board(pos, board.size())

    def _with_identifier(self, s):
        return _(Msg.WITH_PLAYER_IDENT) % (self.icon, s)

    def get_move(self, my_position, board):
        self.ui.display_help(my_position, board)
        move = self._get_choice(_(Msg.ENTER_YOUR_MOVE), board)
        self.ui.clear_help(my_position, board)
        return move

    def get_remove(self, board):
        return self._get_choice(_(Msg.ENTER_YOUR_REMOVE), board, cursor=True)


class LocalUserControlledPlayer(UserControlledPlayer):
    def __init__(self, ui, icon, socket=None):
        """
        A class to be used as a representation of local machine's player in online game.

        :param ui: used interface implementation
        :param icon: player's icon to distinguish from another
        :param socket: socket for writing local player's moves into it
        """
        super().__init__(ui, icon)
        self.socket = socket

    def get_move(self, my_position, board):
        """
        In addition to reading player's move also sends these coordinates to the opponent.
        """
        move = super().get_move(my_position, board)
        conn.send_coords(self.socket, move)
        return move

    def get_remove(self, board):
        """
        In addition to reading player's removed cell also sends these coordinates to the opponent.
        """
        remove = super().get_remove(board)
        conn.send_coords(self.socket, remove)
        return remove


class RemoteUserControlledPlayer(UserControlledPlayer):
    def __init__(self, ui, icon, socket=None):
        """
        A class to be used as a representation of remote machine's player in online game.

        :param ui: used interface implementation
        :param icon: player's icon to distinguish from another
        :param socket: socket for receiving remote player's moves
        """
        super().__init__(ui, icon)
        self.socket = socket

    def get_move(self, my_position, board):
        """
        Reads the remote user's move coordinates from the socket
        """
        if isinstance(self.ui, GUI):
            self.ui.display_info_text(_(Msg.WAIT))
            self.ui.display_info_img(self.ui.WAIT_ICON)
        return conn.receive_one_digit_coords(self.socket)

    def get_remove(self, board):
        """
        Reads the remote user's removal coordinates from the socket
        """
        if isinstance(self.ui, GUI):
            self.ui.display_info_text(_(Msg.WAIT))
            self.ui.display_info_img(self.ui.WAIT_ICON)
        return conn.receive_one_digit_coords(self.socket)


class RobotControlledPlayer(Player):

    def __init__(self, ui, difficulty):
        self.difficulty = difficulty
        self.remove_x = None
        self.remove_y = None
        self.ui = ui

    def get_move(self, my_position, board):
        if isinstance(self.ui, GUI):
            self.ui.display_info_text(_(Msg.WAIT))
            self.ui.display_info_img(self.ui.WAIT_ICON)

        turn = ai.minimax(board, self.difficulty)[1]
        self.remove_x = turn.remove_x
        self.remove_y = turn.remove_y
        return turn.move_x, turn.move_y

    def get_remove(self, board):
        if isinstance(self.ui, GUI):
            self.ui.display_info_text(_(Msg.WAIT))
            self.ui.display_info_img(self.ui.WAIT_ICON)
        return self.remove_x, self.remove_y
