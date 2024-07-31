from neo4j import GraphDatabase
import re
import sys

# Reducing to the bare minimal removes the need for a dotenv dependency
def get_env_variables_from_file(filename):
    '''Reads variable values in an environment file'''
    dict = {}
    with open(filename) as f:
        for line in f:
            res = re.search(r'^(\w+)=(.+)$',line.strip())
            if line.strip().startswith('#') or line.strip() == '':
                continue
            if not res:
                print("PBM can't parse that line in the environment variable file:",line)
                sys.exit(-3)
            dict[res.group(1)] = res.group(2)
    return dict

##############£       MAIN           ###########################
environ = get_env_variables_from_file('../../variables.env')
USER = environ['NEO4J_USER']
PASSWORD = environ['NEO4J_PASSWORD']
AUTH = (USER,PASSWORD)
URI = "neo4j://localhost"

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")
    sys.exit(0)
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