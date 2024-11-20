# SAT Solver Setup Guide

## Overview

This repository contains a SAT (Boolean Satisfiability) solver and a setup script to make it easily accessible on your system. The setup script handles executable permissions and optionally adds the solver to your system PATH.

## Requirements

- Unix-like operating system (Linux, macOS)
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

## Troubleshooting

### Common Issues

1. **"SAT file not found" error**

   - Ensure you're in the correct directory
   - Verify the SAT executable exists
   - Check file permissions

2. **PATH not updated after setup**

   - Manually reload your shell configuration
   - Verify the PATH entry in your `.bashrc` or `.zshrc`

### Manual PATH Configuration

If the automatic PATH configuration fails, add this line to your shell configuration file:

```bash
export PATH=$PATH:/path/to/sat/directory
```

Replace `/path/to/sat/directory` with the actual path to your SAT solver directory.
