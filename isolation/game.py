"""
Module game implements a game logic
"""

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


def move_player(player, board, is_bobs_turn):
    if is_bobs_turn:
        pos = board.get_bob_pos()
    else:
        pos = board.get_ann_pos()
    while True:
        x, y = player.get_move(pos, copy.deepcopy(board))
        if is_bobs_turn and board.move_bob(x, y):
            return
        if not is_bobs_turn and board.move_ann(x, y):
            return


def remove_tile(player, board):
    while True:
        x, y = player.get_remove(copy.deepcopy(board))
        if board.remove_cell(x, y):
            return


def run_game(ui, player_ann, player_bob):
    board = Board()
    ui.display(board)
    while True:
        move_player(player_ann, board, is_bobs_turn=False)
        ui.display(board)
        end, winner = end_of_game(board, ui)
        if end:
            return winner

        remove_tile(player_ann, board)
        ui.display(board)
        end, winner = end_of_game(board, ui)
        if end:
            return winner

        move_player(player_bob, board, is_bobs_turn=True)
        ui.display(board)
        end, winner = end_of_game(board, ui)
        if end:
            return winner

        remove_tile(player_bob, board)
        ui.display(board)
        end, winner = end_of_game(board, ui)
        if end:
            return winner
