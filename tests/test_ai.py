import random
import unittest
from unittest import mock

from isolation import Player, RobotControlledPlayer, run_game, Winner, ai


class RandomControlledPlayer(Player):

    def __init__(self):
        self.rx = 0
        self.ry = 0

    def get_move(self, my_position, board):
        x, y = board.get_ann_pos()
        i = j = None
        while True:
            i = random.randint(x-1, x+1)
            j = random.randint(y-1, y+1)
            if board.move_ann(i, j):
                break
        for p in range(board.size()):
            for s in range(board.size()):
                if board.can_be_removed(p, s):
                    self.rx = p
                    self.ry = s
                    return i, j

    def get_remove(self, board):
        return self.rx, self.ry


class TestAI(unittest.TestCase):

    def test_ai(self):
        nvictory = 0
        total = 10
        for _ in range(total):
            player_a = RandomControlledPlayer()
            player_b = RobotControlledPlayer(ai.Difficulty.hard)
            winner = run_game(mock.Mock(), player_a, player_b)
            if winner == Winner.player_b:
                nvictory += 1

        print(nvictory)
        self.assertTrue(nvictory > total//2)
