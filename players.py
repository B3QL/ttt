from random import randint


class RandomPlayer:
    def make_move(self, state):
        return randint(1, 9)


class HumanPlayer:
    def make_move(self, state):
        print(state)
        cell = None
        while not cell:
            try:
                cell = int(input('Choose cell [1-9]: '))
            except ValueError:
                pass
        return cell