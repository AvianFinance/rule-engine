import json
from converters.build_rule import build_rule

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
    
    commands.append("")

    # function body

    if (len(data["body"])>0):
        for rule_data in data["body"]:
            rule_strings = build_rule(rule_data[0],rule_data[1])
            for command in rule_strings:
                commands.append("\t"+command)

    # function body ends

    if (len(data["events"])>0):
        for event in data['events']:
            commands.append("\temit " + event + ";\n")

    if (len(list(data["return_line"]))>0):
        commands.append("\treturn(" + data["return_line"] + ");\n\t}\n")
    else:
        commands.append("}\n")


    return(commands)



