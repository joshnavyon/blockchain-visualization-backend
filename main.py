import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from neo4j_function import run_neo4j_query, run_neo4j_query2

load_dotenv()

NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")


app = FastAPI()

# Allow all origins during development, change this for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def funcTest1():
    return "Hello, this is fastAPI data"

@app.get("/wallet/{address_id}")
async def getWallet(address_id: str):
    result = run_neo4j_query(address_id, NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

    return result


@app.get("/wallet2/{address_id}")
async def getWallet(address_id: str):
    result = run_neo4j_query2(address_id, NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

    return result