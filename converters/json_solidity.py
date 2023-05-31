from converters.build_contract import write_imports,write_errors,write_libraries,write_structs,write_events,write_modifiers,write_variables,write_constructor,write_body
from converters.build_contract import edit_string

def json_to_solidity(contract_name,c_type):

    to_convert = ["imports","errors","start","libraries","structs","events","modifiers","state_variables","constructor","body","end"]

    function_str_list = ["// SPDX-License-Identifier: MIT","pragma solidity ^0.8.4; \n"]

    for section in to_convert:

        if (section == "imports"):
            function_str_list.append(edit_string(write_imports(c_type),0))
        elif (section == "errors"):
            function_str_list.append(edit_string(write_errors(c_type),0))
        elif (section == "start"):
            function_str_list.append("contract " + contract_name + " is ReentrancyGuard { \n")
        elif (section == "libraries"):
            function_str_list.append(edit_string(write_libraries(c_type),1))
        elif (section == "structs"):
            function_str_list.append(edit_string(write_structs(c_type),1))
        elif (section == "events"):
            function_str_list.append(edit_string(write_events(c_type),1))
        elif (section == "modifiers"):
            function_str_list.append(edit_string(write_modifiers(c_type),1))
        elif (section == "state_variables"):
            function_str_list.append(edit_string(write_variables(c_type),1))
        elif (section == "constructor"):
            function_str_list.append(edit_string(write_constructor(c_type),1))
        elif (section == "body"):
            function_str_list.append(edit_string(write_body(c_type),1))
        elif (section == "end"):
            function_str_list.append("} \n")
        
    return function_str_list



