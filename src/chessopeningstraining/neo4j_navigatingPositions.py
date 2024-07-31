# Explores positions stored in neo4j and navigates onward from the initial position 
# by choosing moves among those proposed in the DB.


from neo4j import GraphDatabase
from chess import Board

from utils.env_file.read_env_file import get_env_variables_from_file

def moving_forward(position_id):
    # Get position with this id
    records, _ , _ = driver.execute_query("MATCH (p:Position) WHERE p.id=$id RETURN p.fen as fen",\
                                                  id = position_id, database_="neo4j")
    # Display the board of this postion
    board = Board(records[0]['fen'])
    print(board)
    # Gets available moves from here
    records, _ , _ = driver.execute_query("MATCH (p:Position)-[m:Move]->(p2:Position) WHERE p.id=$id \
                                               RETURN m.move as move, p2.id as next_id",\
                                               id = position_id, database_="neo4j")
    if len(records)==0: 
        print('No move available from this position')
        return # no more moves from the position
    # printing available moves
    moves = []
    for record in records:
        moves.append(record.data()) 
    for idx, m in enumerate(moves):
        print(idx, m)
    choice = int(input('prochain coup ? '))
    next_position_id = moves[choice]['next_id']
    print('prochaine position = ',next_position_id)
    moving_forward(next_position_id)

##############£       MAIN           ###########################

environ = get_env_variables_from_file('../../variables.env')
AUTH = (environ['NEO4J_USER'],environ['NEO4J_PASSWORD'])
URI = environ['NEO4J_URI']

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")
    moving_forward(0) # starts at initial position (having special label 0)