# sat_solver.py

def parse_dimacs(file_path):
    """
    Parses a DIMACS CNF file and returns the clauses as a list of lists.
    Processes the entire file without limiting the number of clauses.
    """
    clauses = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('c') or line.startswith('p'):
                continue  # Skip comments and problem definition
            clause = list(map(int, line.strip().split()))[:-1]  # Remove trailing 0
            clauses.append(clause)

    # Debugging: Print total rules loaded
    print(f"Parsed {len(clauses)} clauses from {file_path}")
    return clauses




def unit_propagate(clauses, assignment):
    updated_clauses = []
    for clause in clauses:
        if any(lit in assignment for lit in clause):
            continue
        new_clause = [lit for lit in clause if -lit not in assignment]
        if not new_clause:  # Conflict detected
            print(f"Conflict detected: {clause}")
            return None, True
        if len(new_clause) == 1:  # Unit clause
            print(f"Unit propagation: {new_clause[0]}")
            assignment.append(new_clause[0])
            continue
        updated_clauses.append(new_clause)
    return updated_clauses, False


def dpll(clauses, assignment):
    """
    DPLL algorithm with proper constraint propagation.
    """
    # Perform unit propagation
    clauses, conflict = unit_propagate(clauses, assignment)
    if conflict:
        return None

    # Check if all clauses are satisfied
    if not clauses:
        return assignment

    # Select an unassigned variable
    unassigned = set(abs(lit) for clause in clauses for lit in clause) - set(abs(lit) for lit in assignment)
    if not unassigned:
        return assignment

    var = unassigned.pop()

    # Try assigning true
    result = dpll(clauses + [[var]], assignment + [var])
    if result is not None:
        return result

    # Try assigning false
    return dpll(clauses + [[-var]], assignment + [-var])

