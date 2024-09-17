#!/usr/bin/env python

import csv
import argparse

def transform_to_long_format_custom(input_file, output_file, output_format_is_csv):
    # Set the delimiter based on whether the output should be CSV or TSV
    delimiter = ',' if output_format_is_csv else '\t'
    
    # Read the input file (assuming it's a TSV file)
    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile, delimiter='\t')  # Reading input as TSV
        fieldnames = ['name', 'taxonomy_id', 'taxonomy_lvl', 'sample', 'abundance_num', 'abundance_frac']
        
        # Open the output file to write as CSV or TSV
        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=delimiter)  # Writing output based on the format
            writer.writeheader()

            # Process each row from the input
            for row in reader:
                name = row['name']
                taxonomy_id = row['taxonomy_id']
                taxonomy_lvl = row['taxonomy_lvl']
                
                # Initialize variables for each row
                abundance_num = None
                abundance_frac = None
                
                # Extract sample and measure values
                for key in row.keys():
                    if key not in ['name', 'taxonomy_id', 'taxonomy_lvl']:
                        sample, measure = key.rsplit('_', 1)
                        
                        if measure == 'num':
                            abundance_num = row[key]
                        elif measure == 'frac':
                            abundance_frac = row[key]

                        # Only write when both num and frac are present for the sample
                        if abundance_num and abundance_frac:
                            writer.writerow({
                                'name': name,
                                'taxonomy_id': taxonomy_id,
                                'taxonomy_lvl': taxonomy_lvl,
                                'sample': sample,
                                'abundance_num': abundance_num,
                                'abundance_frac': abundance_frac
                            })
                            abundance_num = None  # Reset abundance_num for the next sample
                            abundance_frac = None  # Reset abundance_frac for the next sample

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform a TSV file from wide to long format")
    parser.add_argument("input_file", help="Path to the input TSV file")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument("--csv", action="store_true", help="Set this flag to output in CSV format instead of TSV")

    args = parser.parse_args()
    transform_to_long_format_custom(args.input_file, args.output_file, args.csv)
