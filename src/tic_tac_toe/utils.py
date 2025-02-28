from dataclasses import dataclass
from enum import Enum
from typing import Tuple

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
    terminate: bool = False


@dataclass
class BoardSums:
    row: np.ndarray
    col: np.ndarray
    main_diag: int
    sec_diag: int


def create_board(board_size: int) -> np.ndarray:
    """Creates an empty board of given size."""
    return np.zeros((board_size, board_size), dtype=int)


def calculate_board_sums(board: np.ndarray) -> BoardSums:
    return BoardSums(
        np.sum(board, axis=1),
        np.sum(board, axis=0),
        np.sum(np.diag(board)),
        np.sum(np.diag(np.fliplr(board))),
    )


def game_state(board: np.ndarray) -> Tuple[Outcome, BoardSums]:
    max_sum = board.shape[0]  # Winning sum

    def check_winner(sums):
        if max_sum in sums:
            return Outcome.O_WINS
        if -max_sum in sums:
            return Outcome.X_WINS
        return None

    board_sums = calculate_board_sums(board)

    for sums in [board_sums.row, board_sums.col]:
        winner = check_winner(sums)
        if winner:
            return (winner, board_sums)

    for diag_sum in [board_sums.main_diag, board_sums.sec_diag]:
        if diag_sum == max_sum:
            return (Outcome.O_WINS, board_sums)
        if diag_sum == -max_sum:
            return (Outcome.X_WINS, board_sums)

    # Check for ongoing game
    if 0 in board:
        return (Outcome.ONGOING, board_sums)

    # Otherwise, it's a tie
    return (Outcome.TIE, board_sums)
