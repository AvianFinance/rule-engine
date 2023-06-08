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

    desired_keys = ['function_name', 'input_parameters', 'visibility','state_mutability', 'returns', 'return_line']
    unchange_data = {key: rules[key] for key in desired_keys}

    if (function_name == 'listItem'):
        unchange_data['body'] = [["is_approved",["nftAddress","tokenId"]],["write_listing",["nftAddress","tokenId","price"]]]
        processAFunction(rules, unchange_data, "functions/1_list_item.json")
    elif (function_name == 'updateListing'):
        unchange_data['body'] = [["update_listing",["nftAddress","tokenId","newPrice"]]]
        processAFunction(rules, unchange_data, "functions/2_update_listing.json")
    elif (function_name == 'cancelListing'):
        unchange_data['body'] = [["delete_listing",["nftAddress","tokenId"]]]
        processAFunction(rules, unchange_data, "functions/3_cancel_listing.json")
    elif (function_name == 'buyItem'):
        unchange_data['body'] = [["is_approved",["nftAddress","tokenId"]],["load_listing",["sell","nftAddress","tokenId"]],["is_price_met",[]],["add_proceeds",["sell"]],["delete_listing",["nftAddress","tokenId"]],["owner_transfer",["nftAddress","tokenId"]]]
        processAFunction(rules, unchange_data, "functions/4_buy_item.json")
    elif (function_name == 'withdrawProceeds'):
        unchange_data['body'] = [["withdraw_proceeds",["sell"]]]
        processAFunction(rules, unchange_data, "functions/5_withdraw.json")
    elif (function_name == 'isNFT'):
        unchange_data['body'] = [["isNFT", ["nftContract", "tokenId"]]]
        processAFunction(rules, unchange_data, "functions/6_is_nft.json")
    else:
        print("Unidentified function")

def processAFunction(rules, unchanged_data, filename) :

    keys = ['events','modifiers', 'requires']

    for item in keys:
        
        if(item =='requires'):
            print("Fucntional requires List")
            print("-----------------------------------")
            require_l = rules['requires']
            updated_requires = [sublist[0] for sublist in require_l if sublist[2] == 1]
            requires_json = read_json("function.json", updated_requires, "C")
            unchanged_data["requires"] = requires_json

        elif(item =='modifiers'):
            print("Fucntional modifiers List")
            print("-----------------------------------")
            modifiers_l = rules['modifiers']
            updated_requires = [sublist[0] for sublist in modifiers_l if sublist[2] == 1]
            modifier_json = read_json("modifiers.json", updated_requires, "B")
            unchanged_data["modifiers"] = modifier_json

        elif(item =='events'):
            print("Functional events list")
            print("-----------------------------------")
            events_l = rules['events']
            updated_events = [sublist[0] for sublist in events_l if sublist[2] == 1]
            events_json = read_json("events.json", updated_events, "B")
            unchanged_data["events"] = events_json
        else:
            print("Unidentified type")

    # print(unchanged_data)
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
        json.dump(content, file, indent=1)

    print(filepath + " : Json file updated")
