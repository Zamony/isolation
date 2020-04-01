import copy
from typing import NamedTuple


class Turn(NamedTuple):
    move_x: int
    move_y: int
    remove_x: int
    remove_y: int

    @classmethod
    def default(cls):
        return Turn(0, 0, 0, 0)


def minimax(board, maxdepth, maxscatter):
    return _minimax(board, maxdepth, maxscatter, True, 0)

def max_heuristic():
    # maximum number of possible ways to move
    return 8

def _minimax(board, maxdepth, maxscatter, bobs_turn, depth):
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

    score = dict()
    enemy_pos_x, enemy_pos_y = board.get_ann_pos() if bobs_turn else board.get_bob_pos()
    for pi in range(i-1, i+2):
        for pj in range(j-1, j+2):
            new_board = copy.deepcopy(board)
            moved = new_board.move_bob(pi, pj) if bobs_turn else new_board.move_ann(pi, pj)
            if not moved:
                continue
            for ri in range(board.size()):
                for rj in range(board.size()):
                    is_too_far = abs(ri-enemy_pos_x) >= maxscatter or abs(rj - enemy_pos_y) >= maxscatter
                    if is_too_far or not new_board.can_be_removed(ri, rj):
                        continue
                    nb = copy.deepcopy(new_board)
                    nb.remove_cell(ri, rj)
                    turn_score, turn = _minimax(nb, maxdepth, maxscatter, not bobs_turn, depth+1)
                    if bobs_turn and turn_score == max_heuristic():
                        return turn_score, Turn(pi, pj, ri, rj)
                    if not bobs_turn and turn_score == -max_heuristic():
                        return turn_score, Turn(pi, pj, ri, rj)
                    score[turn_score] = Turn(pi, pj, ri, rj)

    v = max(score.keys()) if bobs_turn else min(score.keys())
    return v, score[v]