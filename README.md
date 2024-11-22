# SAT Solver Setup Guide

## Overview

This repository contains a SAT (Boolean Satisfiability) solver and a setup script to make it easily accessible on your system. The setup script handles executable permissions and optionally adds the solver to your system PATH.

## Requirements

- A Unix-like operating system (Linux, macOS) or Windows using Git Bash.
- Bash shell
- Write permissions in the installation directory

## Installation

1. Clone or download this repository to your local machine
2. Navigate to the repository directory
3. Run the setup script:
   ```bash
   ./install_sat.sh
   ```

The setup script will:

- Verify the SAT solver executable exists
- Set the proper executable permissions
- Optionally add the solver to your system PATH

## Usage

### Basic Usage

After running the setup script, you can execute the SAT solver using:

```bash
./SAT -S[1|2|3] <puzzle_file>
```

The solver supports three different solving strategies (1, 2, or 3).

### Global Access

If you chose to add the solver to your PATH during setup, you can run it from any directory using:

```bash
SAT -S[1|2|3] <puzzle_file>
```

### PATH Configuration

If you added the solver to your PATH, you'll need to either:

- Restart your terminal
- Or reload your shell configuration:

  ```bash
  # For bash users
  source ~/.bashrc

  # For zsh users
  source ~/.zshrc
  ```
  
### Example Commands
- Run using strategy 1 on `sudoku1.cnf`:
  ```bash
  ./SAT -S1 sudoku1.cnf
  ```

- Globally, if added to PATH:
  ```bash
  SAT -S2 sudoku1.cnf
  ```

---

## Troubleshooting

### Common Issues

#### 1. "SAT: Command not found"
- Ensure you’re in the correct directory or use `./SAT` instead of `SAT`.
- If you added the solver to your PATH, ensure it’s correctly configured.

#### 2. "Syntax error near unexpected token"
- Confirm the command syntax:
  ```bash
  ./SAT -S1 puzzle_file.cnf
  ```
- Verify the script uses Unix-style line endings (`LF`) using `dos2unix`:
  ```bash
  dos2unix SAT
  ```

#### 3. PATH not updated
- Reload the shell configuration:
  ```bash
  source ~/.bashrc
  ```
- Manually add the directory to PATH in `~/.bashrc` or `~/.zshrc`:
  ```bash
  export PATH=$PATH:/path/to/sat/directory
  ```
### Debugging Commands
- Run with debugging enabled:
  ```bash
  bash -x ./SAT -S1 puzzle_file.cnf
  ```

---

## Notes for Windows Users

- Use Git Bash for running the script.
- Ensure the script has executable permissions:
  ```bash
  chmod +x SAT
  ```
- Convert files to Unix-style line endings:
  ```bash
  dos2unix SAT install_sat.sh puzzle_file.cnf
  ```

---


## File Format
- Puzzle files must be in [DIMACS CNF format]().
- Ensure valid syntax and no trailing or unexpected characters.

---

## Manual PATH Configuration
If the automatic PATH configuration fails, manually add the SAT solver directory to your PATH.

1. Open your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.):
   ```bash
   nano ~/.bashrc
   ```
2. Add the following line:
   ```bash
   export PATH=$PATH:/path/to/sat/directory
   ```
3. Save the file and reload the configuration:
   ```bash
   source ~/.bashrc
   ```

Replace `/path/to/sat/directory` with the actual path to the SAT solver directory.

---
