import copy
import random
from enum import Enum
from typing import NamedTuple

class Turn(NamedTuple):
    move_x: int
    move_y: int
    remove_x: int
    remove_y: int

    @classmethod
    def default(cls):
        return Turn(0, 0, 0, 0)

class Difficulty(Enum):
    easy = 2
    normal = 3
    hard = 4

turn_number = 0

from .ui import TUI

def minimax(board, difficulty):
    complexity = 0
    i, j = board.get_ann_pos() # ann is an enemy
    complexity += board.count_ways_to_move(i, j)

    i, j = board.get_bob_pos()
    complexity += board.count_ways_to_move(i, j)

    maxdepth = min(Difficulty.hard.value, difficulty.value)
    max_complexity = 2 * max_heuristic()
    # the threshold here was determined empirically
    if complexity > max_complexity // 1.5:
        maxdepth = min(Difficulty.normal.value, maxdepth)

    inf = abs(max_heuristic()) + 1
    maxscatter = 1
    return _minimax(board, maxdepth, maxscatter, True, 0, -inf, inf)

def max_heuristic():
    # maximum number of possible ways to move
    return 8

def _best_turn(scores, is_bobs_turn):
    random.shuffle(scores)
    return max(scores) if is_bobs_turn else min(scores)

def _minimax(board, maxdepth, maxscatter, bobs_turn, depth, alpha, beta):
    i, j = board.get_bob_pos() if bobs_turn else board.get_ann_pos()
    if depth == maxdepth and bobs_turn:
        my_score = board.count_ways_to_move(i, j)
        enemy_score = board.count_ways_to_move(*board.get_ann_pos())
        return -enemy_score + my_score, Turn.default()

    if depth == maxdepth:
        my_score = board.count_ways_to_move(i, j)
        enemy_score = board.count_ways_to_move(*board.get_bob_pos())
        return -my_score + enemy_score, Turn.default()

    bob_isolated = not board.can_bob_move()
    ann_isolated = not board.can_ann_move()
    if bob_isolated and ann_isolated:
        return 0, Turn.default()
    if ann_isolated:
        return max_heuristic(), Turn.default()
    if bob_isolated:
        return -max_heuristic(), Turn.default()

    scores = []
    enemy_pos_x, enemy_pos_y = board.get_ann_pos() if bobs_turn else board.get_bob_pos()
    # heading towards the enemy at the start of the game (better for alpha-beta pruning)
    for pi in range(i+1, i-2, -1):
        for pj in range(j-1, j+2):
            new_board = copy.deepcopy(board)
            moved = new_board.move_bob(pi, pj) if bobs_turn else new_board.move_ann(pi, pj)
            if not moved:
                continue
            for ri in range(enemy_pos_x-maxscatter, enemy_pos_x+maxscatter+1):
                for rj in range(enemy_pos_y-maxscatter, enemy_pos_y+maxscatter+1):
                    if not new_board.can_be_removed(ri, rj):
                        continue
                    nb = copy.deepcopy(new_board)
                    nb.remove_cell(ri, rj)
                    turn_score, turn = _minimax(nb, maxdepth, maxscatter, not bobs_turn, depth+1, alpha, beta)
                    scores.append((turn_score, Turn(pi, pj, ri, rj)))
                    if bobs_turn:
                        alpha = max(alpha, turn_score)
                    else:
                        beta = min(beta, turn_score)
                    if alpha > beta:
                        return _best_turn(scores, bobs_turn)

    # if removal heuristic didn't work
    if len(scores) < 1:
        turn_score, turn = _minimax(board, maxdepth, maxscatter+1, bobs_turn, depth, alpha, beta)
        scores.append((turn_score, turn))

    return _best_turn(scores, bobs_turn)