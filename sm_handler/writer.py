from converters.json_solidity import json_to_solidity

def write_contract(contract_type):

    try:

        txt_path = "contracts/new/" + contract_type + "_logic.txt"
        sol_path = "contracts/new/" + contract_type + "_logic.sol"

        contract_name = "Avian" + contract_type + "Exchange"

        rules = contract_type + "-logic"

        function_str_list = json_to_solidity(contract_name,rules)

        with open(txt_path, 'w') as file:
            for section in function_str_list:
                file.write(section + "\n")
        with open(sol_path, 'w') as file:
            for section in function_str_list:
                file.write(section + "\n")

        return("Writing Successful")
    
    except Exception as e:
        print(e)
        return("Writing Failed")


