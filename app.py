from flask import Flask, jsonify
from sell_compile import compile
from fetch_rules import fetch_rules

app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/compile')
def say_hello():
  compile()
  return 'Hello from Server'

@app.route('/fetch/<contract_type>/<rule_type>')
def get_contract_level_rules(contract_type,rule_type):
  return jsonify(data=fetch_rules(contract_type,rule_type))