from random import choice


class RandomPlayer:
    def make_move(self, game, put_symbol):
        cell = choice(game.state.empty_cells)
        return put_symbol(cell)


class HumanPlayer:
    def make_move(self, game, put_symbol):
        print(game.state)
        cell = None
        while not cell:
            try:
                cell = int(input('Choose cell [1-9]: '))
            except ValueError:
                pass
        return put_symbol(cell)
