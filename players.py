from collections import defaultdict
from random import choice, random


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


class QLearningPlayer:
    def __init__(self, learning_rate=0.1, discount_factor=0.1, exploration_factor=0.1):
        self._alpha = learning_rate
        self._gamma = discount_factor
        self._eps = exploration_factor
        self._q_table = defaultdict(dict)
        self._last = None

    def make_move(self, game, put_symbol):
        state = game.state
        best_action = self._pi(state)
        if random() < self._eps or best_action is None:
            best_action = choice(state.empty_cells)
            self._q_table[state][best_action] = 0

        result = put_symbol(best_action)
        if result:
            next_state = game.state
            self._last = (state, next_state, best_action)
            self._learn(*self._last)
        return result

    def reward(self, value):
        self._learn(*self._last, reward=value)
        self._last = None

    def _learn(self, state, next_state, action, reward=0):
        try:
            rate_action = self._Q(next_state, self._pi(next_state))
        except KeyError:
            rate_action = 0

        learned_value = reward + self._gamma * rate_action
        self._q_table[state][action] = (1 - self._alpha) * self._Q(state, action) + self._alpha * learned_value

    def _Q(self, state, action):
        return self._q_table.get(state, {})[action]

    def _pi(self, state):
        best = None
        actions = self._q_table.get(state, {}).keys()
        if actions:
            score, best = max((self._Q(state, action), action) for action in actions)
        return best

    @property
    def q_table(self):
        return self._q_table