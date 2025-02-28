from dataclasses import dataclass
from enum import Enum

import numpy as np

from tic_tac_toe.utils import Outcome, Play, Symbol, game_state


class Strategy(Enum):
    INF_HORIZON = 1


class Player:
    def __init__(self, symbol: Symbol):
        """Initialize the player with a given symbol (X or O)."""
        self.symbol = symbol


@dataclass
class OutcomeCount:
    X_wins: int = 0
    O_wins: int = 0
    Tie: int = 0

    @classmethod
    def from_outcome(cls, outcome: Outcome):
        if outcome == Outcome.X_WINS:
            return cls(X_wins=1, O_wins=0, Tie=0)
        elif outcome == Outcome.O_WINS:
            return cls(X_wins=0, O_wins=1, Tie=0)
        elif outcome == Outcome.TIE:
            return cls(X_wins=0, O_wins=0, Tie=1)
        elif outcome == Outcome.ONGOING:
            return cls(X_wins=0, O_wins=0, Tie=0)
        else:
            raise ValueError("Invalid outcome")

    def __add__(self, other):
        if not isinstance(other, OutcomeCount):
            return NotImplemented
        return OutcomeCount(
            self.X_wins + other.X_wins, self.O_wins + other.O_wins, self.Tie + other.Tie
        )

    def player(self, symbol: Symbol) -> int:
        """Returns the win count for the given player's symbol."""
        outcomes = {Symbol.X: self.X_wins, Symbol.O: self.O_wins}
        return outcomes.get(symbol, 0)  # Defaults to 0 if symbol is invalid

    def opponent(self, symbol: Symbol) -> int:
        """Returns the win count for the opponent of the given symbol."""
        outcomes = {Symbol.X: self.O_wins, Symbol.O: self.X_wins}
        return outcomes.get(symbol, 0)  # Defaults to 0 if symbol is invalid


class HumanPlayer(Player):
    def __init__(self, symbol: Symbol):
        """Initialize a human player with a symbol (X or O)."""
        super().__init__(symbol)

    def play(self, board: np.ndarray) -> Play:
        """Get a valid move from the human player."""
        while True:
            raw_input = input(
                f"Enter row and column to place {self.symbol} (row,column) or 'q' to quit: "
            ).strip()

            if raw_input == "q":
                return Play(0, 0, self.symbol, True)

            parts = raw_input.split(",")

            # Validate input format
            if len(parts) != 2:
                print(f"Invalid input: '{raw_input}'. Please enter row,column (e.g., 1,2).")
                continue

            try:
                row, column = map(int, parts)  # Convert input to integers
                if 0 <= row < board.shape[0] and 0 <= column < board.shape[1]:
                    return Play(row, column, self.symbol)
                else:
                    print(
                        f"Coordinates out of bounds. Please enter values between 0 and {board.shape[0] - 1}."
                    )
            except ValueError:
                print(
                    f"Invalid entry: '{raw_input}'. Please enter two numbers separated by a comma."
                )


class ArtificialPlayer(Player):
    def __init__(self, symbol: Symbol, strategy: Strategy = Strategy.INF_HORIZON):
        """Initialize a AI player with a symbol (X or O)."""
        super().__init__(symbol)
        self.strategy = strategy

    def play(self, board: np.ndarray) -> Play:

        if self.strategy == Strategy.INF_HORIZON:
            return self.infinite_horizon_search(board)

    def infinite_horizon_search(self, board: np.ndarray) -> Play:
        horizon = board.shape[0]
        horizon = 100
        outcome_count = self._n_next_moves(board, horizon)

        best_move = None
        best_move_score = None
        for move, count in outcome_count.items():
            wins = count.player(self.symbol)
            losses = count.opponent(self.symbol)
            ties = count.Tie
            score = wins - losses
            print(f"move: {move:2}, wins: {wins:4}, losses: {losses:4}, score: {score:4}")
            if not best_move_score or score > best_move_score:
                best_move_score = score
                best_move = move

        print(f"Selected best move is {best_move}")

        row, col = np.unravel_index(best_move, board.shape)
        return Play(row, col, self.symbol)

    def _n_next_moves(self, board: np.ndarray, horizon: int):

        next_move_outcomes_for_horizon = {}
        for move in possible_moves(board):
            temp_board = board.copy()
            temp_board[np.unravel_index(move, board.shape)] = self.symbol.value
            next_move_outcomes_for_horizon[move] = dfs(-self.symbol.value, temp_board, 1, horizon)

        return next_move_outcomes_for_horizon


def possible_moves(board: np.ndarray) -> list:
    return [idx for idx in range(board.size) if board[np.unravel_index(idx, board.shape)] == 0]


def dfs(current_player: int, board: np.ndarray, depth: int, max_depth: int) -> OutcomeCount:
    if depth > max_depth:
        return OutcomeCount()

    depth_outcome, _ = game_state(board)

    if depth_outcome != Outcome.ONGOING:
        return OutcomeCount.from_outcome(depth_outcome)

    outcome_count = OutcomeCount()
    for move in possible_moves(board):
        new_board = board.copy()
        new_board[np.unravel_index(move, board.shape)] = current_player
        outcome_count += dfs(-current_player, new_board, depth + 1, max_depth)

    return outcome_count
