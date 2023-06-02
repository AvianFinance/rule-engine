
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

env_vars = dotenv_values()

uri = "mongodb+srv://avfx_root:irmiot4462281@avianfinance.qc7bqtj.mongodb.net/?retryWrites=true&w=majority"
# uri = env_vars["MONGODB_CONNECTION_STRING"]

def get_collections_length():
    try:
        client = MongoClient("mongodb+srv://avfx_root:irmiot4462281@avianfinance.qc7bqtj.mongodb.net/?retryWrites=true&w=majority")
        db = client["AVFX"]
        collection = db["upgraded-contracts"]
        upgraded_contracts = collection.find()
        upgraded_smartcontracts_list =[]
        for contract in upgraded_contracts:
            upgraded_smartcontracts_list.append(contract)
        return (len(upgraded_smartcontracts_list)+1)
    except Exception as e:
        return(e)
    
def insert_collection(new_contract):
    try:
        client = MongoClient("mongodb+srv://avfx_root:irmiot4462281@avianfinance.qc7bqtj.mongodb.net/?retryWrites=true&w=majority")
        db = client["AVFX"]
        collection = db["upgraded-contracts"]
        print(new_contract)
        collection.insert_one(new_contract)
        print("inserted")
    except Exception as e:
        return(e)
    
def get_collections():
    try:
        client = MongoClient("mongodb+srv://avfx_root:irmiot4462281@avianfinance.qc7bqtj.mongodb.net/?retryWrites=true&w=majority")
        db = client["AVFX"]
        collection = db["upgraded-contracts"]
        upgraded_contracts = collection.find()
        upgraded_smartcontracts_list =[]
        for contract in upgraded_contracts:
            upgraded_smartcontracts_list.append(contract)
        return (upgraded_smartcontracts_list)
    except Exception as e:
        return(e)