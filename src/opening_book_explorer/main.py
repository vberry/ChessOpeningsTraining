import sqlite3
import chess

liste_fichier=["anti-siciliennes.sqlite","Debut_Reti.sqlite", "KIA.sqlite", "Rossolimo.sqlite", "Semi-slave.sqlite","Sicilienne Dragon.sqlite"]
def ask_opening():
    global c
    c="0"
    while not c.isdigit() or not (1 <= int(c) and int(c)<= 6):
        print("merci de choisir une ouverture")
        c=input(f"choisir ouverture:\n" "1- anti-siciliennes\n" "2- Debut_Reti\n" "3- KIA\n" "4- Rossolimo\n" "5- Semi-slave\n" "6- Sicilienne Dragon\n")
    return c
    #position de départ echiquier fen : rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -

def find_moves_from_fen(fen):
    req=("SELECT * FROM positions where fromfen = '"+fen+"'") 
    result=cur.execute(req)
    liste_coups = []
    rows = result.fetchall()
    liste_coups = []
    for row in rows:
        liste_coups.append(row[2])
    return liste_coups


# MAIN 

c=ask_opening()
conn = sqlite3.connect(rf"..\..\openings\{liste_fichier[int(c)-1]}")  
cur = conn.cursor()

current_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"
board = chess.Board(current_fen)
moves = ['something to enter while']
while moves:
    moves = find_moves_from_fen(current_fen)
    for i in range(len(moves)):
        print(f"coup possible : {i} --> {moves[i]}")
    choix = int(input("Choisir un coup à jouer : "))
    board.push_san(moves[choix])
    current_fen = board.fen()
    #test pour retrouver une fen depuis un coup
    # for row in rows:
    #     if row[2]==liste_coups[int(choix)]:
    #         print(row[1])
    #             #fen_suivante=rows[1]
    #test pour jouer coup
    # board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")
    # print(board)
    # coup = chess.Move.from_uci(liste_coups[i])

    #problème il fait mettre la case d'avant le coup dans chess.Move.from_uci trouver solution avec chess


    # board.push(coup)
    # print("")
    # print(board)
        
    
find_fen()

