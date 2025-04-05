"""
test_integration.py

Integration tests for the CSV transform feature. These tests verify that
transform_csv, save_csv_matches, and print_csv_matches work together as expected.
It covers full transform flows including saving and printing results.
"""

import pytest
import os
import csv

from pattern_seek.transform.csv_transform import transform_csv
from pattern_seek.transform.output import print_csv_matches, save_csv_matches

@pytest.fixture
def sample_csv_content():
    """Create sample CSV content for testing."""
    return (
        "name,age,city\n"
        "Alice,30,New York\n"
        "Bob,25,Los Angeles\n"
        "Charlie,35,Chicago\n"
        "David,40,New York\n"
        "John Doe,30,New York\n"
        "Jane Smith,25,Los Angeles\n"
        "Bob Johnson,40,Chicago\n"
        "Alice Brown,35,San Francisco\n"
    )

@pytest.fixture
def temp_csv_file(tmp_path, sample_csv_content):
    """Create a temporary CSV file for testing."""
    file_path = tmp_path / "test.csv"
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        f.write(sample_csv_content)
    return str(file_path)

def test_end_to_end_transform_and_save(temp_csv_file):
    """Test the full transform and save pipeline, then verify saved file content."""
    # Expected output file path
    output_path = temp_csv_file.replace(".csv", "-transformed.csv")

    # Run transform with save
    transform_csv(temp_csv_file, "John", save=True)

    # Verify output file exists
    assert os.path.exists(output_path)

    # Verify output file's contents
    with open(output_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

        # Check that the output file has the expected number of rows
        assert len(rows) == 2

        # Verify contents
        john_row = None
        bob_row = None

        for row in rows:
            if row["name"] == "John Doe":
                john_row = row
            elif row["name"] == "Bob Johnson":
                bob_row = row

        assert john_row is not None
        assert john_row["age"] == "30"
        assert john_row["city"] == "New York"

        assert bob_row is not None
        assert bob_row["age"] == "40"
        assert bob_row["city"] == "Chicago"

def test_end_to_end_with_different_search_params(temp_csv_file):
    """Test transform and save with matchword and column-specific filtering."""
    # Test with matchword=True
    exact_output = temp_csv_file.replace(".csv", "-transformed.csv")
    transform_csv(temp_csv_file, "John", matchword=True, save=True)

    # Verify output
    with open(exact_output, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

        # Should have only one row (John Doe, not Bob Johnson)
        assert len(rows) == 1
        assert rows[0]["name"] == "John Doe"

    # Test with column-specific search
    os.remove(exact_output) # Clean up previous output
    transform_csv(temp_csv_file, "New York", column="city", save=True)

    # Verify output
    with open(exact_output, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

        # Should have only three rows
        assert len(rows) == 3
        assert rows[0]["name"] == "Alice"
        assert rows[1]["name"] == "David"
        assert rows[2]["name"] == "John Doe"

    # Test with column-specific search
    os.remove(exact_output) # Clean up previous output
    transform_csv(temp_csv_file, "New", column="city", save=True)

    # Verify output
    with open(exact_output, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

        # Should have only three rows
        assert len(rows) == 3
        assert rows[0]["name"] == "Alice"
        assert rows[1]["name"] == "David"
        assert rows[2]["name"] == "John Doe"

def test_transform_and_print_integration(temp_csv_file, capsys):
    """Test that print_csv_matches prints output from transform_csv correctly."""
    # Get transform results
    result = transform_csv(temp_csv_file, "John")
    
    # Print the results
    print_csv_matches(result)

    # Check the output
    captured = capsys.readouterr()

    # Verify output contains expected content
    assert f"File: {temp_csv_file}" in captured.out
    assert "John Doe" in captured.out
    assert "New York" in captured.out
    assert "Bob Johnson" in captured.out
    assert "Chicago" in captured.out