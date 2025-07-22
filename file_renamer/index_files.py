import os
import csv
import argparse

def list_files_to_csv(directory_path, output_csv_path):
    """
    Scans a directory for files and creates a CSV with columns
    for the current file name and a blank column for a new name.

    Args:
        directory_path (str): The absolute or relative path to the directory to scan.
        output_csv_path (str): The path where the output CSV file will be saved.
    """
    # --- 1. Validate the directory path ---
    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at '{directory_path}'")
        return

    # --- 2. Get the list of files ---
    try:
        # os.listdir() gets everything, so we filter for files only.
        # This list comprehension checks if the path is a file.
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        print(f"Found {len(files)} files in the directory.")
    except OSError as e:
        print(f"Error reading directory: {e}")
        return

    # --- 3. Write the data to a CSV file ---
    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            # Define the column headers
            fieldnames = ['current_name', 'new_name']
            
            # Create a writer object that will map dictionaries to rows
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Loop through each file and write a row to the CSV
            for filename in files:
                writer.writerow({'current_name': filename, 'new_name': ''})
        
        print(f"Successfully created CSV file at: {output_csv_path}")

    except IOError as e:
        print(f"Error writing to CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # --- 4. Set up command-line argument parsing ---
    # This makes the script more flexible and user-friendly.
    parser = argparse.ArgumentParser(
        description="Create a CSV of filenames from a directory, ready for renaming."
    )
    
    # Add an argument for the directory to scan
    parser.add_argument(
        "directory", 
        type=str, 
        help="The path to the directory you want to scan for files."
    )
    
    # Add an optional argument for the output file name
    parser.add_argument(
        "-o", 
        "--output", 
        type=str, 
        default="file_rename_list.csv", 
        help="The name of the output CSV file. (default: file_rename_list.csv)"
    )

    args = parser.parse_args()

    # --- 5. Construct the output path and run the main function ---
    # The output CSV will now be saved inside the scanned directory.
    output_path = os.path.join(args.directory, args.output)
    
    # The script starts executing here
    list_files_to_csv(args.directory, output_path)

