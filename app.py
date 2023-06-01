from flask import Flask, jsonify
from compiler import contract_compile
from services.upload_contract import upload_contract
from fetch_rules import fetch_rules
import asyncio
from flask_cors import CORS

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
    

@app.route('/fetch/<contract_type>/<rule_type>')
def get_contract_level_rules(contract_type,rule_type):
  return jsonify(data=fetch_rules(contract_type,rule_type))

if __name__ == '__main__':
    app.run(debug=True)
