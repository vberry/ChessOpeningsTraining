import chess
import chess.engine
# https://python-chess.readthedocs.io/en/latest/index.html

# pour avoir que le moteur :
# brew install stockfish
# brew info stockfish -> indique son chemin


# board = chess.Board()
# board.legal_moves
# board.push_san("e4")
# board.push_san("e5")
# board

# Fais jouer Stockfish contre lui même à 100 ms par coup :
engine = chess.engine.SimpleEngine.popen_uci(r"/opt/homebrew/Cellar/stockfish/16.1/bin/stockfish")

board = chess.Board()

while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    print(result.move)
    board.push(result.move)
    print(board) # description texte du board ! mais donne du SVG dans Jupyter

engine.quit()

