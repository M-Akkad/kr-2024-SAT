#!/bin/bash

# Get the directory of the SAT script
SAT_DIR=$(dirname "$(realpath "$0")")

# Check if the SAT file exists
if [[ ! -f "$SAT_DIR/SAT" ]]; then
    echo "Error: SAT file not found in $SAT_DIR. Please ensure the SAT file exists."
    exit 1
fi

# Make SAT executable
chmod +x "$SAT_DIR/SAT"
echo "SAT is now executable in the current directory."

# Inform the user to run the SAT command
echo "You can now run the SAT command from this directory using:"
echo "    ./SAT -S[1|2|3] <puzzle_file>"
echo "If you want to run it without ./, ensure this directory is in your PATH."

# Optionally persist the directory in PATH for global execution
read -p "Would you like to add this directory to your PATH for global access? (y/n): " response
if [[ "$response" =~ ^[Yy]$ ]]; then
    if [[ ":$PATH:" != *":$SAT_DIR:"* ]]; then
        echo "Adding SAT directory to PATH..."
        export PATH=$PATH:$SAT_DIR

        # Persist the change in the user's shell configuration
        if [[ -f "$HOME/.bashrc" ]]; then
            echo "export PATH=\$PATH:$SAT_DIR" >> "$HOME/.bashrc"
        elif [[ -f "$HOME/.zshrc" ]]; then
            echo "export PATH=\$PATH:$SAT_DIR" >> "$HOME/.zshrc"
        else
            echo "Warning: Could not persist PATH changes. Add the following line to your shell configuration:"
            echo "export PATH=\$PATH:$SAT_DIR"
        fi
        echo "SAT directory has been added to PATH. Restart your terminal or run:"
        echo "    source ~/.bashrc  # For bash users"
        echo "    source ~/.zshrc   # For zsh users"
    else
        echo "SAT directory is already in PATH."
    fi
else
    echo "You chose not to add the SAT directory to PATH. Run the command locally using ./SAT."
fi
