import time
from typing import List, Dict, Optional, Tuple
import sys



class SATSolver:
    def __init__(self):
        self.num_vars: int = 0
        self.num_clauses: int = 0
        self.clauses: List[List[int]] = []
        self.assignment: Dict[int, bool] = {}

    def read_dimacs(self, filename: str) -> None:
        """Read DIMACS format file."""
        self.clauses = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('c'):
                    continue
                if line.startswith('p'):
                    parts = line.split()
                    self.num_vars = int(parts[2])
                    self.num_clauses = int(parts[3])
                else:
                    clause = [int(x) for x in line.split()]
                    if clause[-1] == 0:
                        clause.pop()
                        self.clauses.append(clause)

    def write_solution(self, filename: str) -> None:
        """Write solution in DIMACS format."""
        with open(filename + '.out', 'w') as f:
            if self.assignment:
                for var in range(1, self.num_vars + 1):
                    value = self.assignment.get(var, True)
                    f.write(f"{var if value else -var} 0\n")

    def unit_propagation(self, clauses: List[List[int]], assignment: Dict[int, bool]) -> Tuple[
        Optional[List[List[int]]], Optional[Dict[int, bool]]]:
        """Perform unit propagation on clauses."""
        while True:
            unit_clause = None
            for clause in clauses:
                unassigned = []
                is_satisfied = False

                for lit in clause:
                    var = abs(lit)
                    if var in assignment:
                        if (lit > 0) == assignment[var]:
                            is_satisfied = True
                            break
                    else:
                        unassigned.append(lit)

                if not is_satisfied and len(unassigned) == 1:
                    unit_clause = unassigned[0]
                    break

            if unit_clause is None:
                break

            var = abs(unit_clause)
            assignment[var] = unit_clause > 0

            new_clauses = []
            for clause in clauses:
                unassigned = []
                is_satisfied = False

                for lit in clause:
                    var = abs(lit)
                    if var in assignment:
                        if (lit > 0) == assignment[var]:
                            is_satisfied = True
                            break
                    else:
                        unassigned.append(lit)

                if not is_satisfied:
                    if not unassigned:
                        return None, None
                    new_clauses.append(unassigned)

            clauses = new_clauses

        return clauses, assignment

    def calculate_jw_score(self, clauses: List[List[int]], var: int) -> float:
        """Calculate Two-Sided Jeroslow-Wang score for a variable."""
        pos_score = 0.0
        neg_score = 0.0

        for clause in clauses:
            clause_length = len(clause)
            for lit in clause:
                if abs(lit) == var:
                    # Use 2^(-length) as the weight
                    weight = 2.0 ** (-clause_length)
                    if lit > 0:
                        pos_score += weight
                    else:
                        neg_score += weight

        # Return the maximum of positive and negative scores
        return max(pos_score, neg_score)

    def choose_variable_jw(self, clauses: List[List[int]], assignment: Dict[int, bool]) -> Optional[int]:
        """Choose next variable using Two-Sided Jeroslow-Wang heuristic."""
        best_var = None
        best_score = -1.0

        # Calculate scores for all unassigned variables
        for clause in clauses:
            for lit in clause:
                var = abs(lit)
                if var not in assignment:
                    score = self.calculate_jw_score(clauses, var)
                    if score > best_score:
                        best_score = score
                        best_var = var

        return best_var

    def dpll(self, clauses: List[List[int]], assignment: Dict[int, bool]) -> bool:
        """DPLL algorithm implementation with JW heuristic."""
        clauses, assignment = self.unit_propagation(clauses, assignment)
        if clauses is None:
            return False

        if not clauses:
            self.assignment = assignment
            return True

        # Use JW heuristic to choose the next variable
        var = self.choose_variable_jw(clauses, assignment)
        if var is None:
            return False

        # Try the value that had the higher score first
        pos_score = self.calculate_jw_score(clauses, var)
        neg_score = self.calculate_jw_score(clauses, -var)

        # Try the phase with higher score first
        values_to_try = [pos_score >= neg_score, pos_score < neg_score]

        for value in values_to_try:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.dpll(clauses, new_assignment):
                return True

        return False

    def solve(self) -> bool:
        """Solve the SAT problem."""
        return self.dpll(self.clauses, {})

    def print_sudoku_solution(self):
        """Print Sudoku solution in a readable format."""
        if not self.assignment:
            print("No solution found!")
            return

        grid = [[0 for _ in range(9)] for _ in range(9)]

        for var in range(1, self.num_vars + 1):
            if self.assignment.get(var, False):
                var_str = str(var)
                if len(var_str) == 3:
                    row = int(var_str[0]) - 1
                    col = int(var_str[1]) - 1
                    val = int(var_str[2])
                    if 0 <= row < 9 and 0 <= col < 9:
                        grid[row][col] = val

        print("\nSudoku Solution:")
        print("  " + "-" * 25)
        for i in range(9):
            print("| ", end="")
            for j in range(9):
                print(f"{grid[i][j]} ", end="")
                if (j + 1) % 3 == 0:
                    print("| ", end="")
            print()
            if (i + 1) % 3 == 0:
                print("  " + "-" * 25)


