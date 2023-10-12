# Backend Script Example

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from neo4j import GraphDatabase

# for security reasons
# you can store your database information in a separate file
uri = "neo4j+s://19b5ded5.databases.neo4j.io"
user = "neo4j"
password = "eS87GcULkCOLvQeqHzIiRtftod6AbfkzhPCcuOx_iUY"

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def mainpage():
    return ("ASD")

@app.get("/getGDBAddr")
async def funcTest():
    driver = GraphDatabase.driver(uri, auth=(user, password))
    gdb_address = driver.get_server_info().address
    driver.close()

    return gdb_address

@app.get("/graph")
async def funcTest(letter:str):
    result = []

    # connect to GDB
    driver = GraphDatabase.driver(uri, auth=(user, password))
    session = driver.session(database="neo4j")

    # run query
    movies = session.execute_read(
        match_movie_nodes,
        letter
    )

    # struture your results
    for movie in movies:
        title = movie[0]
        year = movie[1]
        result.append({"title":title, "year": year})

    # unless you created them using the with statement
    # call the .close() method on all Driver and Session instances to release any resources still held by them.
    session.close()
    driver.close()

    return result

@app.get("/allppl")
async def allpeople():
    driver = GraphDatabase.driver(uri, auth=(user, password))
    session = driver.session(database="neo4j")

    # Modify your Cypher query to return all people nodes and their properties
    query = "MATCH (p:people) RETURN p"

    result = session.run(query)
    people_list = []

    for record in result:
        person_node = record['p']
        person_properties = person_node.get("Name", "")  # Access the "Name" property
        birth_year = person_node.get("Birth Year", None)  # Access the "Birth Year" property
        people_list.append({"Name": person_properties, "Birth Year": birth_year})

    session.close()
    driver.close()

    return people_list

@app.get("/allwallet")
async def allwallet():
    driver = GraphDatabase.driver(uri, auth=(user, password))
    session = driver.session(database="neo4j")

    # Modify your Cypher query to return all people nodes and their properties
    query = "MATCH (w:wallet) RETURN w"

    result = session.run(query)
    wallet_list = []

    for record in result:
        wallet_node = record['w']
        wallet_addressId = wallet_node.get("addressId", "")  # Access the "Name" property
        wallet_type = wallet_node.get("type", "")  # Access the "Name" property
        wallet_list.append({"ID": wallet_addressId})
        wallet_list.append({"Type": wallet_type})

    session.close()
    driver.close()

    return wallet_list

@app.get("/walletidx")
async def allwallet():
    driver = GraphDatabase.driver(uri, auth=(user, password))
    session = driver.session(database="neo4j")

    # Modify your Cypher query to return all people nodes and their properties
    query = "MATCH (w:wallet) RETURN w"

    result = session.run(query)
    wallet_list = []


    for record in result:
        wallet_node = record['w']
        wallet_addressId = wallet_node.get("type", "")  # Access the "Name" property
        wallet_list.append({"ID": wallet_addressId})

    session.close()
    driver.close()
    return wallet_list[0]["ID"]

# wrap your cypher code here
def match_movie_nodes(tx, name_filter):
    result = tx.run("""
                    MATCH (m:movie) WHERE m.Name STARTS WITH $filter
                    RETURN m.Name AS name, m.`Release Year` AS releaseYear
                    """, filter=name_filter)

    # return a list of Record objects
    return list(result)
