"""
test_common.py

Unit tests for the is_match function in pattern_seek.transform.common. 
Covers all combinations of case sensitivity and whole-word matching logic.
"""

import pytest
from pattern_seek.transform.common import is_match

def test_is_match():
    """Tests default is_match behavior: case-insensitive, partial match."""
    assert is_match("Apple", "app", False, False) == True
    assert is_match("Banana", "nan", False, False) == True
    assert is_match("APPLE", "apple", False, False) == True
    assert is_match("apple", "APPLE", False, False) == True
    assert is_match("Apple", "orange", False, False) == False

def test_is_match_case_sensitive():
    """Tests is_match with case-sensitive, partial match."""
    assert is_match("Apple", "app", True, False) == False  # 'App' != 'app'
    assert is_match("Apple", "App", True, False) == True
    assert is_match("BANANA", "BAN", True, False) == True
    assert is_match("BANANA", "ban", True, False) == False

def test_is_match_whole_word():
    """Tests is_match with whole-word matching (case-insensitive)."""
    assert is_match("Apple Pie", "Apple", False, True) == True
    assert is_match("Pineaple", "Apple", False, True) == False
    assert is_match("An apple a day", "Apple", False, True) == True
    assert is_match("Apples are good", "apple", False, True) == False # 'apple != 'Apples'

    # Punctuation and spacing
    assert is_match("Hello, word!", "Hello", False, True) == True
    assert is_match("Hello, world!", "world", False, True) == True

def test_is_match_case_sensitive_whole_word():
    """Tests is_match with both case sensitivity and whole-word matching."""
    assert is_match("Apple Pie", "apple", True, True) == False  # case mismatch
    assert is_match("Apple Pie", "Apple", True, True) == True
    assert is_match("APPLE PIE", "APPLE", True, True) == True
    assert is_match("APPLE_PIE", "apple", True, True) == False