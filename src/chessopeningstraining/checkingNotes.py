
# This is to check that table notes refer to positions rather than to moves *from* position
# If true, this means each *fromfen* must be unique among tuples in the table
#
#  Result: indeed, this is true on the 6 opening files I got
#
# This means 'fromfen' should be read as 'FOR fen'
#
import sqlite3
import sys

from os import listdir
from os.path import isfile, join

def check_opening_file(filename):
    print('Checking ',filename)
    con = sqlite3.connect(filename)
    cur = con.cursor()
    ###  TUPLES d'une TABLE : 
    cur.execute("SELECT * FROM notes")
    # -> les champs 'note' et 'glyph' ne sont jamais utilisés, il sont toujours vide
    #print(cur.fetchone()) # en donne juste un
    tuples_notes = cur.fetchall()
    print('nb de tuples dans table -notes- = ',len(tuples_notes)) # donne les suivants

    all_fens = {}
    for row in tuples_notes:
        fen = row[1]
        if fen in all_fens:
            print('PBM id='+row[0]+' is already listed y note id='+all_fens[fen])
            break
        else:
            all_fens[fen] = row[0]
    print('all done, no duplicate')

# # ##########    MAIN   #################
if len(sys.argv)<2:
    print("\t\tUsage: "+sys.argv[0]+' <folder_containing_sqlite files>')
    sys.exit(-1)
mypath = sys.argv[1]

for f in listdir(mypath):
    name=join(mypath, f)
    if isfile(name):
        check_opening_file(name)
#print('Premier tuple de cette table :\n',tuples_position[0])
