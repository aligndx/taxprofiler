#!/usr/bin/env python

import argparse
import os
import csv

def parse_kraken_report(input_file):
    """
    Parses a Kraken report file to extract classification statistics.
    """
    total_sequences = 0
    classified_reads = 0
    unclassified_reads = 0

    with open(input_file, "r") as file:
        # Read only the first two lines of the file
        line = file.readline().strip()
        if line:
            parts = line.split("\t")
            if len(parts) >= 6:
                num_reads = int(parts[1])
                taxon_rank = parts[3]
                taxon_name = parts[5].strip()
                if taxon_rank == "U" and taxon_name == "unclassified":
                    unclassified_reads = num_reads

        line = file.readline().strip()
        if line:
            parts = line.split("\t")
            if len(parts) >= 6:
                num_reads = int(parts[1])
                taxon_rank = parts[3]
                taxon_name = parts[5].strip()
                if taxon_rank == "R" and taxon_name == "root":
                    classified_reads = num_reads

    # Calculate total sequences
    total_sequences = unclassified_reads + classified_reads

    return total_sequences, classified_reads, unclassified_reads

def generate_statistics_csv(output_file, summary_data):
    """
    Generate a CSV file with summary statistics.
    """
    fieldnames = [
        "sample_name",
        "total_sequences",
        "classified_reads",
        "unclassified_reads",
        "percentage_classified",
    ]

    with open(output_file, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for sample_name, data in summary_data.items():
            total_sequences, classified_reads, unclassified_reads = data
            percentage_classified = (
                (classified_reads / total_sequences) * 100
                if total_sequences > 0
                else 0.0
            )

            writer.writerow(
                {
                    "sample_name": sample_name,
                    "total_sequences": total_sequences,
                    "classified_reads": classified_reads,
                    "unclassified_reads": unclassified_reads,
                    "percentage_classified": percentage_classified,
                }
            )

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Parse Kraken reports and generate summary statistics."
    )
    parser.add_argument(
        "input_files", nargs="+", help="Paths to the Kraken report input files."
    )
    parser.add_argument("output_file", help="Path to the CSV output file.")
    args = parser.parse_args()

    # Parse each Kraken report and collect statistics
    summary_data = {}
    for input_file in args.input_files:
        sample_name = os.path.basename(input_file).split(".")[
            0
        ]  # Use the filename as the sample name
        total_sequences, classified_reads, unclassified_reads = parse_kraken_report(
            input_file
        )
        summary_data[sample_name] = (
            total_sequences,
            classified_reads,
            unclassified_reads,
        )

    # Generate CSV file with statistics
    generate_statistics_csv(args.output_file, summary_data)
    print(f"Summary statistics written to {args.output_file}")

if __name__ == "__main__":
    main()
