from flask import Flask, jsonify, request
from compiler import contract_compile
from services.upload_contract import upload_contract
from fetch_rules import fetch_rules
from db import get_collections, insert_collection, get_collections_length
import asyncio
from flask_cors import CORS
import json

app = Flask(__name__)

CORS(app)

async def async_upload_contract(contract_name):
    return upload_contract(contract_name)

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/compile/<contract_type>', methods = ['POST'])
def compile_upload_contract(contract_type):
  compile_status = contract_compile(contract_type)
  if (compile_status=="Compiling Successful"):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_upload_contract(contract_type))
    loop.close()
    print("result--------------"+ str(result))
    return jsonify('https://gateway.pinata.cloud/ipfs/' + str(result))
  else:
    return("compiling failed")
  
@app.route('/deploy/<contract_type>', methods = ['POST'])
def deploy_contract(contract_type):

  compile_status = contract_compile(contract_type)
  print("hiii")
  if (compile_status=="Compiling Successful"):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_upload_contract(contract_type))
    loop.close()
    print("result--------------"+ str(result))
    url = 'https://gateway.pinata.cloud/ipfs/' + str(result)
    body = request.data
    data = json.loads(body)
    # for key, value in data.items():
    #   print(key, value)
    id = get_collections_length()
    print(id)
    new_contract = {
      "id": id,
      "contract_name": contract_type,
      "contract_address": "",
      "address": url,
      "events": data["eventsList"],
      "modifiers": data["modifiersList"],
      "errors": data["errorsList"],
      "status" : "active"
    }
    insert_collection(new_contract)

    # return jsonify('https://gateway.pinata.cloud/ipfs/' + str(result))
    return jsonify("url")
  else:
    return("compiling failed")
    

@app.route('/fetch/<contract_type>/<rule_type>')
def get_contract_level_rules(contract_type,rule_type):
  return jsonify(data=fetch_rules(contract_type,rule_type))

@app.route('/upgraded_contracts')
def get_upgraded_contracts():
  return jsonify(data=get_collections())

if __name__ == '__main__':
    app.run(debug=True)
