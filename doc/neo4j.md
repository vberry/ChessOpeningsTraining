# Launching the neo4j server (with web interface)
docker run  --restart always -p7474:7474 -p7687:7687 neo4j
-> 
Bolt enabled on 0.0.0.0:7687.
HTTP enabled on 0.0.0.0:7474.

Puis dans le navigateur on va dans http://localhost:7474 et on se trouve sur l'interface web



# GETTING INFO
## Get type of a node : 
MATCH (n) RETURN labels(n)
## Get info of a node: 
MATCH (n:Position) where n.id=260 RETURN n (ou RETURN n.fromfen)
## Getting back a particular move:
MATCH (:Position)-[m:MOVE]->(:Position) WHERE m.id=10 RETURN m
## Getting all moves from a position indicated by a fen:
MATCH (p:Position)-[m:MOVE]->() WHERE p.fen='rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -' RETURN m.move

# DELETING :
## Deleting a node: 
MATCH (n:Person {name: 'Tom Hanks'}) DELETE n
## Deleting all Position nodes: 
MATCH (n:Position) DELETE n
## Deleting all nodes and relationships in db: 
MATCH (n) DETACH DELETE n

# Savoir si un noeud contient une propriété : 
MATCH (p:Position) WHERE p.id = 1 RETURN p.commentaire IS  NULL
-> True signifie que pas de champ commentaire

# AJOUTER UNE PROPRIETE a un NOEUD (+=) : 
MATCH (p {name: 'Peter'})
SET p += {age: 38, hungry: true, position: 'Entrepreneur'}
RETURN p.name, p.age, p.hungry, p.position