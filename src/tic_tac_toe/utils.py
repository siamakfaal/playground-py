from dataclasses import dataclass
from enum import Enum

import numpy as np
from rich.style import Style


class Outcome(Enum):
    X_WINS = 1
    O_WINS = 2
    TIE = 3
    ONGOING = 4

    def __str__(self):
        return self.name


class Symbol(Enum):
    X = -1
    O = 1

    def __str__(self):
        return self.name


MAP = {
    -1: {"symbol": "X", "style": Style(color="red", bold=True)},
    1: {"symbol": "O", "style": Style(color="blue", bold=True)},
    0: {"symbol": " ", "style": Style(color="white", bold=False)},
}


@dataclass
class Play:
    """Represents a move in the game."""

    row: int
    column: int
    symbol: Symbol


def create_board(board_size: int) -> np.ndarray:
    """Creates an empty board of given size."""
    return np.zeros((board_size, board_size), dtype=int)


def game_state(board: np.ndarray) -> Outcome:
    max_sum = board.shape[0]  # Winning sum

    def check_winner(sums):
        if max_sum in sums:
            return Outcome.O_WINS
        if -max_sum in sums:
            return Outcome.X_WINS
        return None

    # Check rows and columns
    row_sums = np.sum(board, axis=1)
    col_sums = np.sum(board, axis=0)

    for sums in [row_sums, col_sums]:
        winner = check_winner(sums)
        if winner:
            return winner

    # Check diagonals
    main_diag_sum = np.sum(np.diag(board))
    sec_diag_sum = np.sum(np.diag(np.fliplr(board)))

    for diag_sum in [main_diag_sum, sec_diag_sum]:
        if diag_sum == max_sum:
            return Outcome.O_WINS
        if diag_sum == -max_sum:
            return Outcome.X_WINS

    # Check for ongoing game
    if 0 in board:
        return Outcome.ONGOING

    # Otherwise, it's a tie
    return Outcome.TIE
