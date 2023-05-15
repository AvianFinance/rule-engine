import json

def build_function(path): 

    commands = []

    with open(path) as f:
        data = json.load(f)

    command = "function " + data["function_name"] + "(" + data["input_parameters"] + ") " + data["visibility"]

    if (data["state_mutability"] != "none"):
        command = command + " " + data["state_mutability"]

    commands.append(command)

    if (len(data["modifiers"])>0):
        for modifier in data["modifiers"]:
            command = "\t" + modifier
            commands.append(command)

    commands.append("returns(" + data["returns"] + "){")

    if (len(data["requires"])>0):
        for req in data["requires"]:
            command = "\trequire(" + req[0] + ",'" + req[1] + "');"
            commands.append(command)
    
    commands.append("\n")

    # function body

    # function body ends

    if (len(data["events"])>0):
        commands.append("\temit " + data["events"] + ";\n")

    commands.append("\treturns(" + data["return_line"] + ");\n\t}\n")

    return(commands)



