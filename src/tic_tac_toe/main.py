from tic_tac_toe.game import TicTacToe
from tic_tac_toe.player import HumanPlayer, MinMax, OutcomeOverHorizon
from tic_tac_toe.utils import Symbol


def main():
    player_1 = HumanPlayer(Symbol.O)
    player_2 = OutcomeOverHorizon(Symbol.X, horizon=1)
    # player_2 = MinMax(Symbol.X)

    game = TicTacToe(3, player_1, player_2)
    game.play()


if __name__ == "__main__":
    main()
