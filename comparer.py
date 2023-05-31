def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

        total_lines = min(len(lines1), len(lines2))
        matched_lines = sum(1 for line1, line2 in zip(lines1, lines2) if line1.strip() == line2.strip() and line1.strip())

        score = matched_lines / total_lines
        return score


# Example usage
file1_path = 'contracts/main/sell_logic.txt'  # Path to the first text file
file2_path = 'contracts/new/sell_logic.txt'  # Path to the second text file

score = compare_files(file1_path, file2_path)
print(f"Matching score: {score}")
