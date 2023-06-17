import json
import os

def load_json_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data

def get_type_index(contract_name):
    if contract_name == "sell":
        return(0)
    elif contract_name == "rent":
        return(1)
    elif contract_name == "ins":
        return(2)

def get_file_names(directory):
    file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_names.append(file.split(".")[0])
    return sorted(file_names)

def compare_data_one(full,used,c_index):
    used_identifiers = []
    packet = []
    for entry in used:
        used_identifiers.append(entry.split("(")[0])

    for key, value in full.items():
        if value[3][c_index] == 1:
            if key in used_identifiers:
                packet.append([key, value[0], 1])
            else:
                packet.append([key, value[0], 0])

    return(packet)

def compare_data_two(full,used, c_index):
    used_identifiers = []
    packet = []
    for entry in used:
        used_identifiers.append(entry[0])

    for key, value in full.items():
        if value[2][c_index] == 1:
            if value[1][0] in used_identifiers:
                packet.append([key, value[0], 1])
            else:
                packet.append([key, value[0], 0])

    return(packet)

def extract_process_data(used):
    packet = []
    for i in range(len(used)):
        packet.append([i,used[i][0]])

    return(packet)

def load_function(contract_type, function_name):

    function_path = "json-functions/stable/" + str(contract_type) + "-logic/functions/" + str(function_name) + ".json"

    function_data = load_json_file(function_path)
    modifiers_used = function_data['modifiers']
    requires_used = function_data['requires']
    process_used = function_data['body']
    events_used = function_data['events']

    c_index = get_type_index(contract_type)

    modifiers_all = load_json_file('rules/modifiers.json')
    events_all = load_json_file('rules/events.json')
    requires_all = load_json_file('rules/function.json')['requires']
    avaiableprocess = get_available_processes(c_index)

    function_data["modifiers"] = compare_data_one(modifiers_all,modifiers_used,c_index)
    function_data["requires"] = compare_data_two(requires_all,requires_used,c_index)
    function_data["events"] = compare_data_one(events_all,events_used,c_index)
    function_data["body"] = [extract_process_data(process_used),avaiableprocess[1]]

    return(function_data)

def get_available_functions(c_type):
    try:
        return(["Success", get_file_names("json-functions/stable/" + c_type + "-logic/functions/")])
    except Exception as e:
        return (["Error", e])

def get_available_processes(c_index):
    try:
        full_processes = load_json_file('rules/process.json')
        packet = []
        for key, value in full_processes.items():
            if value[2][c_index] == 1:
                packet.append([key, value[0]])
        return (["Success",packet])
    except Exception as e:
        return (["Error", e])



