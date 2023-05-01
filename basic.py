import xml.etree.ElementTree as ET

def get_input_code(variable_name):
    return f'{variable_name} = input("Enter a value for {variable_name}: ")'

def print_variable_to_terminal(variable_name):
    return(f'print({variable_name})')

def replace_target_string(strings_list, target_string, new_string):
    new_list = [s.replace(target_string, new_string) for s in strings_list]
    count = new_list.count(new_string)

    if count == 0:
        raise ValueError(f'The target string "{target_string}" does not appear in the list.')
    else:
        return new_list


action_type =   {
                    "shape=parallelogram;html=1;strokeWidth=2;perimeter=parallelogramPerimeter;whiteSpace=wrap;rounded=1;arcSize=12;size=0.23;" : "input",
                    "rounded=1;whiteSpace=wrap;html=1;fontSize=12;glass=0;strokeWidth=1;shadow=0;" : "process",
                    "rhombus;whiteSpace=wrap;html=1;shadow=0;fontFamily=Helvetica;fontSize=12;align=center;strokeWidth=1;spacing=6;spacingTop=-4;" : "decision",
                    "shape=tape;whiteSpace=wrap;html=1;strokeWidth=2;size=0.19" : "print"
                }

def handle_node(node,function_lines):

    try:
        action = action_type[node.get('style')]

        if action == "input":
            var = str(list(node.get('value').split(" "))[1])
            command = get_input_code(var)
            function_lines.append(command)
        elif action == "decision" :
            print("came here")
            lst = list(node.get("value").split(" "))
            print(lst)
            newlst = replace_target_string(lst,"&gt;","<")
            print(newlst)
            command = ' '.join(newlst)
            function_lines.append(command)
        elif action == "process":
            function_lines.append(node.get("value"))
        elif action == "print":
            command = print_variable_to_terminal(str(node.get("value")))
            function_lines.append(command)
    except:
        print("Not a node")


tree = ET.parse('version1.xml')
root = tree.getroot()

function_data = []

for node in root.iter('mxCell'):

    handle_node(node,function_data)

def save_python_commands_to_file(commands, file_name):
    # open the file for writing
    with open(file_name, 'w') as f:
        # write each command in the list to the file
        for command in commands:
            f.write(command + '\n')
    
    print(f'Saved {len(commands)} lines of Python code to file {file_name}')

save_python_commands_to_file(function_data, 'result.py')


