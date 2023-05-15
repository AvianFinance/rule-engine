def function1():
    print("Executing Function 1")

def function2():
    print("Executing Function 2")

def function3():
    print("Executing Function 3")

def function4():
    print("Executing Function 4")

def function5():
    print("Executing Function 5")

# Map user input to functions
function_map = {
    "1": function1,
    "2": function2,
    "3": function3,
    "4": function4,
    "5": function5
}

# Prompt user for input
user_input = input("Enter a number (1-5): ")

# Execute the corresponding function based on user input
if user_input in function_map:
    selected_function = function_map[user_input]
    selected_function()
else:
    print("Invalid input. Please enter a number between 1 and 5.")
