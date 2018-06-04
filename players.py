from random import randint


class RandomPlayer:
    def make_move(self, state):
        return randint(1, 9)


class HumanPlayer:
    def make_move(self, state):
        print(state)
        return int(input('Choose cell [1-9]: '))