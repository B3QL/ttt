from itertools import cycle
from logic import GameLogic


def play(x_player, o_player):
    game = GameLogic()
    players = cycle([
        (x_player, game.putX),
        (o_player, game.putO)
    ])

    player, make_action = next(players)
    while not game.has_ended:
        if player.make_move(game, make_action):
            player, make_action = next(players)
    return game


if __name__ == '__main__':
    from players import RandomPlayer, HumanPlayer
    game = play(RandomPlayer(), HumanPlayer())
    print('Winner:', game.winner)