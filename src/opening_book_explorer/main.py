import sqlite3
import chess

liste_fichier=["anti-siciliennes.sqlite","Debut_Reti.sqlite", "KIA.sqlite", "Rossolimo.sqlite", "Semi-slave.sqlite","Sicilienne Dragon.sqlite"]
def ask_opening():
    c="0"
    while not c.isdigit() or not (1 <= int(c) and int(c)<= len(liste_fichier)):
        print("merci de choisir une ouverture")
        c=input(f"choisir ouverture:\n" "1- anti-siciliennes\n" "2- Debut_Reti\n" "3- KIA\n" "4- Rossolimo\n" "5- Semi-slave\n" "6- Sicilienne Dragon\n")
    return c
    #position de départ echiquier fen : rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -

def find_moves_from_fen(fen):
    req=("SELECT * FROM positions where fromfen = '"+fen+"'") 
    result=cur.execute(req)
    liste_coups = []
    rows = result.fetchall()
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
    if not moves:
        print("fin de l'ouverture")
    else:
        for i in range(len(moves)):
            print(f"coup possible : {i} --> {moves[i]}")
        choix = input("Choisir un coup à jouer : ")
        while not choix.isdigit() or not (0 <= int(choix) and int(choix)<= len(moves)-1):
            for i in range(len(moves)):
                print(f"coup possible : {i} --> {moves[i]}")
            choix = input("Choisir un coup à jouer : ")
        board.push_san(moves[int(choix)])
        current_fen = board.fen()[:-4] 



conn.close()