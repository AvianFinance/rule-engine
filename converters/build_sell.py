import json
from converters.build_function import build_function
import os

type = "ins-logic"
# type = "rent-logic"
# type = "sell-logic"

def write_imports(): 

    commands = []

    with open('./json-functions/sell-logic/imports.json') as f:
        data = json.load(f)

    for key, value in data.items():
        commands.append('import "' + value + '";')

    return(commands)

def write_errors():

    commands = []
    with open('./json-functions/sell-logic/errors.json') as f:
        data = json.load(f)
    for key, value in data.items():
        commands.append("error " + str(value) + ";")

    return(commands)

def write_libraries(): # Isuru

    commands = []
    
    with open('./json-functions/sell-logic/libraries.json') as f:
        data = json.load(f)
    for key, value in data.items():
        commands.append("using " + str(value) + ";")

    return(commands)

def write_structs():

    commands = []

    with open('./json-functions/sell-logic/structs.json') as f:
        data = json.load(f)

    for key, value in data.items():
        command = "struct " + str(key) + " {"
        for param in value:
            command = command + str(param) + ";"
        command = command + "}"
        commands.append(command)

    return(commands)

def write_events():

    commands = []

    with open('./json-functions/sell-logic/events.json') as f:
        data = json.load(f)

    for key, value in data.items():
        command = "event " + str(key) + "("
        for param in value:
            command = command + str(param) + ","
        command = command[:-1] + ");"
        commands.append(command)

    return(commands)

def write_modifiers():

    commands = []

    with open('./json-functions/sell-logic/modifiers.json') as f:
        data = json.load(f)

    for key, value in data.items():
        command = "modifier " + str(key) + value[0] + "\n"
        for i in range(1,len(value)):
            command = command + "\t"*2 + str(value[i]) + "\n"
        command = command + "\t}\n"
        commands.append(command)

    return(commands)

def write_variables():

    commands = ["// state variables to match as in the proxy context (order should be maintained)\n"]
    with open('./json-functions/sell-logic/state_variables.json') as f:
        data = json.load(f)
    for key, value in data.items():
        commands.append(str(value) + ";\n")

    return(commands)

def write_constructor():

    commands = ["constructor() {"]
    with open('./json-functions/sell-logic/constructor.json') as f:
        data = json.load(f)
    for key, value in data.items():
        commands.append("\t" + str(value) + ";")

    commands.append("}\n")

    return(commands)

def write_body():

    directory = "./json-functions/sell-logic/functions/"  # Replace with the actual directory path

    file_paths = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            file_paths.append(filepath)

    file_paths = sorted(file_paths)

    commands = []

    for function_name in file_paths:
        for f_body in build_function(function_name):
            commands.append(f_body)

    return(commands)

def edit_string(strings, X):
    concatenated_string = ""

    for string in strings:
        tabbed_string = "\t" * X + string
        concatenated_string += tabbed_string + "\n"

    return concatenated_string
