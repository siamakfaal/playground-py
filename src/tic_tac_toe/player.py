from dataclasses import dataclass
from enum import Enum
from typing import Dict

import numpy as np

from tic_tac_toe.utils import Outcome, Play, Symbol, game_state, possible_moves


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


class MinMax(Player):
    @dataclass
    class BestMove:
        score: int | float = 0
        move: tuple = None

    def __init__(self, symbol: Symbol, max_depth: int = None):
        super().__init__(symbol)
        self.max_depth: int = max_depth

    def play(self, board: np.ndarray) -> Play:
        max_depth = self.max_depth if self.max_depth else np.prod(board.shape)
        minmax_move = self._minimax(board, max_depth, self.symbol)

        return Play(
            row=minmax_move.move[0], column=minmax_move.move[1], symbol=self.symbol, terminate=False
        )

    def _minimax(self, board: np.ndarray, depth: int, current_symbol: Symbol) -> BestMove:
        current_state, _ = game_state(board)

        if current_state == Outcome.O_WINS:
            return self.BestMove(score=1)
        elif current_state == Outcome.X_WINS:
            return self.BestMove(score=-1)
        elif current_state == Outcome.TIE or depth == 0:
            return self.BestMove(score=0)

        best_move = self.BestMove(
            score=float("-inf") if current_symbol == Symbol.O else float("inf")
        )

        for move in possible_moves(board):
            board[move] = current_symbol.value  # Make move for the current player
            score = self._minimax(board, depth - 1, self._next_symbol(current_symbol)).score
            board[move] = 0  # Undo move

            if self._compare(score, best_move.score, current_symbol):
                best_move.score = score
                best_move.move = move

        return best_move

    @staticmethod
    def _next_symbol(symbol: Symbol) -> Symbol:
        return Symbol.X if symbol == Symbol.O else Symbol.O

    @staticmethod
    def _compare(new_score: float, previous_score: float, symbol: Symbol) -> bool:
        return new_score > previous_score if symbol == Symbol.O else new_score < previous_score


class OutcomeOverHorizon(Player):
    def __init__(self, symbol: Symbol, horizon: int = None):
        """Initialize a AI player with a symbol (X or O)."""
        super().__init__(symbol)
        self.visited_states: Dict[tuple, OutcomeCount] = {}
        self.horizon = horizon

    def play(self, board: np.ndarray) -> Play:

        outcome_count = self._n_next_moves(board)

        best_move = None
        best_move_score = -float("inf")
        for move, count in outcome_count.items():
            wins = count.player(self.symbol)
            losses = count.opponent(self.symbol)
            score = wins - losses
            print(f"move: {move}, wins: {wins:4}, losses: {losses:4}, score: {score:4}")
            if score > best_move_score:
                best_move_score = score
                best_move = move

        print(f"Selected best move is {best_move}")
        return Play(best_move[0], best_move[1], self.symbol)

    def _n_next_moves(self, board: np.ndarray):
        horizon = self.horizon if self.horizon else board.shape[0]

        print(f"visited size before search: {len(self.visited_states)}")

        next_move_outcomes_for_horizon = {}
        for move in possible_moves(board):
            temp_board = board.copy()
            temp_board[move] = self.symbol.value
            if self._board_to_key(temp_board) in self.visited_states:
                next_move_outcomes_for_horizon[move] = self.visited_states[
                    self._board_to_key(temp_board)
                ]
            else:
                next_move_outcomes_for_horizon[move] = self._dfs(
                    -self.symbol.value, temp_board, 1, horizon, self.visited_states
                )

        print(f"visited size after search: {len(self.visited_states)}")
        return next_move_outcomes_for_horizon

    def _dfs(
        self,
        current_player: int,
        board: np.ndarray,
        depth: int,
        max_depth: int,
        visited_states: Dict[tuple, OutcomeCount],
    ) -> OutcomeCount:
        if depth > max_depth:
            return OutcomeCount()

        depth_outcome, _ = game_state(board)

        if depth_outcome != Outcome.ONGOING:
            count = OutcomeCount.from_outcome(depth_outcome)
            visited_states[self._board_to_key(board)] = count
            return count

        outcome_count = OutcomeCount()
        for move in possible_moves(board):
            new_board = board.copy()
            new_board[move] = current_player
            outcome_count += self._dfs(
                -current_player, new_board, depth + 1, max_depth, visited_states
            )

        visited_states[self._board_to_key(board)] = outcome_count
        return outcome_count

    @staticmethod
    def _board_to_key(board: np.ndarray) -> tuple:
        return tuple(board.flatten())
