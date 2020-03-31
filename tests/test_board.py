import unittest

from isolation import Board, Cell


class TestBoard(unittest.TestCase):

    def test_can_move(self):
        b = Board()
        b.n = 2

        b.ann_pos = (0, 0)
        b.board = [
            [Cell.ann, Cell.none],
            [Cell.none, Cell.none],
        ]
        self.assertFalse(b.can_ann_move())

        b.ann_pos = (1, 0)
        b.board = [
            [Cell.none, Cell.none],
            [Cell.ann, Cell.none],
        ]
        self.assertFalse(b.can_ann_move())

        b.ann_pos = (1, 1)
        b.board = [
            [Cell.none, Cell.none],
            [Cell.none, Cell.ann],
        ]
        self.assertFalse(b.can_ann_move())

        b.ann_pos = (0, 1)
        b.board = [
            [Cell.none, Cell.ann],
            [Cell.none, Cell.none],
        ]
        self.assertFalse(b.can_ann_move())

        b.ann_pos = (0, 1)
        b.board = [
            [Cell.bob, Cell.ann],
            [Cell.none, Cell.none],
        ]
        self.assertFalse(b.can_ann_move())

        b.ann_pos = (0, 1)
        b.board = [
            [Cell.bob, Cell.ann],
            [Cell.ok, Cell.none],
        ]
        self.assertTrue(b.can_ann_move())

        b.n = 3
        b.ann_pos = (1, 1)
        b.board = [
            [Cell.none, Cell.none, Cell.none],
            [Cell.bob, Cell.ann, Cell.none],
            [Cell.none, Cell.none, Cell.none],
        ]
        self.assertFalse(b.can_ann_move())

    def test_move(self):
        b = Board()
        x, y = b.get_ann_pos()
        new_pos = (x-1, y)
        moved = b.move_ann(*new_pos)
        self.assertTrue(moved)
        self.assertTrue(b.get_ann_pos() == new_pos)
        self.assertTrue(b.board[x][y] == Cell.ok)
        self.assertFalse(b.move_ann(*new_pos))
        self.assertFalse(b.move_ann(100, 110))

    def test_remove(self):
        b = Board()
        x, y = b.get_ann_pos()
        self.assertTrue(b.remove_cell(0, 0))
        self.assertFalse(b.remove_cell(0, 0))
        self.assertFalse(b.remove_cell(x, y))
        self.assertFalse(b.remove_cell(100, 100))


if __name__ == '__main__':
    unittest.main()
