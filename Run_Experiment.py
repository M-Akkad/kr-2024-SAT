import os
import subprocess
import csv
import time
import sys

def run_experiment(strategy, puzzle_file):
    python_executable = sys.executable

    # Map strategies to Python scripts
    strategy_scripts = {
        1: 'app.py',
        2: 'mom_heuristic.py',
        3: 'jeroslow_wang_heuristic.py'
    }

    script = strategy_scripts.get(strategy)
    if not script:
        print(f"Error: Invalid strategy {strategy}")
        return {
            'strategy': strategy,
            'puzzle_file': puzzle_file,
            'runtime': None,
            'backtracks': None,
            'max_depth': None,
            'recursive_calls': None
        }

    command = [python_executable, script, f"-S{strategy}", puzzle_file]
    start_time = time.time()
    result = subprocess.run(command, capture_output=True, text=True)
    end_time = time.time()
    runtime = end_time - start_time

    # Check if the subprocess ran successfully
    if result.returncode != 0:
        print(f"Error running solver: {result.stderr}")
        return {
            'strategy': strategy,
            'puzzle_file': puzzle_file,
            'runtime': runtime,
            'backtracks': None,
            'max_depth': None,
            'recursive_calls': None
        }

    # Parse output to get metrics
    output = result.stdout
    backtracks = extract_metric(output, 'Number of backtracks')
    max_depth = extract_metric(output, 'Maximum recursion depth')
    recursive_calls = extract_metric(output, 'Total recursive calls')

    return {
        'strategy': strategy,
        'puzzle_file': puzzle_file,
        'runtime': runtime,
        'backtracks': backtracks,
        'max_depth': max_depth,
        'recursive_calls': recursive_calls
    }

def extract_metric(output, metric_name):
    for line in output.split('\n'):
        if line.startswith(metric_name):
            return int(line.split(':')[1].strip())
    return None

def main():
    puzzles_dir = 'puzzles'  # Adjust if necessary
    strategies = [1, 2, 3]
    results = []

    puzzle_files = [os.path.join(puzzles_dir, f) for f in os.listdir(puzzles_dir) if f.endswith('.cnf')]

    for puzzle_file in puzzle_files:
        for strategy in strategies:
            print(f"Running strategy {strategy} on puzzle {puzzle_file}")
            result = run_experiment(strategy, puzzle_file)
            results.append(result)

    # Write results to CSV
    with open('experiment_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['strategy', 'puzzle_file', 'runtime', 'backtracks', 'max_depth', 'recursive_calls']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

if __name__ == '__main__':
    main()
