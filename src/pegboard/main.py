from pegboard.pegboard import Pegboard

board = Pegboard(bin_size=7)
result = board.simulate(iter=200, animate=True)

board.plot(result)
print(f"exp size = {sum(result)}, \n {result = }")
