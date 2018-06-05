from random import shuffle


class RandomPlayer:
    def __init__(self):
        self._valid_moves = list(range(1, 10))

    def make_move(self, state):
        shuffle(self._valid_moves)
        return self._valid_moves.pop()


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