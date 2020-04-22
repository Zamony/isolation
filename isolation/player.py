import abc

from . import connection_utils
from .ai import minimax


class Player(abc.ABC):
    @abc.abstractmethod
    def get_move(self, board):
        pass

    @abc.abstractmethod
    def get_remove(self, board):
        pass


class UserControlledPlayer(Player):

    def __init__(self, icon):
        self.icon = icon

    def _get_choice(self, msg, board):
        s = input(msg)
        for i, c in enumerate(("A", "B", "C", "D", "E", "F", "G")):
            for j, k in enumerate(("0", "1", "2", "3", "4", "5", "6")):
                if s.lower() == f"{c}{k}".lower():
                    return i, j

        return board.size, board.size

    def _with_identifier(self, s):
        return "Player %s! %s" % (self.icon, s)

    def get_move(self, board):
        return self._get_choice(self._with_identifier("Enter your move (ex. A3): "), board)

    def get_remove(self, board):
        return self._get_choice(self._with_identifier("Enter a cell to remove (ex. B3): "), board)


class LocalUserControlledPlayer(UserControlledPlayer):
    def __init__(self, icon, socket=None):
        super().__init__(icon)
        self.socket = socket

    def get_move(self, board):
        move = super().get_move(board)
        connection_utils.send_coords(self.socket, move)
        return move

    def get_remove(self, board):
        remove = super().get_remove(board)
        connection_utils.send_coords(self.socket, remove)
        return remove


class RemoteUserControlledPlayer(UserControlledPlayer):
    def __init__(self, icon, socket=None):
        super().__init__(icon)
        self.socket = socket

    def get_move(self, board):
        return connection_utils.receive_one_digit_coords(self.socket)

    def get_remove(self, board):
        return connection_utils.receive_one_digit_coords(self.socket)


class RobotControlledPlayer(Player):

    def __init__(self, maxdepth=3, maxscatter=2):
        self.maxdepth = maxdepth
        self.maxscatter = maxscatter
        self.remove_x = None
        self.remove_y = None

    def get_move(self, board):
        _, turn = minimax(board, self.maxdepth, self.maxscatter)
        self.remove_x = turn.remove_x
        self.remove_y = turn.remove_y
        return turn.move_x, turn.move_y

    def get_remove(self, board):
        return self.remove_x, self.remove_y