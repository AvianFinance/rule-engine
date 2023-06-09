import json
import shutil
import os

def json_rule_updator(data,contract_type,check_or_deploy):

    copy_stable(contract_type,check_or_deploy)

    keys = list(data)

    for item in keys:
        if (item == 'eventsList'):
            print("Processing Event List of contract : " + contract_type )
            rules = data['eventsList']
            processEventList(rules,check_or_deploy, contract_type)

        elif(item =='modifiersList'):
            print("Processing modifiers List of contract : " + contract_type )
            rules = data['modifiersList']
            processModifierList(rules,check_or_deploy, contract_type)

        elif(item =='errorsList'):
            print("Processing errors List of contract : " + contract_type )
            rules = data['errorsList']
            processErrorList(rules,check_or_deploy, contract_type)

        elif(item =='functionlist'):
            print("Processing function list of contract : " + contract_type )
            rules = data['functionlist']
            if bool(rules):
                processFunctionList(rules,check_or_deploy, contract_type)
        
        else:
            print("Unidentified type")

def processEventList(rules,check_or_deploy, contract_type) :
    updated_rules = [sublist[0] for sublist in rules if sublist[2] == 1]
    rule_json = read_json("events.json", updated_rules, "A")
    write_to_json("events.json", rule_json, check_or_deploy, contract_type)

def processModifierList(rules,check_or_deploy, contract_type) :
    updated_rules = [sublist[0] for sublist in rules if sublist[2] == 1]
    rule_json = read_json("modifiers.json", updated_rules, "A")
    write_to_json("modifiers.json", rule_json, check_or_deploy, contract_type)

def processErrorList(rules,check_or_deploy, contract_type) :
    updated_rules = [sublist[0] for sublist in rules if sublist[2] == 1]
    rule_json = read_json("errors.json", updated_rules, "A")
    write_to_json("errors.json", rule_json, check_or_deploy, contract_type)
    
def processFunctionList(rules, check_or_deploy, contract_type) :
    print(rules)

    function_file_mapping = {'listItem': "1_list_item.json",
                              'updateListing': "2_update_listing.json",
                              'cancelListing': "3_cancel_listing.json",
                              'buyItem': "4_buy_item.json",
                              'withdrawProceeds': "5_withdraw.json",
                              'isNFT':"6_is_nft.json"
                              }
    
    function_name = rules['function_name']
    file_name =  function_file_mapping[function_name]

    if not file_name:
        print("Function is not defined or Invalid function name. Check function_file_mapping!!")
    else:
        desired_keys = ['function_name', 'input_parameters', 'visibility','state_mutability', 'returns', 'return_line']
        unchange_data = {key: rules[key] for key in desired_keys}

        processAFunction(rules, unchange_data, file_name, check_or_deploy, contract_type)

def processAFunction(rules, unchanged_data, filename, check_or_deploy, contract_type) :

    filepath = "functions/" + filename
    keys = ['events','modifiers', 'requires', 'body']

    for item in keys:
        
        if(item =='requires'):
            print("Fucntional requires List--------------------")
            require_l = rules['requires']
            updated_requires = [sublist[0] for sublist in require_l if sublist[2] == 1]
            requires_json = read_json("function.json", updated_requires, "C")
            unchanged_data["requires"] = requires_json

        elif(item =='modifiers'):
            print("Fucntional modifiers List-----------------------")
            modifiers_l = rules['modifiers']
            updated_requires = [sublist[0] for sublist in modifiers_l if sublist[2] == 1]
            modifier_json = read_json("modifiers.json", updated_requires, "B")
            unchanged_data["modifiers"] = modifier_json

        elif(item =='events'):
            print("Functional events list------------------")
            events_l = rules['events']
            updated_events = [sublist[0] for sublist in events_l if sublist[2] == 1]
            events_json = read_json("events.json", updated_events, "B")
            unchanged_data["events"] = events_json
        
        elif(item =='body'):
            print("Functional body list----------------")
            available_fn = rules['body'][0]
            values = [item['value'] for item in available_fn]
            print(values)
            body_json = read_json("process.json", values, "D")
            print(body_json)
            unchanged_data["body"] = body_json

        else:
            print("Unidentified type")

    write_to_json(filepath, unchanged_data, check_or_deploy, contract_type)
    
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
    if(method == "D"):
        new_data = [data[key][1] for key in updated_list]
    return new_data

def write_to_json(filename, content, check_or_deploy, contract_type):
    filepath = "json-functions/" + check_or_deploy + "/"+contract_type+"-logic/" + filename
    with open(filepath, 'w') as file:
        json.dump(content, file, indent=1)

    print(filepath + " : Json file updated")

def copy_stable(contract_type,check_or_deploy):
    
    source_folder = 'json-functions/stable/' + contract_type + "-logic"
    destination_folder = 'json-functions/' + check_or_deploy + '/' + contract_type + "-logic"

    if os.path.exists(destination_folder):
        try:
            shutil.rmtree(destination_folder)
            print("Destination folder deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting the destination folder: {str(e)}")

    try:
        shutil.copytree(source_folder, destination_folder)
        print("Folder copied successfully.")
    except FileExistsError:
        print("Destination folder already exists.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

