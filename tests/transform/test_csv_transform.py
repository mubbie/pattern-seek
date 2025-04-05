"""
test_csv_transform.py

This file contains unit tests for the CSV transformation feature of the pattern-seek CLI tool.
It tests core behaviors such as text matching, column filtering, case sensitivity, and saving
matched rows to a new file. These tests ensure the transform_csv function behaves as expected
under various scenarios and edge cases.
"""

import pytest
import os
import csv
from unittest.mock import patch, mock_open
from io import StringIO

from pattern_seek.transform.csv_transform import transform_csv

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

def test_transform_csv_basic_search(temp_csv_file):
    """Test basic search functionality without any additional parameters."""
    result = transform_csv(temp_csv_file, "John")

    assert result["file"] == temp_csv_file
    assert result["header"] == ["name", "age", "city"]
    assert len(result["matches"]) == 2  # Both "John Doe" and "Bob Johnson" should match.

    # Verify both expected matches are present
    john_doe = None
    bob_johnson = None

    for match in result["matches"]:
        if match["name"] == "John Doe":
            john_doe = match
        elif match["name"] == "Bob Johnson":
            bob_johnson = match

    assert john_doe is not None
    assert john_doe["age"] == "30"
    assert john_doe["city"] == "New York"

    assert bob_johnson is not None
    assert bob_johnson["age"] == "40"
    assert bob_johnson["city"] == "Chicago"

def test_transform_csv_case_sensitivity(temp_csv_file):
    """Test case sensitivity in searching."""

    # Case insensitive (default)
    result = transform_csv(temp_csv_file, "john")
    assert len(result["matches"]) == 2  # Should find "John Doe" and "Bob Johnson".

    # Case sensitive
    result = transform_csv(temp_csv_file, "john", case_sensitive=True)
    assert len(result["matches"]) == 0  # Should find no matches for lowercase "john".

    # Case sensitive with exact match
    result = transform_csv(temp_csv_file, "John", case_sensitive=True)
    assert len(result["matches"]) == 2  # Should find "John Doe" and "Bob Johnson".

def test_transform_csv_matchword(temp_csv_file):
    """Test matchword functionality."""

    # Without matchword, "John" should match "John Doe" and "Bob Johnson".
    result = transform_csv(temp_csv_file, "John")
    assert len(result["matches"]) == 2  # Should find both "John Doe" and "Bob Johnson".

    # With matchword, "John" should only match "John Doe".
    result = transform_csv(temp_csv_file, "John", matchword=True)
    assert len(result["matches"]) == 1  # Should find only "John Doe".
    assert result["matches"][0]["name"] == "John Doe"

    # With matchword and case sensitivity, "john" should not match anything.
    result = transform_csv(temp_csv_file, "john", matchword=True, case_sensitive=True)
    assert len(result["matches"]) == 0  # Should find no matches.

    result = transform_csv(temp_csv_file, "John", matchword=True, case_sensitive=True)
    assert len(result["matches"]) == 1 # Should find only "John Doe".

def test_transform_csv_column_specific_search(temp_csv_file):
    """Test searching in a specific column."""

    # Search for "New" but only in the city column
    result = transform_csv(temp_csv_file, "New", column="city")

    assert len(result["matches"]) == 3 # "Alice", "David", and "John Doe" should match.
    assert result["matches"][0]["name"] == "Alice"
    assert result["matches"][1]["name"] == "David"
    assert result["matches"][2]["name"] == "John Doe"

    # This should find nothing as "John" is not in the age column
    result = transform_csv(temp_csv_file, "John", column="age")
    assert len(result["matches"]) == 0

def test_transform_csv_no_matches(temp_csv_file):
    """Test behavior when no matches are found."""
    result = transform_csv(temp_csv_file, "NonExistentName")

    assert result["file"] == temp_csv_file
    assert result["header"] == ["name", "age", "city"]
    assert len(result["matches"]) == 0

def test_transform_csv_empty_file():
    """Test handling of an empty CSV file."""
    with patch("builtins.open", mock_open(read_data="name,age,city\n")):
        result = transform_csv("dummy.csv", "test")

        assert result["header"] == ["name", "age", "city"]
        assert len(result["matches"]) == 0

def test_transform_csv_no_header():
    """Test handling of a CSV file with no header."""
    with patch("builtins.open", mock_open(read_data="")):
        with pytest.raises(ValueError, match="CSV file has no header row."):
            transform_csv("dummy.csv", "test")

def test_transform_csv_with_basic_save(temp_csv_file):
    """Test that save=True returns empty dict and prints expected message."""
    with patch("builtins.print") as mock_print:
        # Verify that we get an empty dict when save=True
        result = transform_csv(temp_csv_file, "John", save=True)
        assert result == {}

        #Verify that the expected message is printed
        expected_save_path = temp_csv_file.replace('.csv', '-transformed.csv')
        mock_print.assert_called_once_with(f"\nSaved transformed results to {expected_save_path}")

def test_transform_csv_with_no_matches_save(temp_csv_file):
    """Test save=True when no matches are found; should skip file writing and print a message."""
    with patch("builtins.print") as mock_print:
        result = transform_csv(temp_csv_file, "NonExistentName", save=True)

        # Check that the result is an empty dict
        assert result == {}

        # Check that the appropriate message is printed
        mock_print.assert_called_once_with(f"No matches found in {temp_csv_file}. Nothing was saved.")