def combine_dimacs_files(rules_file: str, puzzle_file: str) -> Tuple[List[List[int]], int]:
    """
    Combine rules and puzzle into one set of clauses and determine max variable number.
    Returns: (clauses, max_var_number)
    """
    clauses = []
    max_var = 0

    # Read rules file
    with open(rules_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('c') or line.startswith('p'):
                continue
            clause = [int(x) for x in line.split()]
            if clause[-1] == 0:
                clause.pop()
                clauses.append(clause)
                # Update max_var
                max_var = max(max_var, max(abs(lit) for lit in clause))

    # Read puzzle file
    with open(puzzle_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('c') or line.startswith('p'):
                continue
            clause = [int(x) for x in line.split()]
            if clause[-1] == 0:
                clause.pop()
                clauses.append(clause)
                # Update max_var
                max_var = max(max_var, max(abs(lit) for lit in clause))

    return clauses, max_var


def main():
    if len(sys.argv) != 3:
        print("Usage: SAT -S3 <puzzle_file>")
        sys.exit(1)

    strategy = sys.argv[1]
    puzzle_file = sys.argv[2]

    if strategy != "-S3":
        print(f"Error: Unsupported strategy {strategy}. This script only supports -S3.")
        sys.exit(1)

    solver = SATSolver()
    rules_file = "rules/sudoku-rules-9x9.txt"

    try:
        print(f"Reading rules from: {rules_file}")
        print(f"Reading puzzle from: {puzzle_file}")

        start_time = time.time()
        # Get clauses and maximum variable number
        solver.clauses, solver.num_vars = combine_dimacs_files(rules_file, puzzle_file)
        solver.num_clauses = len(solver.clauses)

        read_time = time.time() - start_time
        print(f"Files read in {read_time:.3f} seconds")
        print(f"Number of variables: {solver.num_vars}")
        print(f"Number of clauses: {solver.num_clauses}")

        print("\nSolving using Two-Sided Jeroslow-Wang heuristic...")
        solve_start_time = time.time()
        if solver.solve():
            solve_time = time.time() - solve_start_time
            print(f"Solution found in {solve_time:.3f} seconds!")

            write_start_time = time.time()
            solver.write_solution(puzzle_file)
            write_time = time.time() - write_start_time
            print(f"Solution written to {puzzle_file}.out in {write_time:.3f} seconds")

            solver.print_sudoku_solution()

            total_time = read_time + solve_time + write_time
            print(f"\nTotal execution time: {total_time:.3f} seconds")
        else:
            solve_time = time.time() - solve_start_time
            print(f"No solution exists! (Solved in {solve_time:.3f} seconds)")
            with open(puzzle_file + '.out', 'w') as f:
                pass

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
