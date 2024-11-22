import os

def parse_puzzle_line(puzzle_line):
    """
    Parse a single Sudoku puzzle from a string of 81 characters.
    Returns: A list of unit clauses representing the givens.
    """
    clauses = []
    if len(puzzle_line) != 81:
        raise ValueError("Invalid puzzle format. Expected 81 characters.")
    for idx, char in enumerate(puzzle_line):
        if char != '.' and char != '0':
            row = idx // 9 + 1
            col = idx % 9 + 1
            val = int(char)
            # Encode the variable number
            var = row * 100 + col * 10 + val
            clauses.append([var])
    return clauses

def write_puzzle_dimacs(clauses, puzzle_index, output_dir):
    """
    Write the clauses to a DIMACS CNF file for a single puzzle.
    """
    num_clauses = len(clauses)
    num_vars = 999  # Variables range from 111 to 999

    filename = os.path.join(output_dir, f"puzzleHard_{puzzle_index + 1}.cnf")
    with open(filename, 'w') as f:
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            clause_str = ' '.join(map(str, clause)) + " 0\n"
            f.write(clause_str)
    print(f"Puzzle {puzzle_index + 1} written to {filename}")

def convert_puzzles_to_dimacs(puzzles_file, output_dir):
    """
    Convert all puzzles in the given file to DIMACS CNF format.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(puzzles_file, 'r') as f:
        puzzles = f.readlines()

    for idx, puzzle_line in enumerate(puzzles):
        puzzle_line = puzzle_line.strip()
        if puzzle_line:
            try:
                clauses = parse_puzzle_line(puzzle_line)
                write_puzzle_dimacs(clauses, idx, output_dir)
            except ValueError as e:
                print(f"Error in puzzle {idx + 1}: {e}")

def main():
    puzzles_file = 'C:/Users/Latitude 7320/Desktop/KR_SAT2/kr-2024-SAT-main/puzzles/damnhard.sdk.txt'
    output_dir = 'puzzles'

    convert_puzzles_to_dimacs(puzzles_file, output_dir)

if __name__ == "__main__":
    main()
