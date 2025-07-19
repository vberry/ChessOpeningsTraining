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
 
def move_list_to_string(lst):
    print("Current moves list of the game")
    for i in range(len(lst)):
        if i % 2 == 0:
            if i+1 < len(lst):
                print(f"{i//2 +1}.{lst[i]} {lst[i+1]}")
            else:
                print(f"{i//2+1}.{lst[i]}")
 
 
def reverseString(string):
    return "".join(list(reversed(string)))
 
def printBoard(reverse=False):
    txt=str(board)
    lines=txt.split("\n")
    txt2=""
    for i in range(8):
        txt2+=str(8-i)+"│"+lines[i]+"│"+str(8-i)+"\n"
    txt="  A B C D E F G H  \n"+"  ───────────────  \n"+txt2+"  ───────────────  \n"+"  A B C D E F G H  "
 
    if reverse:
        lines=txt.split("\n")
        lines=[reverseString(string) for string in reversed(lines)]
        txt="\n".join(lines)
    print(f"------------------\n{txt}\n------------------")
 
 
 
 
# MAIN
c=ask_opening()
chess_color=ask_color()
current_player=1
conn = sqlite3.connect(rf"..\..\openings\{books[int(c)-1]}")  
cur = conn.cursor()
current_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"
board = chess.Board(current_fen)
ob_moves = ['something to enter while']
move_list=[]
 
good_moves=0
current_life=10
 
printBoard(reverse=(chess_color==2))
while True:
    print("current_life=",current_life)
    legal_moves_lst = [ board.san(move) for move in board.legal_moves ]
    ob_moves = find_moves_from_fen(current_fen)
    if ob_moves==[]:
        break
 
    chosenMove=None
    if current_player!=chess_color:
        chosenMove=random.choice(ob_moves)
        board.push_san(chosenMove)
        print(f'here is the move : {chosenMove}\nand here is the chessboard')
        printBoard(reverse=(chess_color==2))
        move_list.append((chosenMove))
        find_notes_from_fen(current_fen)
 
    else:
        wrong_moves=0
        while wrong_moves<3:
            choice = input("Choosing a move to play : ")
            while not choice in legal_moves_lst:
                choice = input("Please enter a legal move: ")
            if choice not in ob_moves:
                wrong_moves += 1
                print(f"wrong moves = {wrong_moves}")
            else:
                break
 
        if wrong_moves==3:
            current_life-=1
            print(f"you lose one life = {current_life}")
            for i in range(len(ob_moves)):
                print(f"possible move : {ob_moves[i]}")
            choice = input("You have lost 3 times choose a move to play : ")
            while not choice in ob_moves:
                choice = input("You have lost 3 times choose in the menu a move to play : ")
 
        else:
            good_moves+=1  
 
        chosenMove=choice
        board.push_san(chosenMove)
        print(f"Good move!")
        move_list.append((chosenMove))
        find_notes_from_fen(current_fen)
 
 
 
    current_fen = board.fen()[:-4]
    if current_player==1:
        current_player=2
    else:
        current_player=1        
    move_list_to_string(move_list)
 
 
 
 
conn.close()
print("Congratulation you reached the opening end!")
print(f"")#to do: print good moves bad moves and current life