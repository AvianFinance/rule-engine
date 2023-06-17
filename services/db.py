
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

env_vars = dotenv_values()

uri = "mongodb+srv://avfx_root:irmiot4462281@avianfinance.qc7bqtj.mongodb.net/?retryWrites=true&w=majority"

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
        collection.update_many({ "status": { "$in": ["pending", "deployed"] } }, {"$set": {"status": "overwritten"}})
        collection.insert_one(new_contract)
    except Exception as e:
        return(e)
    
def get_collections():
    try:
        client = MongoClient("mongodb+srv://avfx_root:irmiot4462281@avianfinance.qc7bqtj.mongodb.net/?retryWrites=true&w=majority")
        db = client["AVFX"]
        collection = db["upgraded-contracts"]
        upgraded_contracts = collection.find({}, {"_id": 0})
        upgraded_smartcontracts_list = []
        for contract in upgraded_contracts:
            upgraded_smartcontracts_list.append(contract)
        return (["Success",upgraded_smartcontracts_list])
    except Exception as e:
        return(["Error",e])
    
def getlattest(contract_type):
    try:
        client = MongoClient("mongodb+srv://avfx_root:irmiot4462281@avianfinance.qc7bqtj.mongodb.net/?retryWrites=true&w=majority")
        db = client["AVFX"]
        collection = db["upgraded-contracts"]
        lattestcontract = collection.find({"contract_name": contract_type,"status": "upgraded"},{"_id": 0} ).limit(1);
        upgradedcontracts = []
        for contract in lattestcontract:
            upgradedcontracts.append(contract)
        return (["Success",upgradedcontracts])
    except Exception as e:
        return(["Error",e])
    
def update_collections(contract_address):
    try:
        client = MongoClient("mongodb+srv://avfx_root:irmiot4462281@avianfinance.qc7bqtj.mongodb.net/?retryWrites=true&w=majority")
        db = client["AVFX"]
        collection = db["upgraded-contracts"]
        collection.update_one({"contract_address": contract_address}, {"$set": {"status": "pending"}})
        return("Success")
    except Exception as e:
        return(e)