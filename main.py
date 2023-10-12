from fastapi import FastAPI
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase, RoutingControl
import json

load_dotenv()

app = FastAPI()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")

def run_neo4j_query(address_id):
    query = (
        """
        MATCH (wallet:wallet {addressId: '0x8d08aad4b2bac2bb761ac4781cf62468c9ec47b4'})
        OPTIONAL MATCH (wallet)-[s:RECEIVED_FROM]->(wallet_in)
        OPTIONAL MATCH (wallet)-[r:SENT_TO]->(wallet_out)
        WITH wallet, wallet_in, wallet_out, s, r
        ORDER BY s.block_timestamp DESC
        WITH wallet, wallet_in, wallet_out, COLLECT(DISTINCT s)[0] AS latest_sender, COLLECT(DISTINCT r)[0] AS latest_recipient
        WITH wallet,
        COLLECT(DISTINCT wallet_in) AS wallet_in_list,
        COLLECT(DISTINCT wallet_out) AS wallet_out_list,
        COLLECT(DISTINCT latest_sender) AS latest_in,
        COLLECT(DISTINCT latest_recipient) AS latest_out
        RETURN wallet,
        wallet_in_list AS wallet_in,
        wallet_out_list AS wallet_out,
        latest_in AS latest_in,
        latest_out AS latest_out;
        """
    )

    result_json = {
        "main": {
            "id": None,
            "addressId": None,
            "name": None,
            "type": None,
            "dateCreated": None,
            "transactionsIn": [],
            "transactionsOut": []
        },
        "connected": []
    }

    # Create a Neo4j session and run the query
    with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
        with driver.session() as session:
            
            result = list(session.run(query, addressId=address_id))  # Convert result to a list

   
            if result:
                record = result[0]
                
                for record in result:

                    if record["wallet"] is not None:
                        main = result_json["main"]
                        main["id"] = record["wallet"]._element_id.split(":")[0]
                        main["addressId"] = record["wallet"]["addressId"]
                        main["name"] = record["wallet"]["name"]
                        main["type"] = record["wallet"]["type"]
                        main["dateCreated"] = record["wallet"]["dateCreated"]

                        

                        if record["latest_in"] is not None:
                            for latest_in in record["latest_in"]:
                                transaction_in = {
                                    "hash": latest_in["hash"],
                                    "value": latest_in["value"],
                                    "input": latest_in["input"],
                                    "transaction": latest_in["transaction"],
                                    "gas": latest_in["gas"],
                                    "gas_used": latest_in["gas_used"],
                                    "gas_price": latest_in["gas_price"],
                                    "transaction_fee": latest_in["transaction_fee"],
                                    "block_number": latest_in["block_number"],
                                    "block_timestamp": latest_in["block_timestamp"],
                                }
                                main["transactionsIn"].append(transaction_in)

                        if record["latest_out"] is not None:
                            for latest_out in record["latest_out"]:
                                transaction_out = {      
                                    # "id": latest_out["wallet"]._element_id.split(":")[0],                          
                                    "hash": latest_out["hash"],
                                    "value": latest_out["value"],
                                    "input": latest_out["input"],
                                    "transaction": latest_out["transaction"],
                                    "gas": latest_out["gas"],
                                    "gas_used": latest_out["gas_used"],
                                    "gas_price": latest_out["gas_price"],
                                    "transaction_fee": latest_out["transaction_fee"],
                                    "block_number": latest_out["block_number"],
                                    "block_timestamp": latest_out["block_timestamp"],
                                }
                                main["transactionsOut"].append(transaction_out)

                        if record["wallet_in"] is not None:
                            for wallet_in in record["wallet_in"]:
                                connected = {
                                    # "id": wallet_in._element_id.split(":")[0],
                                    "addressId": wallet_in["addressId"],
                                    "name": wallet_in["name"],
                                }
                                result_json["connected"].append(connected)
                            
                        if record["wallet_out"] is not None:
                            print(record["wallet_out"])
                            
                            for wallet_out in record["wallet_out"]:
                                print(wallet_out)
                                connected = {
                                    # "id": wallet_out._element_id.split(":")[0],
                                    "addressId": wallet_out["addressId"],
                                    "name": wallet_out["name"],
                                }
                                result_json["connected"].append(connected)

            print(result_json)
            json_string = json.dumps(result_json, indent=2)
            print(json_string)
            
            # print(record["wallet_in"])
            # print(record["wallet_out"])
            # print(record["latest_in"])
            # print(record["latest_out"])
           

            

            # print(result_json)

        session.close()
        driver.close()
        return result
    
