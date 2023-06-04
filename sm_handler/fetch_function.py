import json
import os

def load_json_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data

def get_file_names(directory):
    file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_names.append(file.split(".")[0])
    return sorted(file_names)

def compare_data_one(full,used):
    used_identifiers = []
    packet = []
    for entry in used:
        used_identifiers.append(entry.split("(")[0])

    for key, value in full.items():
        if key in used_identifiers:
            packet.append([key, value[0], 1])
        else:
            packet.append([key, value[0], 0])

    return(packet)

def compare_data_two(full,used):
    used_identifiers = []
    packet = []
    for entry in used:
        used_identifiers.append(entry[0])

    for key, value in full.items():
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

def load_function(function_path):
    function_data = load_json_file(function_path)
    modifiers_used = function_data['modifiers']
    requires_used = function_data['requires']
    process_used = function_data['body']
    events_used = function_data['events']

    modifiers_all = load_json_file('rules/modifiers.json')
    events_all = load_json_file('rules/events.json')
    requires_all = load_json_file('rules/function.json')['requires']

    function_data["modifiers"] = compare_data_one(modifiers_all,modifiers_used)
    function_data["requires"] = compare_data_two(requires_all,requires_used)
    function_data["events"] = compare_data_one(events_all,events_used)
    function_data["body"] = extract_process_data(process_used)

    with open("testing.json", 'w') as f:
        json.dump(function_data, f, indent=3)

    return(function_data)

def get_available_functions(c_type):
    return(get_file_names("json-functions/" + c_type + "-logic/functions/"))

def get_available_processes():
    return(load_json_file('rules/process.json'))



