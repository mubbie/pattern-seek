"""
Module: csv_transform.py

This module provides functionality for transforming CSV files by searching rows based on a query. It supports column-specific searches, case sensitivity, and whole-word matching. Optionally, matched results can be saved to a new CSV file.
"""

import csv
from typing import List, Dict, Optional
from .common import is_match

def transform_csv(
        file_path: str,
        query: str,
        column: Optional[str] = None,
        case_sensitive: bool = False,
        matchword: bool = False,
        save: bool = False
) -> Dict:
    """
    Searches a CSV file for rows where the query string appears in one or more fields.

    Args:
        file_path (str): Path to the CSV file.
        query (str): The text to search for in the file.
        column (Optional[str]): If provided, only search this specific column.
        case_sensitive (bool): Whether the search should respect letter casing.
        matchword (bool): Whether to match whole words only.
        save (bool): If True, save the matching rows to a new CSV file.

    Returns:
        Dict: A dictionary containing the file path, CSV header, and matched rows.
              If save=True, returns an empty dict and saves results to file.
    """
    matches = []

    # Open and read the CSV file as dictionaries (fieldname => value)
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        header = reader.fieldnames

        if not header:
            raise ValueError("CSV file has no header row.")

        for row in reader:
            # If a specific column is given, limit search to it; otherwise search all fields
            search_fields = [column] if column else header

            for field in search_fields:
                value = row.get(field, "")
                # Check if the current field value matches the query
                if is_match(value, query, case_sensitive, matchword):
                    matches.append(row)
                    break  # stop checking this row once a match is found

    if save:
        if not matches:
            print(f"No matches found in {file_path}. Nothing was saved.")
            return {}
        
        from .output import save_csv_matches
        save_path = file_path.replace('.csv', '-transformed.csv')

        # Save the matched rows to a new CSV file
        save_csv_matches({
            "file": file_path, 
            "header": header, 
            "matches": matches
        }, save_path)

        print(f"\nSaved transformed results to {save_path}")
        return {}
    
    return {
        "file": file_path,
        "header": header,
        "matches": matches
    }