import sys
sys.setrecursionlimit(2000)  # Increase recursion limit

class SATSolver:
    def __init__(self, filename):
        self.clauses = []
        self.num_vars = 0
        self.load_dimacs(filename)

    def load_dimacs(self, filename):
        """Loads DIMACS format input"""
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('p'):
                    _, _, num_vars, _ = line.split()
                    self.num_vars = int(num_vars)
                elif not line.startswith('c') and line.strip():
                    self.clauses.append([int(x) for x in line.strip().split() if x != '0'])

    def is_satisfiable(self):
        """Starts the DPLL algorithm"""
        assignment = {}
        return self.dpll(self.clauses, assignment)

    def dpll(self, clauses, assignment):
        """DPLL Algorithm with Unit Propagation and Pure Literal Elimination"""
        clauses, assignment = self.unit_propagation(clauses, assignment)

        if all(any(lit in assignment and assignment[lit] for lit in clause) for clause in clauses):
            return assignment

        if any(all(lit in assignment and not assignment[lit] for lit in clause) for clause in clauses):
            return False

        unassigned = {abs(lit) for clause in clauses for lit in clause if lit not in assignment}
        if not unassigned:
            return False

        lit = next(iter(unassigned))
        for value in [True, False]:
            assignment[lit] = value
            result = self.dpll(clauses, assignment)
            if result:
                return result
            del assignment[lit]
        return False

    def unit_propagation(self, clauses, assignment):
        """Perform unit propagation"""
        while True:
            unit_clauses = [clause for clause in clauses if len(clause) == 1]
            if not unit_clauses:
                break
            for clause in unit_clauses:
                lit = clause[0]
                if abs(lit) in assignment and assignment[abs(lit)] != (lit > 0):
                    return clauses, False
                assignment[abs(lit)] = lit > 0
                clauses = [c for c in clauses if lit not in c]
                for c in clauses:
                    if -lit in c:
                        c.remove(-lit)
        return clauses, assignment

    def solve(self):
        """Solve the SAT problem and return the assignments"""
        result = self.is_satisfiable()
        if result:
            return {lit: val for lit, val in result.items() if val}
        return None


def combine_dimacs(rule_file, puzzle_file, output_file):
    """Combines the Sudoku rules and puzzle into a single DIMACS file"""
    with open(output_file, 'w') as out, open(rule_file, 'r') as rules, open(puzzle_file, 'r') as puzzle:
        for line in rules:
            out.write(line)
        for line in puzzle:
            if not line.startswith('p') and not line.startswith('c'):
                out.write(line)


def solve_sudoku(rule_file, puzzle_file):
    """Combines the rule file and puzzle, solves it, and prints the solution."""
    combined_file = "combined.cnf"
    combine_dimacs(rule_file, puzzle_file, combined_file)

    solver = SATSolver(combined_file)
    solution = solver.solve()

    if not solution:
        print("No solution found. Check your puzzle or encoding logic.")
        return

    print("Decoded Sudoku Grid:")
    sudoku_grid = decode_solution(solution)

    if validate_sudoku(sudoku_grid):
        print("Solved Sudoku:")
        for row in sudoku_grid:
            print(" ".join(map(str, row)))
    else:
        print("The solution is invalid. Check your rules and encoding.")


def decode_solution(solution, n=9):
    sudoku_grid = [[0 for _ in range(n)] for _ in range(n)]

    for variable, value in solution.items():
        if value:  # Only consider True variables
            abs_variable = abs(variable)
            row = (abs_variable // 100) - 1
            col = ((abs_variable % 100) // 10) - 1
            num = abs_variable % 10
            sudoku_grid[row][col] = num

    return sudoku_grid


def validate_sudoku(grid):
    """Validates the Sudoku solution."""
    n = len(grid)
    subgrid_size = int(n**0.5)

    def is_valid_group(numbers):
        """Check if numbers contain all digits from 1 to n exactly once."""
        return sorted(numbers) == list(range(1, n + 1))

    # Check rows
    for row in grid:
        if not is_valid_group(row):
            return False

    # Check columns
    for col in range(n):
        if not is_valid_group([grid[row][col] for row in range(n)]):
            return False

    # Check subgrids
    for box_row in range(0, n, subgrid_size):
        for box_col in range(0, n, subgrid_size):
            subgrid = [
                grid[r][c]
                for r in range(box_row, box_row + subgrid_size)
                for c in range(box_col, box_col + subgrid_size)
            ]
            if not is_valid_group(subgrid):
                return False

    return True


if __name__ == "__main__":
    sudoku_rules = "sudoku-rules-9x9.txt"
    sudoku_puzzle = "sudoku1.cnf"

    solve_sudoku(sudoku_rules, sudoku_puzzle)
