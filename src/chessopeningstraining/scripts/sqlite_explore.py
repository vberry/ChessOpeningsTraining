# This is a warm up script that examines some content 
# of an opening book stored in a sqlite file


# TO DO : 
# voir comment passer des positions aux notes (que par le fen ?)
# voir aussi How do i get the played move by comparing two different fens? :
#https://stackoverflow.com/questions/66770587/how-do-i-get-the-played-move-by-comparing-two-different-fens


import sys
import sqlite3

con = sqlite3.connect('../../../openings/Semi-slave.sqlite')
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master")

##### LISTE DES TABLES
liste_tables = []
for tuple in cur.fetchall():
	liste_tables.append(tuple[0])	
print('Liste des tables :',liste_tables)
# -> ['positions', 'sqlite_autoindex_positions_1', 
#     'notes', 'sqlite_autoindex_notes_1', 
#     'priyomes', 'sqlite_autoindex_priyomes_1']

#### SCHEMA d'une TABLE :
print('Schema de la table -notes- :')
cur.execute("pragma table_info('notes')")
res = cur.fetchall()
for champ in res:
	print(champ)
 
###  TUPLES d'une TABLE : 
cur.execute("SELECT * FROM positions")
# -> les champs 'note' et 'glyph' ne sont jamais utilisés, il sont toujours vide
#print(cur.fetchone()) # en donne juste un
tuples_position = cur.fetchall()
print('nb de tuples dans table -positions- = ',len(tuples_position)) # donne les suivants
#print('Premier tuple de cette table :\n',tuples_position[0])

cur.execute("SELECT * from positions \
	where positions.fromfen='rnbqkb1r/pp2pppp/2p2n2/3p4/2PPP3/2N5/PP3PPP/R1BQKBNR b KQkq -'")
print('Position qui nous intéresse :',cur.fetchone())

# on cherche s'il y a des positions proches de celle du Gambit Marshall (pour laquelle on a une note mais pas de position)
for p in tuples_position:
	if p[1].startswith('rnbqkb1r/pp2pppp/2p2n2/3p4/2PPP3/2N5/PP3PPP/R1BQKBNR'):
		print(p)

cur.execute("SELECT title,frommoves FROM priyomes")
for t in cur.fetchall():
	print(t)

sys.exit(2)

## VALEURS pour un CHAMP d'une TABLE
print("Valeurs d'un champ d'une table :")
cur.execute("SELECT arrows FROM notes")
##res = cur.fetchall()
# les valeurs différentes constatées sont :
res = list(dict.fromkeys([ t[0] for t in cur.fetchall()]))
print(res)

# Notes pour une position
print("NOTES POUR UNE POSITION")
cur.execute("SELECT notes.note from notes,positions \
	where notes.fromfen=positions.fromfen \
	and positions.fromfen ='r2qkb1r/pp1npppp/2p2n2/3p1b2/8/3P1NP1/PPP1PPBP/RNBQ1RK1 w kq -'")
print(cur.fetchall())
##### Table NOTES :
# id
# fromfen : 'r2qkb1r/pp1npppp/2p2n2/3p1b2/8/3P1NP1/PPP1PPBP/RNBQ1RK1 w kq -'
# note : 'avec l'intention d'occuper le centre par ...e7-e5. Le défaut est que ce Cav occupe la case de repli du Cf6'
# arrows: TOUJOURS VIDE

##### Table PRIYOME (a Russian noun that is used directly and generically in English 
# to represent some sort of typical maneuver or technique)
# En fait ce sont des positions que j'avais mises dans le "coffre fort" pour étudier plus tard.
# id
# frommoves: exemple : '1. Nf3 c5 2. g3 g6 3. Bg2 Bg7 4. O-O Nc6 5. d3 d6 6. e4 Nf6'
# fen : 'r1bqk2r/pp2ppbp/2np1np1/2p5/4P3/3P1NP1/PPP2PBP/RNBQ1RK1 w kq -'
# title : 'A étudier après 1...c5 2.g3'
# visits: integer
# solved: integer

# pour KIA il n'y a qu'un  seul priyome. Peut-etre est-ce les positions sauvegardées pour analyse
# future

###### Table POSITIONS (valeurs rapportées depuis KIA)
# id : integer
# fromfen : chaine
# move : chaine
# note,glyph : TOUJOURS VIDE
# visits : integer
# score : integer TOUJOURS à 0
# learned : integer : 0 ou 1
# correct : integer TOUJOURS à 0
# rotator : 0 ou une date comme '2015-10-04 11:28:27'
# ordinal : nombre 0,1,2,3,4 ou 5 <- serait-ce l'annotation de type '!, +/-, ...'

