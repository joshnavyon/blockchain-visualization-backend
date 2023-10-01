from neo4j import GraphDatabase
from constants import *

class GraphDB:

    def __init__(self):

        uri = NEO4J_URI
        user = NEO4J_USERNAME
        password = NEO4J_PASSWORD

        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print("Neo4j GDB address:", self.driver.get_server_info().address)

    def close(self):
        self.driver.close()


if __name__ == "__main__":
    GDB = GraphDB()
    GDB.close()
