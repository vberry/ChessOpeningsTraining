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

def find_fen():
    c=ask_opening()
    current_fen="r1bqk1nr/pp2ppbp/2np2p1/2p5/4P3/2NP2P1/PPP2PBP/R1BQK1NR w KQkq -"
    conn = sqlite3.connect(rf"..\..\openings\{liste_fichier[int(c)-1]}")  
    cur = conn.cursor()
    req=("SELECT * FROM positions") 
    result=cur.execute(req)
    liste_coups = []
    rows = result.fetchall()
    for row in rows:
        if row[1]==current_fen:
            liste_coups.append(row[2])
    for i in range(len(liste_coups)):
        print(f"coup possible : {i} --> {liste_coups[i]}")
    choix = input("Choisir un coup à jouer : ")
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

