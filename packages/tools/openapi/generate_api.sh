#!/bin/bash

# Check if correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 path_to_json_file path_to_output_directory"
    exit 1
fi

# Assign arguments to variables for easier usage
json_file_path="$1"
output_directory="$2"

# Get the directory where the script itself is located
script_dir="$(dirname "$0")"

# Navigate to the script's directory
cd "$script_dir"

# Call the OpenAPI generator with the provided arguments
openapi-generator-cli generate -i "$json_file_path" -g typescript-fetch -o "$output_directory"

# Check if openapi-generator-cli ran successfully
if [ $? -eq 0 ]; then
    echo "API client code generated successfully."
else
    echo "Failed to generate API client code."
    exit 1
fi
