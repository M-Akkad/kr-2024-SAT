from typing import List, Dict, Optional, Tuple
import time


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
                    # p cnf <num_vars> <num_clauses>
                    parts = line.split()
                    self.num_vars = int(parts[2])
                    self.num_clauses = int(parts[3])
                else:
                    # Read clause: list of integers ending with 0
                    clause = [int(x) for x in line.split()]
                    if clause[-1] == 0:
                        clause.pop()  # Remove trailing 0
                        self.clauses.append(clause)

    def write_solution(self, filename: str) -> None:
        """Write solution in DIMACS format."""
        with open(filename + '.out', 'w') as f:
            if self.assignment:
                # Write assignment for each variable
                for var in range(1, self.num_vars + 1):
                    value = self.assignment.get(var, True)  # Default to True if unassigned
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

            # Simplify clauses
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
                        return None, None  # Conflict detected
                    new_clauses.append(unassigned)

            clauses = new_clauses

        return clauses, assignment

    def dpll(self, clauses: List[List[int]], assignment: Dict[int, bool]) -> bool:
        """DPLL algorithm implementation."""
        # Unit propagation
        clauses, assignment = self.unit_propagation(clauses, assignment)
        if clauses is None:
            return False

        # Check if all clauses are satisfied
        if not clauses:
            self.assignment = assignment
            return True

        # Choose a variable
        for clause in clauses:
            for lit in clause:
                var = abs(lit)
                if var not in assignment:
                    # Try assigning True
                    new_assignment = assignment.copy()
                    new_assignment[var] = True
                    if self.dpll(clauses, new_assignment):
                        return True

                    # Try assigning False
                    new_assignment = assignment.copy()
                    new_assignment[var] = False
                    if self.dpll(clauses, new_assignment):
                        return True

                    return False

        return False

    def solve(self) -> bool:
        """Solve the SAT problem."""
        return self.dpll(self.clauses, {})

    def print_sudoku_solution(self):
        """Print Sudoku solution in a readable format."""
        if not self.assignment:
            print("No solution found!")
            return

        # Create 9x9 grid
        grid = [[0 for _ in range(9)] for _ in range(9)]

        # Fill in the grid based on the assignment
        for var in range(1, self.num_vars + 1):
            if self.assignment.get(var, False):
                # Convert variable number to row, col, value
                var_str = str(var)
                if len(var_str) == 3:  # Only process valid cell assignments
                    row = int(var_str[0]) - 1
                    col = int(var_str[1]) - 1
                    val = int(var_str[2])
                    if 0 <= row < 9 and 0 <= col < 9:
                        grid[row][col] = val

        # Print the grid
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


def print_sudoku_solution(self):
    """Print Sudoku solution in a readable format."""
    if not self.assignment:
        print("No solution found!")
        return

    # Create 9x9 grid
    grid = [[0 for _ in range(9)] for _ in range(9)]

    # Fill in the grid based on the assignment
    for var in range(1, self.num_vars + 1):
        if self.assignment.get(var, False):
            # Convert variable number to row, col, value
            var_str = str(var)
            if len(var_str) == 3:  # Only process valid cell assignments
                row = int(var_str[0]) - 1
                col = int(var_str[1]) - 1
                val = int(var_str[2])
                if 0 <= row < 9 and 0 <= col < 9:
                    grid[row][col] = val

    # Print the grid
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


def main():
    # Create solver instance
    solver = SATSolver()

    # Specify input file
    input_file = "cnf_files/sudoku5.cnf"

    try:
        # Start timing for file reading
        read_start_time = time.time()
        print(f"Reading DIMACS file: {input_file}")
        solver.read_dimacs(input_file)
        read_time = time.time() - read_start_time
        print(f"File reading time: {read_time:.3f} seconds")
        print(f"Number of variables: {solver.num_vars}")
        print(f"Number of clauses: {solver.num_clauses}")

        # Start timing for solving
        solve_start_time = time.time()
        print("\nSolving...")
        if solver.solve():
            solve_time = time.time() - solve_start_time
            print(f"Solution found in {solve_time:.3f} seconds!")

            # Start timing for writing solution
            write_start_time = time.time()
            solver.write_solution(input_file)
            write_time = time.time() - write_start_time
            print(f"Solution written to {input_file}.out in {write_time:.3f} seconds")

            # Calculate total time
            total_time = read_time + solve_time + write_time
            print(f"\nTotal execution time: {total_time:.3f} seconds")

            # Print the Sudoku solution
            solver.print_sudoku_solution()
        else:
            solve_time = time.time() - solve_start_time
            print(f"No solution exists! (Solved in {solve_time:.3f} seconds)")
            with open(input_file + '.out', 'w') as f:
                pass

    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
