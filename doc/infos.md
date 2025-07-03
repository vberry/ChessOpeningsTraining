Contains progs to handle opening books from *Chess Opening Trainer* (COT) <- correct name?
This is an old app that existed on iPad in the early 2010s (on iOS). 

The content of a COT opening book is stored in a graph database with neo4j.
This database server is run in a docker container :

1) first time you need to get the image: 
docker pull neo4j

2) Then to run the container : 
docker run \
    --restart always \
    --publish=7474:7474 --publish=7687:7687 \
    neo4j

Note: if the neo4j plugin of docker Desktop is installed, it occupies port 7474, so the container won't launch this way.
The content of the db can be seen this way: http://localhost:7474

# NOTES
- on peut créer des contraintes d'unicité : il faut faire ça sur les noeuds représentant des positions: 
*Create unique node property constraints to ensure that property values are unique for all nodes with a specific label. Adding the unique constraint, implicitly adds an index on that property.* Example:
`CREATE CONSTRAINT FOR (n:Movie) REQUIRE (n.title) IS UNIQUE`

- Create indexes on one or more properties for all nodes that have a given label. Indexes are used to increase search performance. Example: `CREATE INDEX FOR (m:Movie) ON (m.released)`

- 
