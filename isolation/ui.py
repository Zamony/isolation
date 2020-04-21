import abc

class UI(abc.ABC):

    @abc.abstractmethod
    def display(self, board):
        pass

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def ann_won(self):
        pass

    @abc.abstractmethod
    def bob_won(self):
        pass


class TUI(UI):
    BOARD_DIGITS_GRID = "  0123456"
    ANN_ICON = "◍"
    BOB_ICON = "◆"

    def display(self, board):
        print("\n"*80, end="")
        n = board.size()
        ann_pos = board.get_ann_pos()
        bob_pos = board.get_bob_pos()
        ch = ["A", "B", "C", "D", "E", "F", "G"]
        print(self.BOARD_DIGITS_GRID)
        for i in range(n):
            print(ch[i] + " ", end="")
            for j in range(n):
                if (i, j) == ann_pos:
                    print(self.ANN_ICON, end="")
                    continue
                if (i, j) == bob_pos:
                    print(self.BOB_ICON, end="")
                    continue
                if not board.is_empty(i, j):
                    print("◻", end="")
                    continue
                print(" ", end="")

            print(" " + ch[i])
        print(self.BOARD_DIGITS_GRID)

    def draw(self):
        print("It's a draw!")

    def ann_won(self):
        print("Player %s has won!" % self.ANN_ICON)

    def bob_won(self):
        print("Player %s has won!" % self.BOB_ICON)
