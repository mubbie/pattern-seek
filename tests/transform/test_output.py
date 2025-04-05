"""
test_output.py

Unit tests for the output module, which handles printing and saving of matched
CSV data. These tests verify that print_csv_matches displays correct output and
that save_csv_matches writes the expected files and handles edge cases properly.
"""

import pytest
import os
import csv

from unittest.mock import patch
from io import StringIO
from colorama import Fore, Style

from pattern_seek.transform.output import print_csv_matches, save_csv_matches

@pytest.fixture
def sample_matches_data():
    """Provides a sample dictionary with matched CSV rows for testing."""
    return {
        "file": "test.csv",
        "header": ["name", "age", "city"],
        "matches": [
            {"name": "John Doe", "age": "30", "city": "New York"},
            {"name": "Bob Johnson", "age": "40", "city": "Chicago"}
        ]
    }

@pytest.fixture
def empty_matches_data():
    """Provides a sample dictionary with no matched rows (empty results)."""
    return {
        "file": "test.csv",
        "header": ["name", "age", "city"],
        "matches": []
    }

def test_print_csv_matches(sample_matches_data, capsys):
    """Test that print_csv_matches displays the expected output"""
    # Run the function and capture stdout
    print_csv_matches(sample_matches_data)
    
    # Get captured stdout
    captured = capsys.readouterr()
    
    # Verify output includes expected file reference and row content
    assert f"File: {sample_matches_data['file']}" in captured.out
    assert "John Doe" in captured.out
    assert "New York" in captured.out
    assert "Bob Johnson" in captured.out
    assert "Chicago" in captured.out
    
    # Should contain tabulate's grid format
    assert "+" in captured.out  # Grid lines
    assert "|" in captured.out  # Grid columns

def test_print_csv_matches_no_matches(empty_matches_data, capsys):
    """Test that print_csv_matches handles empty results correctly"""
    # Run the function to print matches
    print_csv_matches(empty_matches_data)
    
    # Get captured stdout
    captured = capsys.readouterr()
    
    # Check output contains expected message for no matches
    assert f"No matches found in {empty_matches_data['file']}" in captured.out

def test_save_csv_matches_creates_file(tmp_path, sample_matches_data):
    """Test that save_csv_matches creates a file with the expected content."""
    # Prepare output file path using pytest's tmp_path fixture
    output_path = os.path.join(tmp_path, "output.csv")
    
    # Save matched row to a CSV file
    save_csv_matches(sample_matches_data, output_path)
    
    # Verify file exists
    assert os.path.exists(output_path)
    
    # Read the saved file and verify it matches input data
    with open(output_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        
        # Check that we have correct number of rows
        assert len(rows) == 2
        
        # Check that headers are correct
        assert reader.fieldnames == sample_matches_data["header"]
        
        # Check content of the first row
        assert rows[0]["name"] == "John Doe"
        assert rows[0]["age"] == "30"
        assert rows[0]["city"] == "New York"
        
        # Check content of the second row
        assert rows[1]["name"] == "Bob Johnson"
        assert rows[1]["age"] == "40"
        assert rows[1]["city"] == "Chicago"

def test_save_csv_matches_empty_data(tmp_path, empty_matches_data, capsys):
    """Test that save_csv_matches handles empty data correctly."""
    # Prepare test file path
    output_path = os.path.join(tmp_path, "empty.csv")
    
    # Save matches
    save_csv_matches(empty_matches_data, output_path)
    
    # Check that appropriate message was printed
    captured = capsys.readouterr()
    assert f"No matches found in {empty_matches_data['file']}" in captured.out
    
    # File should not be created
    assert not os.path.exists(output_path)