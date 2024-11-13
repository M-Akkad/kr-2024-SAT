def encode_sudoku_puzzle(puzzle_file, grid_size):
    """
    Encodes a Sudoku puzzle into DIMACS CNF clauses.
    """
    clauses = []
    with open(puzzle_file, 'r') as file:
        puzzle = [line.strip() for line in file if line.strip()]

    # Validate dimensions
    if len(puzzle) != grid_size:
        raise ValueError(f"Puzzle file has {len(puzzle)} rows, expected {grid_size}.")
    for idx, row in enumerate(puzzle):
        if len(row) != grid_size:
            raise ValueError(f"Row {idx + 1} has {len(row)} characters, expected {grid_size}.")

    # Encode puzzle constraints
    for row in range(grid_size):
        for col in range(grid_size):
            cell = puzzle[row][col]
            if cell != '.':
                var = (row * grid_size ** 2 + col * grid_size + int(cell))
                clauses.append([var])  # Unit clause for fixed value

    print(f"Encoded {len(clauses)} puzzle clauses.")
    return clauses




def output_solution(solution, grid_size=9):
    """
    Converts a SAT solution to a readable 9x9 Sudoku grid.
    """
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    for var in solution:
        if var > 0:
            var -= 1
            row = var // (grid_size ** 2)
            col = (var % (grid_size ** 2)) // grid_size
            num = (var % grid_size) + 1
            if 0 <= row < grid_size and 0 <= col < grid_size:
                grid[row][col] = str(num)
    print("Generated Sudoku Grid:")
    for row in grid:
        print(' '.join(row))
    return grid
