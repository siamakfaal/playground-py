import numpy as np

from tic_tac_toe.utils import Play, Symbol


class Player:
    def __init__(self, symbol: Symbol):
        """Initialize the player with a given symbol (X or O)."""
        self.symbol = symbol


class HumanPlayer(Player):
    def __init__(self, symbol: Symbol):
        """Initialize a human player with a symbol (X or O)."""
        super().__init__(symbol)

    def play(self, board: np.ndarray) -> Play:
        """Get a valid move from the human player."""
        while True:
            raw_input = input(f"Enter row and column to place {self.symbol} (row,column): ").strip()
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
