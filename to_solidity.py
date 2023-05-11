def generate_function_string(function_name, input_params, visibility, state_mutability, modifiers, return_info, require_statement, event_name, return_line):
    function_string = f"function {function_name}({input_params}) {visibility} {state_mutability}\n    {modifiers[0]}\n    {modifiers[1]}\nreturns ({return_info}) {{\n"
    function_string += f"    require({require_statement}, \"Error message\");\n"
    function_string += f"    // function body\n\n"
    function_string += f"    emit {event_name};\n"
    function_string += f"    // return statement\n    return ({return_line});\n}}"
    return function_string

f_content = generate_function_string(state["function_name"],state["input_parameters"],state["visibility"],state["state_mutability"],state["modifiers"],state["returns"],state["requires"],state["events"],state["return_line"])

def save_python_commands_to_file(command, file_name):
    # open the file for writing
    with open(file_name, 'w') as f:
        # write each command in the list to the file
        f.write(command)

save_python_commands_to_file(f_content, "try.txt")