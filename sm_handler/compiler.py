import os
from solcx import compile_standard, set_solc_version, install_solc
import json

def compile_export_contract(c_type):

    try:

        contract_path = 'contracts/pending/' + c_type + '_logic.sol'
        output_folder = 'abis'
        contract_name = 'Avian' + c_type.capitalize() + 'Exchange'

        with open(contract_path, 'r') as f: # Read the contract file
            contract_source_code = f.read()

        install_solc('0.8.9')
        set_solc_version('0.8.9')

        compiled_sol = compile_standard( # Compile the contract
            {
                "language": "Solidity",
                "sources": {
                    os.path.basename(contract_path): {
                        "content": contract_source_code
                    }
                },
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "evm.bytecode.object"]
                        }
                    }
                }
            },
        )

        contract_abi = compiled_sol['contracts'][os.path.basename(contract_path)][contract_name]['abi']

        contract_bcode = compiled_sol['contracts'][os.path.basename(contract_path)][contract_name]["evm"]["bytecode"]["object"]

        result = {
            "abi" : contract_abi,
            "bytecode" : contract_bcode
        }

        abi_file_path = os.path.join(output_folder, str(contract_name + '.json'))
        with open(abi_file_path, 'w') as f:
            json.dump(result, f, indent=4)

        return("Succesful")
    
    except Exception as e:
        print(e)
        return("Failes")