import copy
import enum

from .board import Board


class Winner(enum.Enum):
    none = 0
    player_a = 1
    player_b = 2


def end_of_game(board, ui):
    ann_isolated = not board.can_ann_move()
    bob_isolated = not board.can_bob_move()
    if ann_isolated and bob_isolated:
        ui.display(board)
        ui.draw()
        return True, Winner.none

    if ann_isolated:
        ui.display(board)
        ui.bob_won()
        return True, Winner.player_b

    if bob_isolated:
        ui.display(board)
        ui.ann_won()
        return True, Winner.player_a

    return False, Winner.none


def run_game(ui, player_ann, player_bob):
    board = Board()
    while True:
        ui.display(board)
        while True:
            x, y = player_ann.get_move(copy.deepcopy(board))
            if board.move_ann(x, y):
                break

        ui.display(board)

        while True:
            x, y = player_ann.get_remove(copy.deepcopy(board))
            if board.remove_cell(x, y):
                break

        end, winner = end_of_game(board, ui)
        if end:
            return winner

        ui.display(board)

        while True:
            x, y = player_bob.get_move(copy.deepcopy(board))
            if board.move_bob(x, y):
                break
        
        ui.display(board)

        while True:
            x, y = player_bob.get_remove(copy.deepcopy(board))
            if board.remove_cell(x, y):
                break

        end, winner = end_of_game(board, ui)
        if end:
            return winner

