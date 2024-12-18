#!/bin/bash

# Usage function to display help
usage() {
    echo "Usage: $0 [-i|--input <input_file>] [-o|--output <output_file>] [-p|--plot <plot_file>]"
    echo "If no arguments are provided, then the script will use taxonomic_data.csv as input, phylum_summary.csv and phylum_species_count.png as outputs in the current directory."
    exit 1
}

# Parse arguments
INPUT_FILE=""
OUTPUT_FILE=""
PLOT_FILE=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        -i|--input)
            INPUT_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -p|--plot)
            PLOT_FILE="$2"
            shift 2
            ;;
        *)
            usage
            ;;
    esac
done

# Check if no arguments are provided
if [[ -z "$INPUT_FILE" && -z "$OUTPUT_FILE" && -z "$PLOT_FILE" ]]; then
    # Mount the current folder to /app and run the container without arguments
    docker run --rm -v "$(pwd):/data" gkanogiannis/taxonomic_stats
    exit 0
fi

# Check if wrong argument combination is provided
if [[ -z "$INPUT_FILE" && -n "$OUTPUT_FILE" ]]; then
    usage
fi
if [[ -z "$INPUT_FILE" && -n "$PLOT_FILE" ]]; then
    usage
fi

# Automatically derive OUTPUT_FILE if -i is provided but -o is not
if [[ -n "$INPUT_FILE" && -z "$OUTPUT_FILE" ]]; then
    INPUT_BASENAME=$(basename "$INPUT_FILE")    # Extract the file name
    INPUT_DIR=$(dirname $(realpath "$INPUT_FILE"))          # Extract the input file directory
    OUTPUT_FILE="$INPUT_DIR/${INPUT_BASENAME%.*}.out.csv" # Replace extension with .out.csv
fi

# Automatically derive PLOT_FILE if -i is provided but -p is not
if [[ -n "$INPUT_FILE" && -z "$PLOT_FILE" ]]; then
    INPUT_BASENAME=$(basename "$INPUT_FILE")    # Extract the file name
    INPUT_DIR=$(dirname $(realpath "$INPUT_FILE"))          # Extract the input file directory
    PLOT_FILE="$INPUT_DIR/${INPUT_BASENAME%.*}.plot.png" # Replace extension with .plot.png
fi

# Extract directories from file paths if arguments are provided
INPUT_DIR=$(dirname $(realpath "$INPUT_FILE"))
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
PLOT_DIR=$(dirname "$PLOT_FILE")

# Build the docker run command dynamically with volume mounts
DOCKER_CMD="docker run --rm"

if [[ -n "$INPUT_FILE" ]]; then
    DOCKER_CMD="$DOCKER_CMD -v \"$INPUT_DIR:/data/input\""
fi

if [[ -n "$OUTPUT_FILE" ]]; then
    DOCKER_CMD="$DOCKER_CMD -v \"$OUTPUT_DIR:/data/output\""
fi

if [[ -n "$PLOT_FILE" ]]; then
    DOCKER_CMD="$DOCKER_CMD -v \"$PLOT_DIR:/data/plot\""
fi

# Add the image name
DOCKER_CMD="$DOCKER_CMD gkanogiannis/taxonomic_stats"

# Add arguments
if [[ -n "$INPUT_FILE" ]]; then
    DOCKER_CMD="$DOCKER_CMD -i \"/data/input/$(basename "$INPUT_FILE")\""
fi

if [[ -n "$OUTPUT_FILE" ]]; then
    DOCKER_CMD="$DOCKER_CMD -o \"/data/output/$(basename "$OUTPUT_FILE")\""
fi

if [[ -n "$PLOT_FILE" ]]; then
    DOCKER_CMD="$DOCKER_CMD -p \"/data/plot/$(basename "$PLOT_FILE")\""
fi

# Execute the command
eval "$DOCKER_CMD"
