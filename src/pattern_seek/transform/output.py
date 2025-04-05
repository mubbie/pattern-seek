"""
output.py

This module is responsible for displaying matched CSV rows in a tabular format
and optionally saving them to a new CSV file. It's part of the transform feature
in pattern-seek and helps visualize or persist filtered CSV data.

Functions:
- print_csv_matches(result): Pretty-prints the matched CSV rows using tabulate.
- save_csv_matches(result, output_file): Writes matched CSV rows to a new CSV file.
"""

import csv
from typing import Dict
from colorama import Fore, Style, init
from tabulate import tabulate

init()

def print_csv_matches(result: Dict) -> None:
    """
    Prints the matched rows from a CSV file in a tabular format.

    Args:
        result (Dict): The result dictionary containing file path, header, and matches.
    """
    file = result["file"]
    rows = result["matches"]
    header = result["header"]

    if not rows:
        print(f"{Fore.YELLOW}No matches found in {file}.{Style.RESET_ALL}")
        return
    
    # Display the filename
    print(f"\n{Fore.CYAN}{Style.BRIGHT}File: {file}{Style.RESET_ALL}")

    # Display the matching rows in a table format
    print(tabulate(rows, headers="keys", tablefmt="grid"))


def save_csv_matches(result: Dict, output_file: str) -> None:
    """
    Saves the matched rows from a CSV file to a new CSV file.

    Args:
        result (Dict): The result dictionary containing file path, header, and matches.
        output_file (str): The path to the output CSV file.
    """
    rows = result["matches"]
    header = result["header"]

    if not rows:
        print(f"{Fore.YELLOW}No matches found in {result['file']}.{Style.RESET_ALL}")
        return

    # Write matched rows to a new CSV file with headers
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=result["header"])
        writer.writeheader()  # Write the header to the CSV file
        writer.writerows(result["matches"])  # Write the matched rows to the CSV file
