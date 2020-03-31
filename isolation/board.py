import enum


class Cell(enum.Enum):
    none = 0
    ok = 1
    ann = 2
    bob = 3


class Board:
    def __init__(self):
        self.n = 7  # standard board size
        self.board = [[Cell.ok for _ in range(self.n)] for _ in range(self.n)]
        self.board[0][self.n // 2] = Cell.bob
        self.board[self.n - 1][self.n // 2] = Cell.ann
        self.bob_pos = (0, self.n // 2)
        self.ann_pos = (self.n - 1, self.n // 2)

    def size(self):
        return self.n

    def _neighbours(self, i, j):
        nb = []
        if i - 1 >= 0 and j - 1 >= 0:
            nb.append(self.board[i-1][j-1])
        if j - 1 >= 0:
            nb.append(self.board[i][j-1])
        if i + 1 < self.n and j - 1 >= 0:
            nb.append(self.board[i+1][j-1])
        if i - 1 >= 0:
            nb.append(self.board[i-1][j])
        if i + 1 < self.n:
            nb.append(self.board[i+1][j])
        if i - 1 >= 0 and j + 1 < self.n:
            nb.append(self.board[i-1][j+1])
        if j + 1 < self.n:
            nb.append(self.board[i][j+1])
        if i + 1 < self.n and j + 1 < self.n:
            nb.append(self.board[i+1][j+1])

        return nb

    def _count_ok(self, i, j):
        return self._neighbours(i, j).count(Cell.ok)

    def _find(self, who):
        if who == Cell.ann:
            return self.ann_pos
        return self.bob_pos

    def _move_player(self, who, x, y):
        i, j = self._find(who)
        if x == i and y == j:
            return False

        if abs(i - x) > 1 or abs(j - y) > 1:
            return False

        if x >= self.n or x < 0 or y >= self.n or y < 0:
            return False

        if self.board[x][y] != Cell.ok:
            return False

        self.board[x][y] = who
        self.board[i][j] = Cell.ok

        if who == Cell.ann:
            self.ann_pos = (x, y)
        else:
            self.bob_pos = (x, y)

        return True

    def move_ann(self, x, y):
        return self._move_player(Cell.ann, x, y)

    def move_bob(self, x, y):
        return self._move_player(Cell.bob, x, y)

    def _can_player_move(self, who):
        i, j = self._find(who)
        return Cell.ok in self._neighbours(i, j)

    def can_ann_move(self):
        return self._can_player_move(Cell.ann)

    def can_bob_move(self):
        return self._can_player_move(Cell.bob)

    def can_be_removed(self, x, y):
        if x >= self.n or x < 0 or y >= self.n or y < 0:
            return False
        if self.board[x][y] != Cell.ok:
            return False
        return True

    def remove_cell(self, x, y):
        if not self.can_be_removed(x, y):
            return False
        self.board[x][y] = Cell.none
        return True

    def get_ann_pos(self):
        return self.ann_pos

    def get_bob_pos(self):
        return self.bob_pos

    def is_empty(self, x, y):
        if x >= self.n or x < 0 or y >= self.n or y < 0:
            return True
        return self.board[x][y] == Cell.none

