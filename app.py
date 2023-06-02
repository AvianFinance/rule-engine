import asyncio
from flask_cors import CORS
import json
from flask import Flask, jsonify, request

from services.upload_contract import upload_contract
from services.db import get_collections, insert_collection, get_collections_length
from sm_handler.writer import write_contract
from sm_handler.fetch_rules import fetch_rules
from sm_handler.compiler import compile_export_contract
from sm_handler.com_up_dep import full_flow

app = Flask(__name__)

CORS(app)

async def async_upload_contract(contract_name):
    return upload_contract(contract_name)

async def async_deploy_contract(contract_name):
    return compile_export_contract(contract_name)

@app.route('/')
def index():
  return 'Welcome to the Avian Finance Rule Engine !!!'
  
@app.route('/check/<contract_type>', methods = ['POST']) # Use this route for the check button usecase
def write_upload_contract(contract_type):

  compile_status = write_contract(contract_type)
  if (compile_status=="Compiling Successful"):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_upload_contract(contract_type))
    loop.close()
    return jsonify('https://gateway.pinata.cloud/ipfs/' + str(result))
  else:
    return("compiling failed")
  
@app.route('/deploy/<contract_type>')
def deploy_contract(contract_type):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(full_flow(contract_type))
    loop.close()
    return result
    
@app.route('/fetch/<contract_type>/<rule_type>')
def get_contract_level_rules(contract_type,rule_type):
  return jsonify(data=fetch_rules(contract_type,rule_type))

@app.route('/upgraded_contracts')
def get_upgraded_contracts():
  return jsonify(data=get_collections())

if __name__ == '__main__':
    app.run(debug=True)
