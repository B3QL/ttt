from itertools import cycle
from logic import GameLogic


REWARDS_X = {
    GameLogic.X: 1,
    GameLogic.O: -1,
    None: 0
}


REWARDS_O = {
    GameLogic.X: -1,
    GameLogic.O: 1,
    None: 0
}


def game_loop(x_player, o_player, reward):
    game = GameLogic()
    players = cycle([
        (x_player, game.putX),
        (o_player, game.putO)
    ])

    player, make_action = next(players)
    while not game.has_ended:
        if player.make_move(game, make_action):
            player, make_action = next(players)

    if reward:
        x_player.reward(REWARDS_X[game.winner])
        o_player.reward(REWARDS_O[game.winner])

    x_player.reset()
    o_player.reset()
    return game


def learn(x_player, o_player):
    return game_loop(x_player, o_player, reward=True)

def play(x_player, o_player):
    return game_loop(x_player, o_player, reward=False)


if __name__ == '__main__':
    from players import RandomPlayer, HumanPlayer
    game = play(RandomPlayer(), HumanPlayer())
    print('Winner:', game.winner)