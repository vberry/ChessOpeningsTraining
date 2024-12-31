from neo4j import GraphDatabase
import re
import sys

from utils.env_file.read_env_file import get_env_variables_from_file

##############£       MAIN           ###########################

environ = get_env_variables_from_file('../../../variables.env')
AUTH = (environ['NEO4J_USER'],environ['NEO4J_PASSWORD'])
URI = environ['NEO4J_URI']

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")

    # Getting data from a DB:
    #records, summary, keys = driver.execute_query("MATCH (p:Position)-[m:MOVE]->() WHERE p.fen='rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -' RETURN m.move as move",database_="neo4j")
    records, summary, keys = driver.execute_query("MATCH (p:Position)-[m:MOVE]->() WHERE p.id=0 RETURN m.move as move",database_="neo4j")
    # Loop through results and do something with them
    for record in records:
        print(record.data())  # obtain record as dict
    # Summary information
    # print("The query `{query}` returned {records_count} records in {time} ms.".format(
    #     query=summary.query, records_count=len(records),
    #     time=summary.result_available_after
    # ))

    # Adding data in a DB:
    # # with parameters in the middle (name) whoe value is indicated afterwards:
    # summary = driver.execute_query("CREATE (:Person {name: $name})", \
    #                                  name="Alice", \
    #                                  database_="neo4j",).summary
    # print("Created {nodes_created} nodes in {time} ms.".format(
    # nodes_created=summary.counters.nodes_created,
    # time=summary.result_available_after))