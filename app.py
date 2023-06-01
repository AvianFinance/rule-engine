from flask import Flask
from sell_compile import compile
app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/compile')
def say_hello():
  compile()
  return 'Hello from Server'