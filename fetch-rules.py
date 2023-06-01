import json

def compare_json_files(larger_file_path, smaller_file_path):
    larger_json = load_json_file(larger_file_path)
    smaller_json = load_json_file(smaller_file_path)

    comparison_result = []
    is_subset = True

    for key, value in larger_json.items():
        if key in smaller_json and smaller_json[key] == value:
            comparison_result.append([key, True])
        else:
            comparison_result.append([key, False])
            is_subset = False

    return comparison_result


def load_json_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data


print(compare_json_files("rules/events.json","json-functions/sell-logic/events.json"))
