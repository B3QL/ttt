from copy import deepcopy
from itertools import chain


class GameState:
    BOARD_SIZE = 3
    EMPTY_SYMBOL = None

    def __init__(self, state=None):
        row = [self.EMPTY_SYMBOL] * self.BOARD_SIZE
        self._state = state or [list(row) for _ in range(self.BOARD_SIZE)]

    def put_symbol(self, cell, symbol):
        next_state = deepcopy(self._state)
        row, col = self._get_index(cell)
        next_state[row][col] = symbol
        return GameState(next_state)

    def _get_index(self, cell_number):
        row, col = divmod(cell_number - 1, self.BOARD_SIZE)
        return row, col

    def cell(self, cell_number):
        row, col = self._get_index(cell_number)
        return self._state[row][col]

    @property
    def rows(self):
        return deepcopy(self._state)

    @property
    def cols(self):
        return list(zip(*deepcopy(self._state)))

    @property
    def diagonal(self):
        return list(self._state[i][i] for i in range(self.BOARD_SIZE))

    @property
    def antidiagonal(self):
        max_index = self.BOARD_SIZE - 1
        return list(self._state[max_index - i][i] for i in range(self.BOARD_SIZE))

    @property
    def is_full(self):
        return not bool(self.empty_cells)

    @property
    def empty_cells(self):
        start, stop = 1, self.BOARD_SIZE ** 2
        return [cell for cell in range(start, stop + 1) if self.cell(cell) is self.EMPTY_SYMBOL]

    def __str__(self):
        line = ' -' * (1 + 2 * self.BOARD_SIZE)
        sep = ' | '
        board = [line]
        for row in self._state:
            format_row = map(lambda x: str(x) if x != self.EMPTY_SYMBOL else ' ', row)
            board.append(sep + sep.join(format_row) + sep)
            board.append(line)
        return '\n'.join(board)

    def _state_repr(self):
        return ''.join(map(lambda x: str(x) if x != self.EMPTY_SYMBOL else '-', chain(*self._state)))

    def __repr__(self):
        return '<{0.__class__.__name__} {0.BOARD_SIZE}x{0.BOARD_SIZE} [{1}]>'.format(self, self._state_repr())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self._state_repr())


class GameLogic:
    X = 'x'
    O = 'o'
    def __init__(self):
        self._player = self.X
        self._state = GameState()

    @property
    def state(self):
        return self._state

    @property
    def has_ended(self):
        return self._state.is_full or bool(self.winner)

    @property
    def winner(self):
        patterns = [
            *self._state.rows,
            *self._state.cols,
            self._state.diagonal,
            self._state.antidiagonal
        ]
        non_empty = filter(lambda p: all(p), patterns)
        winning = list(filter(self._same_values, non_empty))
        if winning:
            return winning[0][0]
        return None

    def _same_values(self, iterable):
        iterator = iter(iterable)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(map(lambda elem: elem == first, iterator))

    def putX(self, cell):
        return self._make_move(cell, self.X)

    def putO(self, cell):
        return self._make_move(cell, self.O)

    def _make_move(self, cell, symbol):
        if self._player != symbol:
            return False

        if self._state.cell(cell):
            return False

        if self.winner is not None:
            return False

        self._state = self._state.put_symbol(cell, symbol)
        self._player, = self._next_player(symbol)
        return True

    def _next_player(self, symbol):
        players = {self.X, self.O}
        return players - {symbol}

    def __str__(self):
        return str(self._state)

    def __repr__(self):
        return '<{0.__class__.__name__} player: {0._player}>'.format(self)