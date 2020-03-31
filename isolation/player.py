import copy

class UserControlledPlayer:

    def __init__(self):
        pass

    def _get_choice(self, msg, board):
        s = input(msg)
        for i, c in enumerate(("A", "B", "C", "D", "E", "F", "G")):
            for j, k in enumerate(("0", "1", "2", "3", "4", "5", "6")):
                if s == f"{c}{k}":
                    return (i, j)

        return board.size, board.size

    def get_move(self, board):
        return self._get_choice("Enter your move (ex. A3):", board)

    def get_remove(self, board):
        return self._get_choice("Enter a cell to remove (ex. B3):", board)


def minimax(board, bob=True, depth=0):
    i = j = 0
    if bob:
        i, j = board.get_bob_pos()
    else:
        i, j = board.get_ann_pos()

    if depth == 3 and bob:
        myscore = board._count_ok(i, j)
        en_score = board._count_ok(*board.get_ann_pos())
        return -en_score + myscore, 0, 0, 0, 0

    if depth == 3:
        myscore = board._count_ok(i, j)
        en_score = board._count_ok(*board.get_bob_pos())
        return -myscore + en_score, 0, 0, 0, 0

    bob_isolated = not board.can_bob_move()
    ann_isolated = not board.can_ann_move()
    if bob_isolated and ann_isolated:
        return 0, 0, 0, 0, 0
    if ann_isolated:
        return 8, 0, 0, 0, 0
    if bob_isolated:
        return -8, 0, 0, 0, 0

    bob_mover = lambda b, x, y: b.move_bob(x, y)
    ann_mover = lambda b, x, y: b.move_ann(x, y)
    score = dict()
    enemy_pos_x = enemy_pos_y = None
    if bob:
        enemy_pos_x, enemy_pos_y = board.get_ann_pos()
    else:
        enemy_pos_x, enemy_pos_y = board.get_bob_pos()
    for pi in range(i-1, i+2):
        for pj in range(j-1, j+2):
            new_board = copy.deepcopy(board)
            mover = bob_mover if bob else ann_mover
            if mover(new_board, pi, pj):
                for ri in range(board.size()):
                    for rj in range(board.size()):
                        if abs(ri-enemy_pos_x) < 2 and abs(rj - enemy_pos_y) < 2:
                            if new_board.can_be_removed(ri, rj):
                                nb = copy.deepcopy(new_board)
                                nb.remove_cell(ri, rj)
                                v, _, _, _, _ = minimax(nb, (not bob), depth+1)
                                if bob and v == 8:
                                    return v, pi, pj, ri, rj
                                if not bob and v == -8:
                                    return v, pi, pj, ri, rj
                                score[v] = (pi, pj, ri, rj)

    v = max(score.keys()) if bob else min(score.keys())
    return v, score[v][0], score[v][1],  score[v][2],  score[v][3]


class RobotControlledPlayer:

    def __init__(self):
        self.remove_i = None
        self.remove_j = None

    def get_move(self, board):
        _, pi, pj, ri, rj = minimax(board, True)
        self.remove_i = ri
        self.remove_j = rj
        return pi, pj

    def get_remove(self, board):
        return self.remove_i, self.remove_j