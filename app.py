import asyncio
from flask_cors import CORS
from flask import Flask, request, jsonify, make_response


from services.upload_contract import upload_contract
from services.json_rule_updator import json_rule_updator
from services.db import get_collections, update_collections, getlattest
from sm_handler.writer import write_contract
from sm_handler.fetch_rules import fetch_rules
from sm_handler.compiler import compile_export_contract
from sm_handler.com_up_dep import full_flow
from sm_handler.fetch_function import load_function, get_available_functions, get_available_processes

app = Flask(__name__)

CORS(app)

async def async_upload_contract(contract_name,check_type):
    return upload_contract(contract_name,check_type)

async def async_deploy_contract(contract_name):
    return compile_export_contract(contract_name)

@app.route('/')
def index():
    return 'Welcome to the Avian Finance Rule Engine !!!'

@app.route('/check/<contract_type>', methods = ['POST']) # Use this route for the check button usecase
def write_upload_contract(contract_type):
    data = request.get_json()
    json_rule_updator(data,contract_type)
    write_status = write_contract(contract_type,"check")
    if (write_status=="Writing Successful"):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        contract_info = loop.run_until_complete(async_upload_contract(contract_type,"check"))
        loop.close()
        response = make_response(jsonify('https://gateway.pinata.cloud/ipfs/' + str(contract_info)))
        response.status_code = 200  # Set the desired status code
        return response
    else:
        response = make_response("Writing failed")
        response.status_code = 400  # Set the desired status code
        return response

@app.route('/deploy/<contract_type>', methods = ['POST']) # compiles the specified contract in the  "contracts/new/" folder
def deploy_contract(contract_type):
    try:
        data = request.get_json()
        json_rule_updator(data)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print('contract_type',contract_type)
        contract_info = loop.run_until_complete(full_flow(contract_type))
        loop.close()
        print('contract_info',contract_info)
        if(contract_info[0] != 0):
            response = make_response(jsonify(ipfs=contract_info[0],contract_addr=contract_info[1]))
            response.status_code = 200  # Set the desired status code
            return response
        else:
            response = make_response("Error occured")
            response.status_code = 400  # Set the desired status code
            return response
    except:
        response = make_response("deploying failed")
        response.status_code = 400  # Set the desired status code
        return response
    
@app.route('/fetch/<contract_type>/<rule_type>') # fetch contract level data
def get_contract_level_rules_individually(contract_type,rule_type):
    return jsonify(data=fetch_rules(contract_type,rule_type))

@app.route('/fetch_contract/<contract_type>') # fetch contract level data
def get_contract_level_rules(contract_type):
    try:
        errors=fetch_rules(contract_type,"errors")
        print('errors----------------',errors)
        events=fetch_rules(contract_type,"events")
        modifiers=fetch_rules(contract_type,"modifiers")
        response = make_response(jsonify(errors=errors,events=events,modifiers=modifiers))
        response.status_code = 200  # Set the desired status code
        return response
    except:
        response = make_response("Network Error")
        response.status_code = 400  # Set the desired status code
        return response

@app.route('/fetch_function/<contract_type>/<function_name>') # fetch function level data
def get_function_level_rules(contract_type,function_name):
    path = "json-functions/" + str(contract_type) + "-logic/functions/" + str(function_name) + ".json"
    return jsonify(data=load_function(path))

@app.route('/available_function/<contract_type>') # fetch available functions for a given contract
def get_contract_functions(contract_type):
    data=get_available_functions(contract_type)
    if(data[0]=="Success"):
        response = make_response(jsonify(data=data[1]))
        response.status_code = 200  # Set the desired status code
        return response
    else:
        response = make_response(jsonify("Error Occured"))
        response.status_code = 400  # Set the desired status code
        return response

@app.route('/available_process') # fetch available processes
def get_processes():
    data=get_available_processes()
    if(data[0]=="Success"):
        response = make_response(jsonify(data=data[1]))
        response.status_code = 200  # Set the desired status code
        return response
    else:
        response = make_response(jsonify("Error Occured"))
        response.status_code = 400  # Set the desired status code
        return response

@app.route('/upgraded_contracts')
def get_upgraded_contracts():
    data=get_collections()
    if(data[0]=="Success"):
        response = make_response(jsonify(data=data[1]))
        response.status_code = 200  # Set the desired status code
        return response
    else:
        response = make_response(jsonify("Error Occured"))
        response.status_code = 400  # Set the desired status code
        return response

@app.route('/lattestcontract/<contract_type>') # fetch available functions for a given contract
def get_lattest_contract(contract_type):
    data=getlattest(contract_type)
    print('data-----------------------',data)
    if(data[0]=="Success"):
        response = make_response(jsonify(data=data[1]))
        response.status_code = 200  # Set the desired status code
        return response
    else:
        response = make_response(jsonify("Error Occured"))
        response.status_code = 400  # Set the desired status code
        return response


@app.route('/created_proposal/<address>')
def created_proposal(address):
    if(update_collections(address)=="Success"):
        response = make_response(jsonify("Successful"))
        response.status_code = 200  # Set the desired status code
        return response
    else:
        response = make_response(jsonify("Error Occured"))
        response.status_code = 400  # Set the desired status code
        return response

if __name__ == '__main__':
    app.run(debug=True)
