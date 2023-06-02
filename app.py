from flask import Flask, jsonify
from compiler import contract_compile
from services.upload_contract import upload_contract
from fetch_rules import fetch_rules
import asyncio
from flask_cors import CORS
from sm_handler.deploy import compile_export_contract

app = Flask(__name__)

CORS(app)

async def async_upload_contract(contract_name):
    return upload_contract(contract_name)

async def async_deploy_contract(contract_name):
    return compile_export_contract(contract_name)

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/check/<contract_type>', methods = ['POST'])
def write_upload_contract(contract_type):
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
  
@app.route('/deploy/<contract_type>')
def compile_deploy_contract(contract_type):

  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  result = loop.run_until_complete(async_deploy_contract(contract_type.capitalize()))
  loop.close()
  print("result--------------"+ str(result))
  return str(result)
    

@app.route('/fetch/<contract_type>/<rule_type>')
def get_contract_level_rules(contract_type,rule_type):
  return jsonify(data=fetch_rules(contract_type,rule_type))

if __name__ == '__main__':
    app.run(debug=True)
