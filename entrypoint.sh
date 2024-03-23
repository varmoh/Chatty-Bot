#!/bin/bash

# Function to install modules if needed
install_modules() {
    if [ -f "/app/helpers/install_modules.py" ]; then
        echo "Installing Python modules..."
        python /app/helpers/install_modules.py
    fi
}

# Function to run scripts
run_script() {
    script=$1
    if [ -f "/app/$script" ]; then
        echo "Running $script..."
        python "/app/$script"
    else
        echo "Script $script not found."
    fi
}

# Install modules
install_modules

# Run scripts based on environment variable
if [ "$RUN_SCRIPT" ]; then
    run_script "$RUN_SCRIPT"
else
    echo "No script specified. Exiting."
fi
