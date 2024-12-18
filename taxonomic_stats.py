"""
Taxonomic Data Analysis script
Author: Anestis Gkanogiannis
Email: anestis@gkanogiannis.com
Date: 18 December 2024
Version: 1.0
Description:
    This script processes taxonomic species data to:
    1. Calculate summary statistics (total and average species count per phylum).
    2. Save results in a CSV file.
    3. Generate a bar chart visualizing the total species count per phylum.

License:
    MIT License

    Copyright (c) 2024 Anestis Gkanogiannis

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software
    and associated documentation files (the "Software"), to deal in the Software without restriction,
    including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial
    portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
    LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from io import StringIO
import logging
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def read_data(file_path: str | StringIO) -> pd.DataFrame:
    """
    Reads the input CSV file and handles missing/invalid data.
    
    Args:
        file_path (str | StringIO): Path to the input CSV file or a StringIO object.
    
    Returns:
        pd.DataFrame: Cleaned data frame with valid rows.
    """
    try:
        # Check if input is a file path or StringIO object
        if isinstance(file_path, str):
            if not os.path.exists(file_path):
                logging.error("File not found: %s", file_path)
                sys.exit(1)
            df = pd.read_csv(file_path)
        elif isinstance(file_path, StringIO):
            df = pd.read_csv(file_path)
        else:
            logging.error("Invalid input: file_path must be a string or StringIO object.")
            sys.exit(1)
        
        # Validate required columns
        required_columns = {"species", "phylum", "count"}
        if not required_columns.issubset(df.columns):
            logging.error("Invalid file format. Required columns: %s", required_columns)
            sys.exit(1)

        # Handle missing and invalid data
        df = df.dropna(subset=list(required_columns))
        df["count"] = pd.to_numeric(df["count"], errors="coerce")
        df = df.dropna(subset=["count"])  # Drop rows where count is not numeric
        df["count"] = df["count"].astype(int)

        logging.info("Data successfully loaded and cleaned.")
        return df

    except Exception as e:
        logging.error("Error while reading the file: %s", e)
        sys.exit(1)

def calculate_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates total and average species count per phylum.
    
    Args:
        df (pd.DataFrame): Input data frame with species counts.
    
    Returns:
        pd.DataFrame: Summary statistics per phylum.
    """
    try:
        summary = (
            df.groupby("phylum", as_index=False)
            .agg(
                total_species_count=("count", "sum"),
                average_species_count=("count", "mean")
            )
        )
        summary["average_species_count"] = summary["average_species_count"].round(2)
        logging.info("Summary statistics successfully calculated.")
        return summary
    except Exception as e:
        logging.error("Error calculating summary statistics: %s", e)
        sys.exit(1)

def save_results(df: pd.DataFrame, output_file: str):
    """
    Saves the summary statistics to a CSV file.
    
    Args:
        df (pd.DataFrame): Summary statistics data.
        output_file (str): Path to the output CSV file.
    """
    try:
        df.to_csv(output_file, index=False)
        logging.info("Results saved to %s", output_file)
    except Exception as e:
        logging.error("Error saving results to file: %s", e)
        sys.exit(1)

def generate_bar_chart(df: pd.DataFrame, output_image: str):
    """
    Generates a bar chart showing total species count per phylum.
    
    Args:
        df (pd.DataFrame): Summary statistics data.
        output_image (str): Path to save the bar chart image.
    """
    try:
        plt.figure(figsize=(10, 6))
        plt.bar(df["phylum"], df["total_species_count"], color="skyblue")
        plt.title("Total Species Count by Phylum", fontsize=14)
        plt.xlabel("Phylum", fontsize=12)
        plt.ylabel("Total Species Count", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_image)
        plt.close()
        logging.info("Bar chart saved to %s", output_image)
    except Exception as e:
        logging.error("Error generating bar chart: %s", e)
        sys.exit(1)

def main():
    """
    Main function to execute the script workflow.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description=(
            "Taxonomic Data Analysis Script\n"
            "This script processes taxonomic species data to calculate summary statistics, "
            "save results to a CSV file, and generate a bar chart visualization.\n\n"
            "Examples:\n"
            "  python taxonomic_stats.py\n"
            "  python taxonomic_stats.py -i custom_data.csv -o custom_summary.csv -p custom_plot.png"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-i", "--input", type=str, default="taxonomic_data.csv",
        help="Path to the input CSV file. Defaults to 'taxonomic_data.csv'."
    )
    parser.add_argument(
        "-o", "--output", type=str, default="phylum_summary.csv",
        help="Path to the output CSV file. Defaults to 'phylum_summary.csv'."
    )
    parser.add_argument(
        "-p", "--plot", type=str, default="phylum_species_count.png",
        help="Path to the output bar chart image file. Defaults to 'phylum_species_count.png'."
    )
    args = parser.parse_args()

    # Assign arguments to variables
    input_file = args.input
    output_csv = args.output
    output_image = args.plot

    # Step 1: Read and clean the data
    data = read_data(input_file)

    # Step 2: Calculate summary statistics
    summary_stats = calculate_summary_statistics(data)

    # Step 3: Save results to CSV
    save_results(summary_stats, output_csv)

    # Step 4: Generate bar chart
    generate_bar_chart(summary_stats, output_image)

    logging.info("Task completed successfully!")

if __name__ == "__main__":
    main()
