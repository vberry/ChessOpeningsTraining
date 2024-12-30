
# This program is here to check that the table "notes" refers to positions rather 
#    than to moves *from* position
# If true, this means each *fromfen* must be unique among tuples in the notes table
#  Result: indeed, this is true on the 6 opening book files I got.
# This means 'fromfen' should be read as '**FOR*** fen' in the notes table

# To run this program from the root folder of the project:
#     python3 src/chessopeningstraining/checkingNotes.py $PWD/openings
# or  uv run  src/chessopeningstraining/checkingNotes.py $PWD/openings
#----------------------------------------------------------
# DOCTEST are automatically checked when running the script
#----------------------------------------------------------

import sqlite3
import sys

from os import listdir
from os.path import isfile, join

def check_opening_file(filename):
    """ 
    This is a doc comment
    >>> check_opening_file("openings/Semi-slave.sqlite")
    Checking openings/Semi-slave.sqlite
    nb of tuples in the -notes- table = 238
    all done, no duplicate
    """
    # /Users/vberry/Prog/ChessOpeningsTraining/src/chessopeningstraining/
    print('Checking',filename)
    con = sqlite3.connect(filename)
    cur = con.cursor()
    ###  Rows of a TABLE : 
    cur.execute("SELECT * FROM notes")
    # -> 'note' and 'glyph' fields are never used (always empty)
    #print(cur.fetchone()) # gives just one result row
    tuples_notes = cur.fetchall()
    print('nb of tuples in the -notes- table =',len(tuples_notes)) # gives the following
    # Checks that ...
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
if __name__ == "__main__":
    # Checks that we got one folder name as argument to run the script:
    if len(sys.argv)<2:
        print("\t\tUsage: "+sys.argv[0]+' <folder_containing_sqlite files>')
        sys.exit(-1)
    mypath = sys.argv[1]

    print("First running the doctests.")
    import doctest
    test_res=doctest.testmod()
    if test_res.failed:
        print('some tests failed: refusing to run the script') 
        sys.exit()
    print('All tests are OK, proceeding with running the script')
    for i in range(60):
        print('-',end='')
    print()
    # MAIN script:
    for f in listdir(mypath):
      name=join(mypath, f)
      #print(f'Got this file: {name}')
      if isfile(name) and name.endswith('sqlite'):
         check_opening_file(name)
    