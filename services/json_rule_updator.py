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
    rule_json = read_json("events.json", updated_rules)
    write_to_json("events.json", rule_json)

def processModifierList(rules) :
    updated_rules = [sublist[0] for sublist in rules if sublist[2] == 1]
    rule_json = read_json("modifiers.json", updated_rules)
    write_to_json("modifiers.json", rule_json)

def processErrorList(rules) :
    updated_rules = [sublist[0] for sublist in rules if sublist[2] == 1]
    rule_json = read_json("errors.json", updated_rules)
    write_to_json("errors.json", rule_json)
    
def processFunctionList(rules) :
    print(rules)
    function_name = rules['function_name']
    print(function_name)

    if (function_name == 'listItem'):
        print("Go to the function")
    else:
        print("Unidentified function")

def processAFunction(rules) :
    print(rules)
    keys = list(rules)
    print("Keysss")
    print(keys)

    for item in keys:
        if (item == 'body'):
            print("Processing body List")
            print("-----------------------------------")
            a = rules['body']
            print(a)
        
        elif(item =='requires'):
            print("Processing Event List")
            print("-----------------------------------")
            a = rules['requires']
            print(a)

        elif(item =='modifiers'):
            print("Processing errors List")
            print("-----------------------------------")
            a = rules['modifiers']
            processErrorList(a)

        elif(item =='events'):
            print("Processing function list")
            print("-----------------------------------")
            a = rules['functionlist']
            processFunctionList(a)
        
        else:
            print("Unidentified type")
    
def read_json(filename, updated_list):
    filepath = "rules/" + filename
    with open(filepath) as file:
        data = json.load(file)

    # Create the new JSON object
    new_data = {key: data[key][1] for key in updated_list}
    return new_data

def write_to_json(filename, content):
    filepath = "json-functions/sell-logic/" + filename
    # Write the new JSON object to a JSON file
    with open(filepath, 'w') as file:
        json.dump(content, file, indent=4)

    print(filepath + " : Json file updated")