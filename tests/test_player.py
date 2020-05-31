import unittest
import pygame as pg
from unittest.mock import Mock, patch
from isolation import UserControlledPlayer, GUI, Board, Cell


class TestUserControlPlayer(unittest.TestCase):

    def setUp(self):
        pg.display.set_mode = Mock(wraps=pg.Surface)
        pg.display.set_caption = Mock()
        pg.display.update = Mock()
        self.ui = GUI()
        self.ui.display_cursor = Mock()

        self.board = Board()
        self.board.n = 2
        self.board.board = [
            [Cell.ann, Cell.ok],
            [Cell.none, Cell.none],
        ]

        self.player = UserControlledPlayer(self.ui, self.ui.ANN_ICON)

    def tearDown(self):
        pg.quit()

    def test_get_move(self):
        events = [
            pg.event.Event(pg.MOUSEBUTTONDOWN,
                           button=pg.BUTTON_LEFT,
                           pos=self.ui.board2screen((0, 1), self.board.size())),
            pg.event.Event(pg.QUIT),
        ]
        with patch('pygame.event', **{'get.return_value': events}):
            pos = self.player.get_move(self.board.get_ann_pos(), self.board)
            self.assertEqual(pos, (0, 1))
        with patch('pygame.event', **{'get.return_value': reversed(events)}):
            with self.assertRaises(SystemExit):
                self.player.get_move(self.board.get_ann_pos(), self.board)

    def test_get_remove(self):
        events = [
            pg.event.Event(pg.MOUSEBUTTONDOWN,
                           button=pg.BUTTON_LEFT,
                           pos=self.ui.board2screen((0, 1), self.board.size())),
            pg.event.Event(pg.QUIT),
        ]
        with patch('pygame.event', **{'get.return_value': events}):
            pos = self.player.get_remove(self.board)
            self.assertEqual(pos, (0, 1))
        with patch('pygame.event', **{'get.return_value': reversed(events)}):
            with self.assertRaises(SystemExit):
                self.player.get_remove(self.board)


if __name__ == '__main__':
    unittest.main()
