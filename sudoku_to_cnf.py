import os

def read_sudoku_rules(rules_file):
    """Read the 9x9 Sudoku rules from the specified file."""
    with open(rules_file, 'r') as f:
        # Exclude any line starting with "p cnf"
        return [line.strip() for line in f if not line.startswith("p")]

def sudoku_to_cnf(puzzle, rules, output_file):
    """
    Convert a Sudoku puzzle to CNF format by combining it with the rules.
    Arguments:
    - puzzle: A string of 81 characters representing the Sudoku puzzle.
    - rules: The rules as a list of clauses.
    - output_file: File path to write the output CNF.
    """
    clauses = rules[:]
    num_clauses = len(clauses)

    # Translate the puzzle into CNF format
    for i, char in enumerate(puzzle):
        if char.isdigit():
            row = i // 9 + 1
            col = i % 9 + 1
            value = int(char)
            # Add a clause for the fixed value in the puzzle
            clauses.append(f"{row}{col}{value} 0")
            num_clauses += 1

    # Write to output file
    with open(output_file, 'w') as f:
        f.write(f"p cnf 999 {num_clauses}\n")  # Write the correct header
        f.write("\n".join(clauses) + "\n")     # Write all clauses

def process_sudoku_file(input_file, rules_file, output_dir):
    """
    Process a Sudoku file and convert each puzzle into its corresponding CNF file.
    Arguments:
    - input_file: Path to the Sudoku puzzles file.
    - rules_file: Path to the Sudoku rules file.
    - output_dir: Directory to store generated CNF files.
    """
    # Read rules
    rules = read_sudoku_rules(rules_file)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each puzzle
    base_name = os.path.splitext(os.path.basename(input_file))[0]  # Strip extension
    with open(input_file, 'r') as f:
        for idx, line in enumerate(f):
            puzzle = line.strip()
            if len(puzzle) != 81:
                print(f"Skipping invalid puzzle at line {idx + 1} in {input_file}")
                continue
            output_file = os.path.join(output_dir, f"{base_name}_{idx + 1}.cnf")
            sudoku_to_cnf(puzzle, rules, output_file)
            print(f"Generated CNF for puzzle {idx + 1}: {output_file}")

if __name__ == "__main__":
    # Inputs
    sudoku_files = [
        "puzzles/top95.sdk.txt",
        "puzzles/top91.sdk.txt",
        "puzzles/top870.sdk.txt",
        "puzzles/top2365.sdk.txt",
        "puzzles/top100.sdk.txt",
        "puzzles/damnhard.sdk.txt",
        "puzzles/1000sudokus.txt"
    ]
    rules_file = "rules/sudoku-rules-9x9.txt"
    output_dir = "puzzles"

    # Convert all Sudoku files
    for sudoku_file in sudoku_files:
        print(f"Processing file: {sudoku_file}")
        process_sudoku_file(sudoku_file, rules_file, output_dir)
