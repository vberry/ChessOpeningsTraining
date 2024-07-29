# Transforms positions and notes from an sqlite db of the CPT app
# into the creation of a graph for the neo4j graph database system

import sqlite3
import sys
import chess
import re

from os import listdir
from os.path import isfile, join

def get_COT_formatted_fen(board):
    ''' remove the last part of the fen generated by the chess module as this part is not stored with positions in the COT database'''
    m = re.search('(.*)\s+\d+\s+\d+',board.fen())
    if m:
        return m.group(1)
    else:
        print('function get_COT_formatted_fen: regexp not correct to remove last part of large fen')
        sys.exit(-1)

def fen_after_move(fen,move):
    board = chess.Board(fen)
    board.push_san(move)
    return get_COT_formatted_fen(board)

#######    MAIN        #########

mypath = 'openings' ; index = 0 ; files = []
for f in listdir(mypath):
    if isfile(join(mypath, f)) and f.endswith('.sqlite'):
        print(index,' : ',f)
        files.append(f) ; index += 1
choice = int(input('Which file to transform? '))
filename=join(mypath, files[choice])
con = sqlite3.connect(filename)
cur = con.cursor()
###  GET all positions : 
cur.execute("SELECT id,fromfen,move,ordinal FROM positions")
positionsLITE = cur.fetchall()
print('nb of positions in this opening book = ',len(positionsLITE)) 

# Load positions in a dictionary
SQlite_positions = {} ; SQlite_from_fens = {}
for (id,fromfen,move,ordinal) in positionsLITE:
    if id in SQlite_positions:
        print('ERROR: id ',id,' is not unique in the sqlite db!')
        sys.exit(-1)
    SQlite_positions[id] = {'fromfen':fromfen,'move':move,'ordinal':ordinal}
    if fromfen in SQlite_from_fens:
        SQlite_from_fens[fromfen].append((move,ordinal)) # adds the move of the SQlite position and ordinal of this move
    else:
        SQlite_from_fens[fromfen] = [(move,ordinal)]


# Generate data structures for the positions and moves to be stored in the graph db
nodes = {} # fen to id in the graphDB
moves = {} # move_id relating a 'from' and a 'to' positions (the move_id is taken from the SQLite position)

# Adds the initial position in the graphDB with id 0
if 0 in SQlite_positions:
    print("Houston we have a pbm: id 0 is already taken by a 'position' of the SQlite db")
    sys.exit(-2)

init_fen = get_COT_formatted_fen(chess.Board())
nodes[init_fen] = 0 ; node_id = 1 

# In fact each 'position in the SQlite DB is in fact a move" -> we prepare it as this in the graphDB
for id in SQlite_positions:
    # if id already seen we have duplicate ids:
    if id in moves:
        print("Duplicate position ids in SQlite db")
        sys.exit(-1)
    # is the starting position already known? Otherwise we create it for the graphDB
    starting_fen = SQlite_positions[id]['fromfen']
    if starting_fen not in nodes:
        nodes[starting_fen] = node_id ; node_id += 1
    # for this position we reach a new position:
    resulting_fen = fen_after_move(starting_fen,SQlite_positions[id]['move'])
    #print('resulting board :', chess.Board(resulting_fen))
    # we add this node if this position is not already registered
    if resulting_fen not in nodes:
        nodes[resulting_fen] = node_id ; node_id += 1
    # Now we add the move between the two
    moves[id] = {'label': SQlite_positions[id]['move'], 'from': starting_fen, 'to':resulting_fen, 'ordinal':SQlite_positions[id]['ordinal']} 

    # to which we give our id (if position is not already existing)
    #CREATION.append( "CREATE (n"+str(id)+":Position {id: "+str(id)+", fromfen:'"+newFen+"'})" ) 
    # CREATION.append( "CREATE (n"+str(id)+":Position {id: "+str(id)+", fromfen:'"+positions[id]['fromfen']+"'})" )
    #stop -= 1
    #if stop == 0: break

print('Nb de noeuds pour graph DB = ',len(nodes.keys()))
print('Nb de moves pour graph DB = ',len(moves.keys()))



stop = 5
# Create graph nodes 
CREATION = []
for (fen,id) in nodes.items():
    CREATION.append( "CREATE (n"+str(id)+":Position {id: "+str(id)+", fen:'"+fen+"'})" ) 
    # stop -= 1
    # if stop == 0: 
    #     break

# Create move relationships
stop = 5
for m_id in moves:
    move = moves[m_id]['label']
    from_fen = moves[m_id]['from']
    to_fen = moves[m_id]['to']
    ordinal = moves[m_id]['ordinal']
    s_id = nodes[from_fen]
    t_id = nodes[to_fen]
    CREATION.append( "CREATE (n"+str(s_id)+")-[:MOVE {id: "+str(m_id)+", move:'"+move+"', ordinal:"+str(ordinal)+"}]->(n"+str(t_id)+")" )
            
    # stop -= 1
    # if stop == 0: 
    #     break

# open file in write mode

filename = filename.removesuffix('.sqlite')+'.cypher'
with open(filename, 'w') as f:
    for line in CREATION:
        # write each item on a new line
        f.write("%s\n" % line)
    print('Done')

print('neo4j file created: ',filename)

#print("\n".join(CREATION))

