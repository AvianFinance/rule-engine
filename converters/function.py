import json

def build_function(path): 

    commands = []

    with open(path) as f:
        data = json.load(f)

    command = "function " + data["function_name"] + "(" + data["input_parameters"] + ") " + data["visibility"]

    if (data["state_mutability"] != "none"):
        command = command + " " + data["state_mutability"]

    commands.append(command)

    for modifier in data["modifiers"]:
        command = "\t" + modifier
        commands.append(command)

    commands.append("returns(" + data["returns"] + "){")

    for req in data["requires"]:
        command = "\trequire(" + req[0] + ",'" + req[1] + "');"
        commands.append(command)
    
    commands.append("\n")

    # function body

    # function body ends

    commands.append("\temit " + data["events"] + ";\n")

    commands.append("\treturns('" + data["return_line"] + "');\n}")

    return(commands)

for cmd in build_function('./json-functions/sell-logic/list_item.json'):
    print(cmd)



