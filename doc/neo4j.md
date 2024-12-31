# Launching the neo4j server (with web interface)
docker run  --restart always -p7474:7474 -p7687:7687 neo4j
-> 
Bolt enabled on 0.0.0.0:7687.
HTTP enabled on 0.0.0.0:7474.

Then in a browser, open http://localhost:7474 and you get to the web GUI interface of neo4J

# Cypher cheat sheet:
https://neo4j.com/docs/cypher-cheat-sheet/5/auradb-enterprise/

# INTERRUPTING LONG transaction: 
SHOW TRANSACTIONS
TERMINATE TRANSACTION "neo4j-transaction-1461"

# DELETING :
## Deleting a node: 
MATCH (n:Person {name: 'Tom Hanks'}) DELETE n
## Deleting all Position nodes: 
MATCH (n:Position) DELETE n
## Deleting all nodes and relationships in db: 
MATCH (n) DETACH DELETE n
# Deleting constraints is more painfull by hand:
SHOW CONSTRAINTS yield name RETURN "DROP CONSTRAINT " + name + ";";

# CONSTRAINTS : 
Graph academy: 
- "Constraints are internally encoded as indexes"
- "Best practice: define a uniqueness constraint for evey node"
- "Best practice is to create constraints before adding data to the graph": pbm this makes the addition very slow!
- Existence constraints apply on nodes and rel°
- =Node key: "existence and uniqueness" constraint for a node: we need that for Pos° 
- for Move ids we need also existence and uniqueness.

SHOW CONSTRAINT
CREATE CONSTRAINT FOR (p:Position) REQUIRE p.id IS UNIQUE  ;
DROP CONSTRAINT constraint_3432423

WARNING: StackOverflow oct 2016: "There are no indexes on relationships, so any CREATE UNIQUE or MERGE operation like what you have above must scan all relationships of that type and compare property values to see if that relationship already exists"

# INDEXES
Graph academy: 
- "they allow the graphe engine to retrieve data quickly
- Create indexes after data has been put into the graph
- Indexes makes creating data slower but retreiving it faster
-> for positions' fens (and comments?) we can create an index of type TEXT that will allow to find not only exact fens (as type RANGE) but also to query for subparts of the fen (TEXT: optimized for queries filtering with the STRING operators CONTAINS and ENDS WITH) 


# GETTING INFO
## Get type of a node : 
MATCH (n) RETURN labels(n)
## Get info of a node: 
MATCH (n:Position) where n.id=260 RETURN n (ou RETURN n.fromfen)
## Getting back a particular move:
MATCH (:Position)-[m:MOVE]->(:Position) WHERE m.id=10 RETURN m
## Getting all moves from a position indicated by a fen:
MATCH (p:Position)-[m:MOVE]->() WHERE p.fen='rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -' RETURN m.move

## Getting connected nodes:
MATCH (n) MATCH (n)-[r]-() RETURN n,r : will return all nodes that have a relationship to another node or nodes, irrespective of the direction of the relationship.
MATCH (p:Position{id:966})-[*0..]->(autre) RETURN autre.id  : all nodes that can be accessed from pos° 966


All nodes not reachable from the starting position:
MATCH (Position{id:0})-[:MOVE*]->(conn:Position)
WITH collect(distinct conn) as connected
MATCH (p:Position) WHERE NOT p IN connected
RETURN p.id

Deleting all these nodes and their relationships:
MATCH (Position{id:0})-[:MOVE*]->(conn:Position)
WITH collect(distinct conn) as connected
MATCH (p:Position) WHERE NOT p IN connected
DETACH DELETE p

# Knowing if a node contains a property:
MATCH (p:Position) WHERE p.id = 1 RETURN p.commentaire IS  NULL
-> True signifie que pas de champ commentaire

# Adding a property to a node (+=): 
MATCH (p {name: 'Peter'})
SET p += {age: 38, hungry: true, position: 'Entrepreneur'}
RETURN p.name, p.age, p.hungry, p.position