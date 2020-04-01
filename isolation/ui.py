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

    def display(self, board):
        print("\n"*80, end="")
        n = board.size()
        ann_pos = board.get_ann_pos()
        bob_pos = board.get_bob_pos()
        ch = ["A", "B", "C", "D", "E", "F", "G"]
        print(" 0123456")
        for i in range(n):
            print(ch[i], end="")
            for j in range(n):
                if (i, j) == ann_pos:
                    print("◍", end="")
                    continue
                if (i, j) == bob_pos:
                    print("◆", end="")
                    continue
                if not board.is_empty(i, j):
                    print("◻", end="")
                    continue
                print(" ", end="")

            print()

    def draw(self):
        print("It's a draw!")

    def ann_won(self):
        print("Player ◍ has won!")

    def bob_won(self):
        print("Player ◆ has won!")