import xml.etree.ElementTree as ET

def get_input_code(variable_name):
    return f'{variable_name} = int(input("Enter a value for {variable_name}: "))'

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
                    "strokeWidth=2;html=1;shape=mxgraph.flowchart.start_1;whiteSpace=wrap;" : "start",
                    "strokeWidth=2;html=1;shape=mxgraph.flowchart.stored_data;whiteSpace=wrap;" : "input",
                    "rounded=1;whiteSpace=wrap;html=1;absoluteArcSize=1;arcSize=14;strokeWidth=2;" : "process",
                    "strokeWidth=2;html=1;shape=mxgraph.flowchart.decision;whiteSpace=wrap;" : "decision",
                    "strokeWidth=2;html=1;shape=mxgraph.flowchart.display;whiteSpace=wrap;" : "print",
                    "strokeWidth=2;html=1;shape=mxgraph.flowchart.terminator;whiteSpace=wrap;" : "end"
                }

def handle_node(node,function_lines):

    try:
        action = action_type[node.get('style')]

        if action == "input":
            var = str(list(node.get('value').split(" "))[1])
            command = get_input_code(var)
            function_lines.append(command)
        elif action == "decision" :
            lst = list(node.get("value").split(" "))
            newlst = replace_target_string(lst,"&gt;",">")
            condition = ['if'] + newlst + [':']
            command = ' '.join(condition)
            function_lines.append(command)
        elif action == "process":
            function_lines.append(node.get("value"))
        elif action == "print":
            toPrint = (list(node.get("value").split(":"))[1]).strip()
            command = print_variable_to_terminal(str(toPrint))
            function_lines.append(command)
        elif action == "start":
            function_lines.append("# Start of the program")
        elif action == "end":
            function_lines.append("# End of the program")
    except:
        print("Not a node")

def handle_next_node(start_node,root,commands):

    current_node = start_node
    edge_condition = ".//mxCell[@source='" + str(current_node.get("id")) + "']"

    out_edges = root.findall(".//mxCell[@edge='1']" and edge_condition) 

    edge_count = len(out_edges)

    while (edge_count>0):

        vertex_condition = ".//mxCell[@id='" + str(out_edges[0].get("target")) + "']" 
        edge_condition = ".//mxCell[@source='" + str(out_edges[0].get("target")) + "']"

        current_node = root.findall(vertex_condition)

        handle_node(current_node[0],commands)

        out_edges = root.findall(".//mxCell[@edge='1']" and edge_condition) 

        edge_count = len(out_edges)

def save_python_commands_to_file(commands, file_name):
    # open the file for writing
    with open(file_name, 'w') as f:
        # write each command in the list to the file
        for command in commands:
            f.write(command + '\n')
    
    print(f'Saved {len(commands)} lines of Python code to file {file_name}')


tree = ET.parse('sequential.xml')
root = tree.getroot()

function_data = []

start_cell = root.findall(".//mxCell[@style='strokeWidth=2;html=1;shape=mxgraph.flowchart.start_1;whiteSpace=wrap;']") 

function_data.append("# Start of the program")

handle_next_node(start_cell[0],root,function_data)

save_python_commands_to_file(function_data, 'result.py')


