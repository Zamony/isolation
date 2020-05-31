import unittest
from unittest.mock import Mock, patch
import pygame as pg
from isolation import run_game, Board, Cell, Winner


class TestGame(unittest.TestCase):

    def setUp(self):
        pg.display.set_mode = Mock(wraps=pg.Surface)
        pg.display.set_caption = Mock()
        pg.display.update = Mock()

        self.board = Board()

    @patch.object(Board, '__new__')
    @patch.object(Board, '__init__')
    def test_draw(self, mock_init, mock_new):
        self.board.n = 2
        self.board.board = [
            [Cell.ann, Cell.ok],
            [Cell.none, Cell.bob],
        ]
        self.board.ann_pos = (0, 0)
        self.board.bob_pos = (1, 1)
        mock_new.return_value = self.board
        mock_init.return_value = None
        ann = Mock()
        ann.get_move.return_value = (0, 1)
        ann.get_remove.return_value = (0, 0)
        bob = Mock()
        winner = run_game(Mock(), ann, bob)
        self.assertEqual(winner, Winner.none)

    @patch.object(Board, '__new__')
    @patch.object(Board, '__init__')
    def test_ann(self, mock_init, mock_new):
        self.board.n = 3
        self.board.board = [
            [Cell.ann, Cell.ok, Cell.none],
            [Cell.ok, Cell.none, Cell.bob],
            [Cell.ok, Cell.none,Cell.none]
        ]
        self.board.ann_pos = (0, 0)
        self.board.bob_pos = (1, 2)
        mock_new.return_value = self.board
        mock_init.return_value = None
        ann = Mock()
        ann.get_move.return_value = (0, 1)
        bob = Mock()
        winner = run_game(Mock(), ann, bob)
        self.assertEqual(winner, Winner.player_a)

    @patch.object(Board, '__new__')
    @patch.object(Board, '__init__')
    def test_bob(self, mock_init, mock_new):
        self.board.n = 3
        self.board.board = [
            [Cell.ann, Cell.ok, Cell.none],
            [Cell.ok, Cell.none, Cell.bob],
            [Cell.none, Cell.none, Cell.none]
        ]
        self.board.ann_pos = (0, 0)
        self.board.bob_pos = (1, 2)
        mock_new.return_value = self.board
        mock_init.return_value = None
        ann = Mock()
        ann.get_move.return_value = (1, 0)
        ann.get_remove.return_value = (0, 0)
        bob = Mock()
        bob.get_move.return_value = (0, 1)
        winner = run_game(Mock(), ann, bob)
        self.assertEqual(winner, Winner.player_b)


if __name__ == '__main__':
    unittest.main()
