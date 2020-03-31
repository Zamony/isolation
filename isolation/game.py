import copy

from .board import Board


def end_of_game(board, ui):
    ann_isolated = not board.can_ann_move()
    bob_isolated = not board.can_bob_move()
    if ann_isolated and bob_isolated:
        ui.display(board)
        ui.draw()
        return True

    if ann_isolated:
        ui.display(board)
        ui.bob_won()
        return True

    if bob_isolated:
        ui.display(board)
        ui.ann_won()
        return True

    return False


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

        if end_of_game(board, ui):
            return

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

        if end_of_game(board, ui):
            return

