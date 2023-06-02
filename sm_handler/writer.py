from converters.json_solidity import json_to_solidity

def write_contract(contract_type):

    try:

        file_path = "contracts/new/" + contract_type + "_logic.txt"

        contract_name = "Avian" + contract_type + "Exchange"

        rules = contract_type + "-logic"

        function_str_list = json_to_solidity(contract_name,rules)

        with open(file_path, 'w') as file:
            for section in function_str_list:
                file.write(section + "\n")

        return("Compiling Successful")
    
    except:

        return("Compiling Failed")


