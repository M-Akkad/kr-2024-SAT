from sat_solver import parse_dimacs, dpll
from sudoku_encoder import encode_sudoku_puzzle, output_solution


def solve_sudoku(rule_file, puzzle_file, output_file, grid_size=9):
    """
    Solves a 9x9 Sudoku puzzle using SAT.
    """
    # Parse rules
    rules = parse_dimacs(rule_file)

    # Debugging rules for completeness
    debug_rules(rules, grid_size)

    # Encode the puzzle
    puzzle_clauses = encode_sudoku_puzzle(puzzle_file, grid_size)

    # Combine rules and puzzle clauses
    clauses = rules + puzzle_clauses

    print(f"Total combined clauses: {len(clauses)}")

    # Solve using DPLL
    solution = dpll(clauses, [])

    if solution is None:
        with open(output_file, 'w') as file:
            file.write('')  # Write empty file for no solution
        print("No solution exists.")
    else:
        # Convert SAT solution to Sudoku grid
        grid = output_solution(solution, grid_size)

        # Validate the Sudoku grid
        if validate_sudoku(grid):
            print("Solution is valid.")
            with open(output_file, 'w') as file:
                for row in grid:
                    file.write(' '.join(row) + '\n')
            print(f"Solution written to {output_file}:")
            for row in grid:
                print(' '.join(row))
        else:
            print("Solution is invalid!")


def validate_sudoku(grid):
    """
    Validates a Sudoku grid for row, column, and 3x3 subgrid constraints.
    """
    size = len(grid)
    subgrid_size = int(size ** 0.5)

    # Check rows and columns
    for i in range(size):
        row = [val for val in grid[i] if val != '.']
        col = [grid[j][i] for j in range(size) if grid[j][i] != '.']
        if len(row) != len(set(row)) or len(col) != len(set(col)):
            print(f"Validation failed for row {i} or column {i}")
            return False

    # Check subgrids
    for r in range(0, size, subgrid_size):
        for c in range(0, size, subgrid_size):
            subgrid = []
            for dr in range(subgrid_size):
                for dc in range(subgrid_size):
                    val = grid[r + dr][c + dc]
                    if val != '.':
                        subgrid.append(val)
            if len(subgrid) != len(set(subgrid)):
                print(f"Validation failed for subgrid starting at ({r}, {c})")
                return False

    return True


def extract_9x9_puzzles(input_file, output_prefix):
    """
    Extracts all 9x9 puzzles from a stacked input file where each puzzle is written as a single line.
    """
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]

    puzzles = []
    for line in lines:
        if len(line) == 81:  # A single-line puzzle with 81 characters
            puzzle = [line[i:i+9] for i in range(0, 81, 9)]  # Split into 9 rows
            puzzles.append(puzzle)

    for idx, puzzle in enumerate(puzzles):
        output_file = f"{output_prefix}_{idx + 1}.txt"
        with open(output_file, 'w') as file:
            for row in puzzle:
                file.write(row + '\n')
        print(f"Extracted puzzle {idx + 1} to {output_file}")

    return len(puzzles)



def process_and_solve_puzzles(input_file, rule_file, solution_prefix):
    """
    Extracts 9x9 puzzles, solves each one, and writes solutions to separate files.
    """
    print("Extracting puzzles...")
    num_puzzles = extract_9x9_puzzles(input_file, "temp_puzzle")

    for idx in range(1, num_puzzles + 1):
        puzzle_file = f"temp_puzzle_{idx}.txt"
        solution_file = f"{solution_prefix}_{idx}.out"
        print(f"Solving puzzle {idx}...")
        solve_sudoku(rule_file, puzzle_file, solution_file, grid_size=9)



def debug_rules(rules, grid_size):
    """
    Debugs the rules for completeness and correctness.
    """
    print("Debugging Sudoku Rules...")

    # Cell constraints
    for row in range(1, grid_size + 1):
        for col in range(1, grid_size + 1):
            variable_base = (row - 1) * grid_size ** 2 + (col - 1) * grid_size
            cell_has_rule = any(
                variable_base + num in clause
                for clause in rules
                for num in range(1, grid_size + 1)
            )
            if not cell_has_rule:
                print(f"Missing rule for cell ({row},{col}) to contain at least one number.")

    print("Rule debugging completed.")



if __name__ == "__main__":
    process_and_solve_puzzles(
        input_file="top91.sdk.txt",
        rule_file="sudoku-rules-9x9.txt",
        solution_prefix="solution_9x9"
    )
