import json

def compare_json_files(larger_file_path, smaller_file_path,contract_name):

    c_types = ["sell","rent","ins"]

    c_types.pop(c_types.index(contract_name))

    cond = False

    larger_json = load_json_file(larger_file_path)
    smaller_json = load_json_file(smaller_file_path)

    comparison_result = []

    cond = False

    for key, value in larger_json.items():

        if ((c_types[0].capitalize() not in key) and (c_types[1].capitalize() not in key)):
            if key in smaller_json:
                comparison_result.append([key, value[0], 1])
            else:
                comparison_result.append([key, value[0], 0])

    return comparison_result


def load_json_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data

def fetch_rules(contract_name,rule_type):

    all_rules_path = "rules/" + rule_type + ".json"
    cuurent_rules_paths = "json-functions/stable/" + str(contract_name) + "-logic/" + str(rule_type) + ".json"

    return(compare_json_files(all_rules_path,cuurent_rules_paths,contract_name))