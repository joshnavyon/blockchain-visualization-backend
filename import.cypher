CREATE CONSTRAINT `imp_uniq_people_Name` IF NOT EXISTS
FOR (n: `people`)
REQUIRE (n.`Name`) IS UNIQUE;
CREATE CONSTRAINT `imp_uniq_movie_Name` IF NOT EXISTS
FOR (n: `movie`)
REQUIRE (n.`Name`) IS UNIQUE;

:param {
  idsToSkip: []
};

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/KellyUni/COS30049_DA/main/WorkshopW6/nodes_people.csv' AS row
WITH row
WHERE NOT row.`Name` IN $idsToSkip AND NOT row.`Name` IS NULL
CALL {
  WITH row
  MERGE (n: `people` { `Name`: row.`Name` })
  SET n.`Birth Year` = toInteger(trim(row.`Birth Year`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/KellyUni/COS30049_DA/main/WorkshopW6/nodes_movies.csv' AS row 
WITH row
WHERE NOT row.`Name` IN $idsToSkip AND NOT row.`Name` IS NULL
CALL {
  WITH row
  MERGE (n: `movie` { `Name`: row.`Name` })
  SET n.`Release Year` = toInteger(trim(row.`Release Year`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/KellyUni/COS30049_DA/main/WorkshopW6/rels.csv' AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `people` { `Name`: row.`People` })
  MATCH (target: `movie` { `Name`: row.`Movie` })
  CREATE (source)-[r: `stars in`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;