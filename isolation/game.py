import copy
import enum
import pygame as pg

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

    if pg.get_init():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True, Winner.none

    return False, Winner.none


def run_game(ui, player_ann, player_bob):
    board = Board()
    ui.display(board)
    while True:
        while True:
            ann_pos = board.get_ann_pos()
            ui.display_help(ann_pos, board)
            x, y = player_ann.get_move(copy.deepcopy(board))
            if board.move_ann(x, y):
                ui.clear_help(ann_pos, board)
                break

        ui.display(board)
        end, winner = end_of_game(board, ui)
        if end:
            return winner

        while True:
            x, y = player_ann.get_remove(copy.deepcopy(board))
            if board.remove_cell(x, y):
                break

        ui.display(board)
        end, winner = end_of_game(board, ui)
        if end:
            return winner

        while True:
            x, y = player_bob.get_move(copy.deepcopy(board))
            if board.move_bob(x, y):
                break

        ui.display(board)
        end, winner = end_of_game(board, ui)
        if end:
            return winner

        while True:
            x, y = player_bob.get_remove(copy.deepcopy(board))
            if board.remove_cell(x, y):
                break

        ui.display(board)
        end, winner = end_of_game(board, ui)
        if end:
            return winner
