import sqlite3
import chess
import os
import random
books_file='../../openings'
bf=os.listdir(books_file)
books=[]
for file in bf:
    if file.endswith('.sqlite'):
        books.append(file) 
def ask_opening():
    c="0"
    while not c.isdigit() or not (1 <= int(c) and int(c)<= len(books)):
        for i in range(len(books)):
            print(f"{i+1} -  {books[i]}")
        c = input("Choose an opening: ")
    return c
    #starting position of the board rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -
def ask_color():
    color="0"
    while not color.isdigit() or not (1 <= int(color) and int(color)<= 2):
        color = input(f"\n1-White\n2-Black\nChoose a color : ")
    if int(color)==1:
        return 1
    else:
        return 2
 
 
def find_moves_from_fen(fen):
    req=("SELECT * FROM positions where fromfen = '"+fen+"'")
    result=cur.execute(req)
    move  = []
    rows = result.fetchall()
    for row in rows:
        move.append(row[2])
    return move  
 
def find_notes_from_fen(fen):
    req=("SELECT * FROM notes where fromfen = '"+fen+"'")
    result=cur.execute(req)
    notes  = []
    rows = result.fetchall()
    for row in rows:
        notes.append(row[2])
    if notes!=[]:
        print (notes)

# MAIN
c=ask_opening()
chess_color=ask_color()
current_player=1
conn = sqlite3.connect(rf"..\..\openings\{books[int(c)-1]}")  
cur = conn.cursor()
current_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"
board = chess.Board(current_fen)
moves = ['something to enter while']
move_list=[]
 
 
while True:
    moves = find_moves_from_fen(current_fen)
    if moves==[]:
        break
 
    chosenMove=None
 
    if current_player!=chess_color:
        chosenMove=random.choice(moves)
        board.push_san(chosenMove)
        print(f'here the action : {chosenMove}\nand here is the chessboard')
        print(f"------------------\n{board}\n------------------")

    else:
        for i in range(len(moves)):
            print(f"possible move : {i} --> {moves[i]}")
        choix = input("Choosing a move to play : ")
        while not choix.isdigit() or not (0 <= int(choix) and int(choix)<= len(moves)-1):
            for i in range(len(moves)):
                print(f"possible move : {i} --> {moves[i]}")
            choix = input("Choosing a move to play: ")
        chosenMove=moves[int(choix)]
        board.push_san(chosenMove)


    current_fen = board.fen()[:-4]
    find_notes_from_fen(current_fen)
    if current_player==1:
        current_player=2
    else:
        current_player=1
 
    move_list.append((current_player,chosenMove))
    print(move_list)
 
 
 
 
conn.close()