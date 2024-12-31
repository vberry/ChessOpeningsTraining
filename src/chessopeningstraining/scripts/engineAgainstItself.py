
import chess
import chess.engine
# https://python-chess.readthedocs.io/en/latest/index.html

# To obtain the stockfish chess engine on Mac:
#    brew install stockfish
#    brew info stockfish -> indicates where the engine has been stored

# To run this program from the root folder of the project:
#     python3 src/chessopeningstraining/engineAgainstItself.py
# or  uv run  src/chessopeningstraining/engineAgainstItself.py

"""
This module shows how to load the stockfish chess engine and make it play against itself
"""

# No doctest as there is no function in this simple script.


# # ##########    MAIN   #################
if __name__ == "__main__":
    # Makes Stockfish play against itself with 100ms per move:
    engine = chess.engine.SimpleEngine.popen_uci(r"/opt/homebrew/Cellar/stockfish/16.1/bin/stockfish")

    board = chess.Board()
    # board.legal_moves
    # board.push_san("e4")
    # board.push_san("e5")

    while not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=0.1))
        print(result.move)
        board.push(result.move)
        print(board) # text description of the board! but gives SVG output when run in Jupyter

    engine.quit()

