import json

def json_rule_updator(data):
    # print(data)
    keys = list(data)

    for item in keys:
        if (item == 'eventsList'):
            print("Processing Event List")
            rules = data['eventsList']
            processEventList(rules)
               
        elif(item =='modifiersList'):
            print("Processing modifiers List")
            rules = data['modifiersList']
            processModifierList(rules)

        elif(item =='errorsList'):
            print("Processing errors List")
            rules = data['errorsList']
            processErrorList(rules)

        elif(item =='functionlist'):
            print("Processing function list")
            rules = data['functionlist']
            if bool(rules):
                processFunctionList(rules)
        
        else:
            print("Unidentified type")
         
    return 1


def processEventList(rules) :
    updated_rules = [sublist[0] for sublist in rules if sublist[2] == 1]
    rule_json = read_json("events.json", updated_rules, "A")
    write_to_json("events.json", rule_json)

def processModifierList(rules) :
    updated_rules = [sublist[0] for sublist in rules if sublist[2] == 1]
    rule_json = read_json("modifiers.json", updated_rules, "A")
    write_to_json("modifiers.json", rule_json)

def processErrorList(rules) :
    updated_rules = [sublist[0] for sublist in rules if sublist[2] == 1]
    rule_json = read_json("errors.json", updated_rules, "A")
    write_to_json("errors.json", rule_json)
    
def processFunctionList(rules) :
    function_name = rules['function_name']

    desired_keys = ['function_name', 'input_parameters', 'return_line', 'returns', 'state_mutability', 'visibility']
    unchange_data = {key: rules[key] for key in desired_keys}

    if (function_name == 'listItem'):
        processAFunction(rules, unchange_data, "functions/1_list_item.json")
    else:
        print("Unidentified function")

def processAFunction(rules, unchanged_data, filename) :
    # print(rules)

    keys = ['body', 'events','modifiers', 'requires']
    print(unchanged_data)

    for item in keys:
        if (item == 'body'):
            print("Processing body List")
            print("-----------------------------------")
            # body_l = rules['body']
            # print(body_l)
            # updated_rules = [sublist[0] for sublist in a if sublist[2] == 1]
            # print(updated_rules)
        
        elif(item =='requires'):
            print("Processing requires List")
            print("-----------------------------------")
            require_l = rules['requires']
            updated_requires = [sublist[0] for sublist in require_l if sublist[2] == 1]
            requires_json = read_json("function.json", updated_requires, "C")
            print(requires_json)
            unchanged_data["requires"] = requires_json

        elif(item =='modifiers'):
            print("Processing modifiers List")
            print("-----------------------------------")
            modifiers_l = rules['modifiers']
            updated_requires = [sublist[0] for sublist in modifiers_l if sublist[2] == 1]
            modifier_json = read_json("modifiers.json", updated_requires, "B")
            unchanged_data["modifiers"] = modifier_json

        elif(item =='events'):
            print("Processing events list")
            print("-----------------------------------")
            events_l = rules['events']
            updated_events = [sublist[0] for sublist in events_l if sublist[2] == 1]
            events_json = read_json("events.json", updated_events, "B")
            unchanged_data["events"] = events_json
        else:
            print("Unidentified type")

        print(unchanged_data)
        write_to_json(filename, unchanged_data)
    
def read_json(filename, updated_list, method):
    filepath = "rules/" + filename
    with open(filepath) as file:
        data = json.load(file)

    # Create the new JSON object
    if(method == "A") :
        new_data = {key: data[key][1] for key in updated_list}
    if(method == "B"):
        dictionary_data = {data[key][2] for key in updated_list}
        new_data = list(dictionary_data)
    if(method == "C"):
        r_list = data['requires']
        new_data = [r_list[key][1] for key in updated_list]
    return new_data

def write_to_json(filename, content):
    filepath = "json-functions/sell-logic/" + filename
    # Write the new JSON object to a JSON file
    with open(filepath, 'w') as file:
        json.dump(content, file, indent=4)

    print(filepath + " : Json file updated")
