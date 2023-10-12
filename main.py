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
        "MATCH (wallet:wallet {addressId: $addressId})\n"
        "OPTIONAL MATCH (wallet)-[s:RECEIVED_FROM]->(wallet_in)\n"
        "OPTIONAL MATCH (wallet)-[r:SENT_TO]->(wallet_out)\n"
        "WITH wallet, wallet_in, wallet_out, s, r\n"
        "ORDER BY s.block_timestamp DESC\n"
        "WITH wallet, wallet_in, wallet_out, COLLECT(DISTINCT s)[0] AS latest_in, COLLECT(DISTINCT r)[0] AS latest_out\n"
        "RETURN wallet, wallet_in, wallet_out, latest_in, latest_out;"
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
                
                if record["wallet"] is not None:
                    main = result_json["main"]
                    
                    main["addressId"] = record["wallet"]["addressId"]
                    main["type"] = record["wallet"]["type"]
                    

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
                        for latest_out in result:
                            transaction_out = {
                                
                                "hash": latest_out["latest_out"]["hash"],
                                "value": latest_out["latest_out"]["value"],
                                "input": latest_out["latest_out"]["input"],
                                "transaction": latest_out["latest_out"]["transaction"],
                                "gas": latest_out["latest_out"]["gas"],
                                "gas_used": latest_out["latest_out"]["gas_used"],
                                "gas_price": latest_out["latest_out"]["gas_price"],
                                "transaction_fee": latest_out["latest_out"]["transaction_fee"],
                                "block_number": latest_out["latest_out"]["block_number"],
                                "block_timestamp": latest_out["latest_out"]["block_timestamp"],
                            }
                            main["transactionsOut"].append(transaction_out)

                    if record["wallet_in"] is not None:
                        for wallet_in in result:
                            connected = {
                                "addressId": wallet_in["wallet"]["addressId"],
                                "name": wallet_in["wallet"]["name"],
                            }
                            result_json["connected"].append(connected)
                        
                    if record["wallet_out"] is not None:
                        for wallet_out in result:
                            connected = {
                                "addressId": wallet_out["wallet"]["addressId"],
                                "name": wallet_out["wallet"]["name"],
                            }
                            result_json["connected"].append(connected)

            # print(result_json)
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

run_neo4j_query("0x58f56615180a8eea4c462235d9e215f72484b4a3")
