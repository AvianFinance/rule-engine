from converters.json_solidity import json_to_solidity

def write_contract(contract_type,check_type):

    try:

        txt_path = "contracts/" + check_type + "/" + contract_type + "_logic.txt"
        sol_path = "contracts/" + check_type + "/" + contract_type + "_logic.sol"

        contract_name = "Avian" + contract_type.capitalize() + "Exchange"

        rules = "/" + check_type + "/" + contract_type + "-logic"

        function_str_list = json_to_solidity(contract_name,rules)

        with open(txt_path, 'w') as file:
            for section in function_str_list:
                file.write(section + "\n")
                
        if (check_type == "pending"):
            with open(sol_path, 'w') as file:
                for section in function_str_list:
                    file.write(section + "\n")

        return("Writing Successful")
    
    except Exception as e:
        print(e)
        return("Writing Failed")


