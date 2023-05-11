import json

def write_imports(): # Isuru

    commands = []

    with open('./json-functions/sell-logic/imports.json') as f:
        data = json.load(f)

    for key, value in data.items():
        commands.append("import " + str(value)+ ";")

    return(commands)

def write_errors(): # Isuru

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
        command = "modifier " + str(key)
        for param in value:
            command = command + "\t"*2 + str(param) + "\n"
        command = command + "\t}\n"
        commands.append(command)

    return(commands)


def edit_string(strings, X):
    concatenated_string = ""

    for string in strings:
        tabbed_string = "\t" * X + string
        concatenated_string += tabbed_string + "\n"

    print(concatenated_string)
    return concatenated_string

