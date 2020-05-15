"""
Module AI implements minimax algorithm
"""

import copy
import random
import dataclasses
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


@dataclasses.dataclass
class MinimaxState:
    scatter: int
    depth: int
    alpha: int
    beta: int


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
    state = MinimaxState(scatter=1, depth=0, alpha=-inf, beta=inf)
    return _minimax(board, maxdepth, True, state)


def max_heuristic():
    # maximum number of possible ways to move
    return 8


def _best_turn(scores, is_bobs_turn):
    random.shuffle(scores)
    return max(scores) if is_bobs_turn else min(scores)


def _is_end_of_the_game(board, maxdepth, depth):
    if depth == maxdepth:
        return True
    return not board.can_bob_move() or not board.can_ann_move()


def _get_end_score(board, maxdepth, bobs_turn, depth):
    i, j = board.get_bob_pos() if bobs_turn else board.get_ann_pos()
    if depth == maxdepth and bobs_turn:
        my_score = board.count_ways_to_move(i, j)
        enemy_score = board.count_ways_to_move(*board.get_ann_pos())
        return -enemy_score + my_score

    if depth == maxdepth:
        my_score = board.count_ways_to_move(i, j)
        enemy_score = board.count_ways_to_move(*board.get_bob_pos())
        return -my_score + enemy_score

    bob_isolated = not board.can_bob_move()
    ann_isolated = not board.can_ann_move()
    if bob_isolated and ann_isolated:
        return 0
    if ann_isolated:
        return max_heuristic()
    return -max_heuristic()


def _minimax(board, maxdepth, bobs_turn, state):
    if _is_end_of_the_game(board, maxdepth, state.depth):
        return _get_end_score(board, maxdepth, bobs_turn, state.depth), Turn.default()

    scores = []
    i, j = board.get_bob_pos() if bobs_turn else board.get_ann_pos()
    enemy_pos_x, enemy_pos_y = board.get_ann_pos() if bobs_turn else board.get_bob_pos()
    # heading towards the enemy at the start of the game (better for alpha-beta pruning)
    for pi in range(i+1, i-2, -1):
        for pj in range(j-1, j+2):
            new_board = copy.deepcopy(board)
            moved = new_board.move_bob(pi, pj) if bobs_turn else new_board.move_ann(pi, pj)
            if not moved:
                continue
            for ri in range(enemy_pos_x-state.scatter, enemy_pos_x+state.scatter+1):
                for rj in range(enemy_pos_y-state.scatter, enemy_pos_y+state.scatter+1):
                    if not new_board.can_be_removed(ri, rj):
                        continue
                    nb = copy.deepcopy(new_board)
                    nb.remove_cell(ri, rj)
                    new_state = MinimaxState(state.scatter, state.depth+1, state.alpha, state.beta)
                    turn_score, _ = _minimax(nb, maxdepth, not bobs_turn, new_state)
                    scores.append((turn_score, Turn(pi, pj, ri, rj)))
                    if bobs_turn:
                        state.alpha = max(state.alpha, turn_score)
                    else:
                        state.beta = min(state.beta, turn_score)
                    if state.alpha > state.beta:
                        return _best_turn(scores, bobs_turn)

    # if removal heuristic didn't work
    if len(scores) < 1:
        new_state = MinimaxState(state.scatter+1, state.depth, state.alpha, state.beta)
        turn = _minimax(board, maxdepth, bobs_turn, new_state)
        scores.append(turn)

    return _best_turn(scores, bobs_turn)
