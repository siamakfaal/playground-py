from rich.console import Console

from tic_tac_toe.player import Player
from tic_tac_toe.utils import MAP, Outcome, Play, create_board, game_state


class TicTacToe:
    def __init__(self, board_size: int, player_1: Player, player_2: Player):
        self.players = [player_1, player_2]
        self.board_size = board_size
        self.board = create_board(board_size)
        self.console = Console()

    def play(self):
        turn = 0
        state = Outcome.ONGOING
        while state == Outcome.ONGOING:
            self.print_board()
            print(f"Player {turn+1} make your move: ")
            move = self.players[turn].play(self.board)
            if self.update(move):
                state = game_state(self.board)
                turn = (turn + 1) % 2
            else:
                print("Invalid Move! Try again")
        self.print_board()
        print(f"{state.name = }")

    def update(self, move: Play) -> bool:
        if 0 <= move.row < self.board_size and 0 <= move.column < self.board_size:
            if self.board[move.row, move.column] == 0:
                self.board[move.row, move.column] = move.symbol.value
                return True
        return False

    def print_board(self) -> None:
        self.console.clear()
        for i, row in enumerate(self.board):
            row_str = " | ".join(f"[{MAP[tile]['style']}]{MAP[tile]['symbol']}[/]" for tile in row)
            self.console.print(row_str)
            if i < self.board_size - 1:
                self.console.print("-" * (self.board_size * 4 - 3))
        self.console.print()
