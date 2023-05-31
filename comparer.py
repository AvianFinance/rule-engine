def compare_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        for line_num, (line1, line2) in enumerate(zip(file1, file2), start=1):
            if line1.strip() != line2.strip():
                return f"Files are not similar. Difference found in line {line_num}"
    
    return "Looks great! Files are similar."

file1_path = 'contracts/main/sell_logic.txt'
file2_path = 'contracts/new/sell_logic.txt'

result = compare_files(file1_path, file2_path)
print(result)

