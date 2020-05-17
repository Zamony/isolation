import unittest
from unittest.mock import Mock
import pygame as pg
from isolation import GUI, Board


class TestGUI(unittest.TestCase):

    def setUp(self):
        self.board = Board()

        pg.display.set_mode = Mock(wraps=pg.Surface)
        pg.display.set_caption = Mock()
        pg.display.update = Mock()
        self.ui = GUI()

    def tearDown(self):
        if pg.get_init():
            pg.quit()

    def test_pg_init(self):
        self.assertTrue(pg.get_init())

    def test_display(self):
        self.ui.display(self.board)
        ann_pos = self.board.get_ann_pos()
        ann_screen_pos = self.ui.board2screen(ann_pos, self.board.size())
        ann = self.ui.screen.subsurface(pg.Rect(*ann_screen_pos, *self.ui.cell_size)).copy()
        ann_new_pos = ann_pos[0], ann_pos[1] + 1
        ann_screen_new_pos = self.ui.board2screen(ann_new_pos, self.board.size())
        old_ann = self.ui.screen.subsurface(pg.Rect(*ann_screen_new_pos, *self.ui.cell_size)).copy()

        self.board.move_ann(*ann_new_pos)
        self.assertNotEqual(ann.get_buffer().raw, old_ann.get_buffer().raw)
        self.ui.display(self.board)

        new_ann = self.ui.screen.subsurface(pg.Rect(*ann_screen_new_pos, *self.ui.cell_size)).copy()
        self.assertEqual(ann.get_buffer().raw, new_ann.get_buffer().raw)

    def test_draw(self):
        pg.event.post(pg.event.Event(pg.QUIT, dict()))
        self.ui.draw()
        self.assertFalse(pg.get_init())

    def test_ann_won(self):
        pg.event.post(pg.event.Event(pg.QUIT, dict()))
        self.ui.ann_won()
        self.assertFalse(pg.get_init())

    def test_bob_won(self):
        pg.event.post(pg.event.Event(pg.QUIT, dict()))
        self.ui.bob_won()
        self.assertFalse(pg.get_init())

    def test_info_img(self):
        empty_info = self.ui.info.copy()
        pos = self.ui.display_info_img(self.ui.WAIT_ICON)
        wait_info = self.ui.info.copy()
        self.assertNotEqual(empty_info.get_buffer().raw, wait_info.get_buffer().raw)

        w, h = self.ui.WAIT_ICON.get_width(), self.ui.WAIT_ICON.get_height()
        icon = self.ui.info.subsurface(pg.Rect(*pos, w, h)).copy()
        for i in range(w):
            for j in range(h):
                pixel2 = self.ui.WAIT_ICON.get_at((i, j))
                if pixel2.a == 255:
                    pixel1 = icon.get_at((i, j))
                    self.assertEqual(pixel1, pixel2)

    def test_info_text(self):
        empty_info = self.ui.info.copy()
        self.ui.display_info_text("Test")
        info = self.ui.info.copy()
        self.assertNotEqual(empty_info.get_buffer().raw, info.get_buffer().raw)

    def test_reser_info(self):
        empty_info = self.ui.info.copy()
        self.ui.reset_info()
        info = self.ui.info.copy()
        self.assertNotEqual(empty_info.get_buffer().raw, info.get_buffer().raw)


if __name__ == '__main__':
    unittest.main()
