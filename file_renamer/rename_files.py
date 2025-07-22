import os
import csv

# --- Configuration ---

FILE_NAMES = 'file_rename_list.csv'

OLD_FILENAME_COLUMN = 'current_name'

NEW_FILENAME_COLUMN = 'new_name'

FILES_DIRECTORY = input("Please enter the path to the folder containing the files to rename: ")

CSV_FILE_PATH = FILES_DIRECTORY + "/" + FILE_NAMES

# --- Script Logic (No need to edit below this line) ---

def rename_files_from_csv():
    """
    Reads a CSV file and renames files in a specified directory
    based on the 'old' and 'new' filename columns.
    """
    print("--- Starting File Renaming Script ---")

    # Check if the CSV file exists
    if not os.path.isfile(CSV_FILE_PATH):
        print(f"ERROR: The CSV file was not found at '{CSV_FILE_PATH}'")
        return

    # Check if the files directory exists
    if not os.path.isdir(FILES_DIRECTORY):
        print(f"ERROR: The directory was not found at '{FILES_DIRECTORY}'")
        return

    processed_count = 0
    error_count = 0

    try:
        with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as csvfile:
            # Using DictReader to access columns by their header names
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    old_name = row[OLD_FILENAME_COLUMN]
                    new_name = row[NEW_FILENAME_COLUMN]

                    # Construct the full path for the old and new filenames
                    old_file_path = os.path.join(FILES_DIRECTORY, old_name)
                    new_file_path = os.path.join(FILES_DIRECTORY, new_name)

                    # --- Core Renaming Logic ---

                    # Check if the original file actually exists
                    if os.path.exists(old_file_path):
                        # Check if the new filename would overwrite an existing file
                        if os.path.exists(new_file_path):
                            print(f"SKIPPED: New name '{new_name}' already exists. Cannot rename '{old_name}'.")
                            error_count += 1
                        else:
                            # Perform the rename
                            os.rename(old_file_path, new_file_path)
                            print(f"SUCCESS: Renamed '{old_name}' to '{new_name}'")
                            processed_count += 1
                    else:
                        print(f"SKIPPED: Original file '{old_name}' not found in the directory.")
                        error_count += 1

                except KeyError as e:
                    print(f"ERROR: CSV is missing a required column: {e}. Please check your column names.")
                    return # Stop the script if columns are wrong
                except Exception as e:
                    print(f"An unexpected error occurred for row: {row}. Error: {e}")
                    error_count += 1

    except FileNotFoundError:
        print(f"ERROR: Could not open the CSV file at '{CSV_FILE_PATH}'")
        return
    except Exception as e:
        print(f"A critical error occurred: {e}")
        return

    print("\n--- Script Finished ---")
    print(f"Successfully renamed: {processed_count} files.")
    print(f"Skipped or failed: {error_count} files.")

if __name__ == '__main__':
    # This makes the script runnable from the command line
    rename_files_from_csv()

