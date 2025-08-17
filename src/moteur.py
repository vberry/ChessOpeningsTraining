import sqlite3
import chess
import os
import random
 
# 1=BLANCS
# 2=NOIRS
 
class States:
    NORMAL= 0, #l'état au départ
    ILLEGAL=1, #le joueur vient de rentrer un coup illégal
    LEGAL_PAS_BON=2, #le joueur vient de rentrer un coup légal pas dans la base
 
 
def reversestring(string):
    return "".join(list(reversed(string)))
class Moteur:
    def __init__(self,path):
        self.path=path
        self.fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"
        self.board=chess.Board(self.fen)
        self.conn=None
        self.cur=None
        self.human=1
        self.current_player=1
        self.state=States.NORMAL
        self.wrong_moves=0
       
        self.txt="Voici votre plateau\n"+self.board_string()
 
    def display(self):
        return self.txt
 
    def get_book_list(self):
        return [f for f in os.listdir(self.path) if f.endswith('.sqlite')]
   
 
   
    def open_book(self,book):
        print(book)
        self.conn = sqlite3.connect(book,check_same_thread=False)  
        self.cur = self.conn.cursor()
        req=("SELECT * FROM positions where fromfen = '"+self.fen+"'")
        result=self.cur.execute(req)
        move  = []
        rows = result.fetchall()
        for row in rows:
            print("khkjhkjhkjh",row[2])
       
   
 
    def close_book(self):
        self.conn.close()
   
    def board_string(self,reverse=False):
        txt=str(self.board)
        lines=txt.split("\n")
        txt2=""
        for i in range(8):
            txt2+=str(8-i)+"│"+lines[i]+"│"+str(8-i)+"\n"
        txt="  A B C D E F G H  \n"+"  ───────────────  \n"+txt2+"  ───────────────  \n"+"  A B C D E F G H  "
        if reverse:
            lines=txt.split("\n")
            lines=[reversestring(string) for string in reversed(lines)]
            txt="\n".join(lines)
        return f"\n------------------\n{txt}\n------------------\n"
   
    def find_moves_from_fen(self):
        req=("SELECT * FROM positions where fromfen = '"+self.fen+"'")
        result=self.cur.execute(req)
        move  = []
        rows = result.fetchall()
        for row in rows:
            move.append(row[2])
        #print(f"-----------\n{move}\n------------")
        return move
 
 
    def find_notes_from_fen(self):
        req=("SELECT * FROM notes where fromfen = '"+self.fen+"'")
        result=self.cur.execute(req)
        notes  = []
        rows = result.fetchall()
        for row in rows:
            notes.append(row[2])
        if notes!=[]:
            print (notes)
   
    #Cette fonction est la fonction principale
    #C'est elle qui met à jour la plupart des variables
    def jouer_coup(self, move=None):
        legal_moves_lst = [ self.board.san(move) for move in self.board.legal_moves ]
        ob_moves = self.find_moves_from_fen()
       
        return_value=True
        #Distinguer si c'est l'humain ou la machine qui joue
        print("current player=",self.current_player,"human=",self.human)
        print("wrong_moves=",self.wrong_moves)
        #SI C'EST L'HUMAIN QUI JOUE
        if self.current_player==self.human:
 
         
            legal = [self.board.san(m) for m in self.board.legal_moves]
            if move not in legal:
                self.state=States.ILLEGAL
                self.txt+="COUP ILLEGAL\n"
                return False      
            else:
                if move not in ob_moves:
                    self.state=States.LEGAL_PAS_BON
                    self.wrong_moves+=1
                    self.txt+="COUP PAS DANS LA BASE\n"
                    if self.wrong_moves>=3:
                        self.txt+="Vous vous débrouillez mal. Voici la liste des coups possibles:\n"
                        self.txt+=str(ob_moves)
                    return False
 
               
               
               
 
 
                self.board.push_san(move)
                self.txt+=self.board_string(reverse=(self.human==2))
 
        else:
            #SI C'EST LA MACHINE
            print("la machine joue...")
            chosenMove=random.choice(ob_moves)
            print(chosenMove)
            self.board.push_san(chosenMove)
            self.txt+=f'here is the computer move : {chosenMove}\nand here is the chessboard'
            self.txt+=self.board_string(reverse=(self.human==2))
            #move_list.append((chosenMove))
            #find_notes_from_fen(fen)
       
       
       
        #A FAIRE DANS TOUS LES CAS
        self.fen = self.board.fen()[:-4]
        if self.current_player==1:
            self.current_player=2
        else:
            self.current_player=1
        return return_value
        self.state=Etats.NORMAL
        self.wrong_moves=0