from neo4j import GraphDatabase
from fastapi import HTTPException

def run_neo4j_query(address_id, uri, username, password):
    query = (
        """
        MATCH (wallet:wallet {addressId: $addressId})
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

    result_json = [{
            "id": None,
            "addressId": None,
            "name": None,
            "type": None,
            "dateCreated": None,
            "transactionsIn": [],
            "transactionsOut": []
    }]


    
    # Create a Neo4j session and run the query
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
    

            with driver.session() as session:
                
                result = list(session.run(query, addressId=address_id))  # Convert result to a list
                print(result)
    
                if result:
                    record = result[0]
                    
                    for record in result:


                        if record["wallet"] is not None:
                            
                            result_json[0]["id"] = record["wallet"]["id"]
                            result_json[0]["addressId"] = record["wallet"]["addressId"]
                            result_json[0]["name"] = record["wallet"]["name"]
                            result_json[0]["type"] = record["wallet"]["type"]
                            result_json[0]["dateCreated"] = record["wallet"]["dateCreated"]

                            
                            if record["wallet_in"] and record["latest_in"] is not None:
                                id = []
                                for wallet_in in record["wallet_in"]:
                                    connected = {
                                    "id": wallet_in["id"],
                                        "addressId": wallet_in["addressId"],
                                        "name": wallet_in["name"],
                                    }
                                    id.append(wallet_in["id"])
                                    result_json.append(connected)
                        
                                for latest_in in record["latest_in"]:
                                    transaction_in = {
                                        "id": id.pop(0),
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
                                    result_json[0]["transactionsIn"].append(transaction_in)

                            if record["wallet_out"] and record["latest_out"] is not None:
                                id = []
                                
                                for wallet_out in record["wallet_out"]:
                                    
                                    connected = {
                                        "id": wallet_out["id"],
                                        "addressId": wallet_out["addressId"],
                                        "name": wallet_out["name"],
                                    }
                                    id.append(wallet_out["id"])
                              
                                    result_json.append(connected)


                                for latest_out in record["latest_out"]:
                                 
                                    transaction_out = {      
                                        "id": id.pop(0),                
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
                                    result_json[0]["transactionsOut"].append(transaction_out)

                    
                    result = result_json
                else:
                    raise HTTPException(status_code=500, detail="Query failed")
                # result = json.dumps(result_json, indent=2)

                
        
            return result
  


def run_neo4j_query2(address_id, uri, username, password):
    query = (
        """
        MATCH (wallet:wallet {addressId: $addressId})
        OPTIONAL MATCH (wallet)-[s:RECEIVED_FROM]->(wallet_in)
        OPTIONAL MATCH (wallet)-[r:SENT_TO]->(wallet_out)
        WITH wallet, wallet_in, wallet_out, s, r
        ORDER BY s.block_timestamp DESC
        WITH wallet, wallet_in, wallet_out, s as latest_sender, r AS latest_recipient
        WITH wallet,
        COLLECT(DISTINCT(wallet_in)) AS wallet_in_list,
        COLLECT(DISTINCT(wallet_out)) AS wallet_out_list,
        COLLECT(DISTINCT(latest_sender)) AS latest_in,
        COLLECT(DISTINCT(latest_recipient)) AS latest_out
        RETURN wallet,
        wallet_in_list AS wallet_in,
        wallet_out_list AS wallet_out,
        latest_in AS latest_in,
        latest_out AS latest_out;
        """
    )

    result_json = [{
            "id": None,
            "addressId": None,
            "name": None,
            "type": None,
            "dateCreated": None,
            "transactionsIn": [],
            "transactionsOut": []
    }]



    # Create a Neo4j session and run the query
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:


            with driver.session() as session:
                
                result = list(session.run(query, addressId=address_id))  # Convert result to a list
                print(result)

                if result:
                    record = result[0]
                    
                    for record in result:


                        if record["wallet"] is not None:
                            
                            result_json[0]["id"] = record["wallet"]["id"]
                            result_json[0]["addressId"] = record["wallet"]["addressId"]
                            result_json[0]["name"] = record["wallet"]["name"]
                            result_json[0]["type"] = record["wallet"]["type"]
                            result_json[0]["dateCreated"] = record["wallet"]["dateCreated"]

                            
                            if record["wallet_in"] and record["latest_in"] is not None:
                                id = []
                                for wallet_in in record["wallet_in"]:
                                    connected = {
                                    "id": wallet_in["id"],
                                        "addressId": wallet_in["addressId"],
                                        "name": wallet_in["name"],
                                    }
                                    id.append(wallet_in["id"])
                                    result_json.append(connected)
                        
                                for latest_in in record["latest_in"]:
                                    transaction_in = {
                                        "id": latest_in.end_node['id'],
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
                                    result_json[0]["transactionsIn"].append(transaction_in)

                            if record["wallet_out"] and record["latest_out"] is not None:
                                id = []
                                
                                for wallet_out in record["wallet_out"]:
                                    
                                    connected = {
                                        "id": wallet_out["id"],
                                        "addressId": wallet_out["addressId"],
                                        "name": wallet_out["name"],
                                    }
                                    id.append(wallet_out["id"])
                                    # print("ID is: ", id)
                                    # print('---')
                                    result_json.append(connected)


                                for latest_out in record["latest_out"]:

                                    transaction_out = {      
                                        "id": latest_out.end_node['id'],                
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
                                    result_json[0]["transactionsOut"].append(transaction_out)

                    
                    result = result_json
                else:
                    raise HTTPException(status_code=500, detail="Query failed")
                # result = json.dumps(result_json, indent=2)

                
        
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