def create_graph():
    query = (
        """
        CREATE CONSTRAINT `uniq_wallet_addressId` IF NOT EXISTS
        FOR (n: wallet)
        REQUIRE (n.addressId ) IS UNIQUE;

        :param {
        idsToSkip: []
        };

        LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/KellyUni/COS30049_DA/main/Assignment2/nodes.csv' AS row
        WITH row
        WHERE NOT row.addressId IN $idsToSkip AND NOT row.addressId IS NULL
        CALL {
        WITH row
        MERGE (n: `wallet` { `addressId`: row.`addressId` })
        SET n.`type` = toString(trim(row.`type`))
        SET n.`name` = toString(trim(row.`name`))
        SET n.`dateCreated` = toString(trim(row.`dateCreated`))
        } IN TRANSACTIONS OF 10000 ROWS;

        // Create relationships a -`SENT_TO`-> b
        LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/KellyUni/COS30049_DA/main/Assignment2/relationships.csv' AS row
        WITH row 
        CALL {
        WITH row
        MATCH (source: wallet { addressId: row.from_address } )
        MATCH (target: wallet { addressId: row.to_address } )
        CREATE (source) - [r:`SENT_TO`] -> (target)
        SET r.`hash` = toString(trim(row.`hash`))
        SET r.`value` = toString(trim(row.`value`))
        SET r.`gas` = toInteger(trim(row.`gas`))
        SET r.`gas_used` = toInteger(trim(row.`gas_used`))
        SET r.`gas_price` = toInteger(trim(row.`gas_price`))
        SET r.`transaction_fee` = toInteger(trim(row.`transaction_fee`))
        SET r.`block_number` = toInteger(trim(row.`block_number`))
        SET r.`block_timestamp` = toInteger(trim(row.`block_timestamp`))
        } IN TRANSACTIONS OF 10000 ROWS;

        // Create relationships a -`RECEIVED_FROM`-> b
        LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/KellyUni/COS30049_DA/main/Assignment2/relationships.csv' AS row
        WITH row 
        CALL {
        WITH row
        MATCH (source: wallet { addressId: row.to_address } )
        MATCH (target: wallet { addressId: row.from_address } )
        CREATE (source) - [received:`RECEIVED_FROM`] -> (target)
        SET received.`hash` = toString(trim(row.`hash`))
        SET received.`value` = toString(trim(row.`value`))
        SET received.`gas` = toInteger(trim(row.`gas`))
        SET received.`gas_used` = toInteger(trim(row.`gas_used`))
        SET received.`gas_price` = toInteger(trim(row.`gas_price`))
        SET received.`transaction_fee` = toInteger(trim(row.`transaction_fee`))
        SET received.`block_number` = toInteger(trim(row.`block_number`))
        SET received.`block_timestamp` = toInteger(trim(row.`block_timestamp`))
        } IN TRANSACTIONS OF 10000 ROWS;
        """
    )

    # Create a Neo4j session and run the query
    with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
        with driver.session() as session:
            session.run(query)






app = FastAPI()

# Allow all origins during development, change this for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)






# for section 3


@app.get("/")
async def funcTest1():
    return "Hello, this is fastAPI data"


@app.get("/getAboutData")
async def funcTest2():
    return "Hello, this is about us data"


@app.get("/getHomeData")
async def funcTest3():
    return "Hello, this is home data"


@app.get("/jsonData")
async def funcTest():
    jsonResult = {
        "name": "Your name",
        "Uni-year": 2,
        "isStudent": True,
        "hobbies": ["reading", "swimming"]
    }
    return jsonResult


@app.get("/student/{student_id}")
async def getStudentId(student_id: int):
    return {"student_id": student_id}


@app.get("/wallet")
async def allwallet():
    result = run_neo4j_query("0x58f56615180a8eea4c462235d9e215f72484b4a3")
    for record in result:
        print(record)
   

    return result

run_neo4j_query("0x8d08aad4b2bac2bb761ac4781cf62468c9ec47b4")
