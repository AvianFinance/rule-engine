import json

def load_json_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data

def load_function(function_path):
    function_data = load_json_file(function_path)
    modifiers_used = function_data['modifiers']
    requires_used = function_data['requires']
    rules_used = function_data['body']

    print(modifiers_used)
    print(requires_used)
    print(rules_used)

