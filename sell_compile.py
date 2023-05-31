from converters.build_sell import write_imports,write_errors,write_libraries,write_structs,write_events,write_modifiers,write_variables,write_constructor,write_body
from converters.build_sell import edit_string

file_path = "contracts/new/sell_logic.txt"
contract_name = "AvianSellExchange"

to_convert = ["imports","errors","start","libraries","structs","events","modifiers","state_variables","constructor","body","end"]
function_str_list = ["// SPDX-License-Identifier: MIT","pragma solidity ^0.8.4; \n"]

for section in to_convert:

    if (section == "imports"):
        function_str_list.append(edit_string(write_imports(),0))
    elif (section == "errors"):
        function_str_list.append(edit_string(write_errors(),0))
    elif (section == "start"):
        function_str_list.append("contract " + contract_name + " is ReentrancyGuard { \n")

    # Realization of the contract body starts here

    elif (section == "libraries"):
        function_str_list.append(edit_string(write_libraries(),1))
    elif (section == "structs"):
        function_str_list.append(edit_string(write_structs(),1))
    elif (section == "events"):
        function_str_list.append(edit_string(write_events(),1))
    elif (section == "modifiers"):
        function_str_list.append(edit_string(write_modifiers(),1))
    elif (section == "state_variables"):
        function_str_list.append(edit_string(write_variables(),1))
    elif (section == "constructor"):
        function_str_list.append(edit_string(write_constructor(),1))
    elif (section == "body"):
        function_str_list.append(edit_string(write_body(),1))


    # Function body ends here 
    
    elif (section == "end"):
        function_str_list.append("} \n")

with open(file_path, 'w') as file:
    for section in function_str_list:
        file.write(section + "\n")


