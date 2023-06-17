import json
import shutil
import os
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)

def json_rule_updator(data,contract_type,check_or_pending):

    copy_stable(contract_type,check_or_pending)

    logging.info('User accessed the json rule updater')

    keys = list(data)

    for item in keys:
        if (item == 'eventsList'):
            logging.info("Processing Event List of contract : " + contract_type )
            rules = data['eventsList']
            logging.info("Event List provided from FE : " + str(rules) )
            processEventList(rules,check_or_pending, contract_type)

        elif(item =='modifiersList'):
            logging.info("Processing modifiers List of contract : " + contract_type )
            rules = data['modifiersList']
            logging.info("Modifier List provided from FE : " + str(rules) )
            processModifierList(rules,check_or_pending, contract_type)

        elif(item =='errorsList'):
            logging.info("Processing errors List of contract : " + contract_type )
            rules = data['errorsList']
            logging.info("Error List provided from FE : " + str(rules) )
            processErrorList(rules,check_or_pending, contract_type)

        elif(item =='functionlist'):
            logging.info("Processing function list of contract : " + contract_type )
            rules = data['functionlist']
            logging.info("Function List provided from FE : " + str(rules) )
            if bool(rules):
                processFunctionList(rules,check_or_pending, contract_type)
        
        else:
            print("Unidentified type")

def processEventList(rules,check_or_pending, contract_type) :
    updated_rules = [sublist[0] for sublist in rules if sublist[2] == 1]
    rule_json = read_json("events.json", updated_rules, "A")
    logging.info("Writing contract level events")
    write_to_json("events.json", rule_json, check_or_pending, contract_type)

def processModifierList(rules,check_or_pending, contract_type) :
    updated_rules = [sublist[0] for sublist in rules if sublist[2] == 1]
    rule_json = read_json("modifiers.json", updated_rules, "A")
    logging.info("Writing contract level modifiers")
    write_to_json("modifiers.json", rule_json, check_or_pending, contract_type)

def processErrorList(rules,check_or_pending, contract_type) :
    updated_rules = [sublist[0] for sublist in rules if sublist[2] == 1]
    rule_json = read_json("errors.json", updated_rules, "A")
    logging.info("Writing contract level errors")
    write_to_json("errors.json", rule_json, check_or_pending, contract_type)
    
def processFunctionList(rules, check_or_pending, contract_type) :

    sell_function_file_mapping = {'listItem': "1_list_item.json",
                              'updateListing': "2_update_listing.json",
                              'cancelListing': "3_cancel_listing.json",
                              'buyItem': "4_buy_item.json",
                              'withdrawProceeds': "5_withdraw.json",
                              'isNFT':"6_is_nft.json",
                              'isRentableNFT':"7_is_rentable_nft.json",
                              'isNotRented':"8_marketplace_approved.json",
                              'isNotRented':"9_is_not_rented.json"
                              }
    
    rent_function_file_mapping = {'listNFT': "1_listNFT.json",
                              'unlistNFT': "2_unlistNFT.json",
                              'updateRentNFT': "3_updateRentNFT.json",
                              'rentNFT': "4_rentNFT.json",
                              'isRentableNFT': "5_isRentableNFT.json",
                              'isNFT':"6_isNFT.json",
                              'MarketplaceIsApproved': "7_marketplace_approved.json",
                              'isNotRented' : "8_is_not_rented.json"
                              }
    
    ins_function_file_mapping = {'listInsBasedNFT': "1_listInsBasedNFT.json",
                              'unlistINSNFT': "2_unlistNFT.json",
                              'rentINSNFT': "3_rentINSNFT.json",
                              'calculateInstallment': "4_calculateInstallment.json",
                              'payNFTIns': "5_payNFTIns.json",
                              'isRentableNFT':"6_isRentableNFT.json",
                              'isNFT': "7_isNFT.json",
                              'MarketplaceIsApproved' : "8_marketplace_approved.json"
                              }
    
    function_name = rules['function_name']

    if (contract_type == "sell"):
        file_name =  sell_function_file_mapping[function_name]
    if (contract_type == "rent"):
        file_name =  rent_function_file_mapping[function_name]
    if (contract_type == "ins"):
        file_name =  ins_function_file_mapping[function_name]

    if not file_name:
        print("Function is not defined or Invalid function name. Check function_file_mapping!!")
    else:
        desired_keys = ['function_name', 'input_parameters', 'visibility','state_mutability', 'returns', 'return_line']
        unchange_data = {key: rules[key] for key in desired_keys}

        processAFunction(rules, unchange_data, file_name, check_or_pending, contract_type)

def processAFunction(rules, unchanged_data, filename, check_or_deploy, contract_type) :

    filepath = "functions/" + filename
    keys = ['events','modifiers', 'requires', 'body']

    for item in keys:
        
        if(item =='requires'):
            logging.info("Handling function Reqirues rules")
            require_l = rules['requires']
            updated_requires = [sublist[0] for sublist in require_l if sublist[2] == 1]
            requires_json = read_json("function.json", updated_requires, "C")
            unchanged_data["requires"] = requires_json

        elif(item =='modifiers'):
            logging.info("Handling function Modifier rules")
            modifiers_l = rules['modifiers']
            updated_requires = [sublist[0] for sublist in modifiers_l if sublist[2] == 1]
            modifier_json = read_json("modifiers.json", updated_requires, "B")
            unchanged_data["modifiers"] = modifier_json

        elif(item =='events'):
            logging.info("Handling function Event rules")
            events_l = rules['events']
            updated_events = [sublist[0] for sublist in events_l if sublist[2] == 1]
            events_json = read_json("events.json", updated_events, "B")
            unchanged_data["events"] = events_json
        
        elif(item =='body'):
            logging.info("Handling function body rules")
            available_fn = rules['body'][0]
            values = [item[1] for item in available_fn]
            logging.info("function rules in order: %s", ', '.join(str(item) for item in values))
            body_json = read_json("process.json", values, "D")
            unchanged_data["body"] = body_json

        else:
            print("Unidentified type")

    logging.info("Writing selected function json")
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
        json.dump(content, file, indent=2)
        

    print(filepath + " : Json file updated")

def copy_stable(contract_type,check_or_pending):
    
    source_folder = 'json-functions/stable/' + contract_type + "-logic"
    destination_folder = 'json-functions/' + check_or_pending + '/' + contract_type + "-logic"

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

