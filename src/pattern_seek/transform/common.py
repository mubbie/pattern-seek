"""
common.py

This module provides reusable logic for matching text values, used across various transformation formats (e.g., CSV, XLSX). It supports case sensitivity and whole-word matching options and is used to determine if a cell value matches a given query string.
"""

import re

def is_match(cell_value: str, query: str, case_sensitive: bool, matchword: bool) -> bool:
    """
    Checks if a cell value matches a given query based on specified criteria.

    Args:
        cell_value (str): The value in the cell to check.
        query (str): The query string to match against.
        case_sensitive (bool): If True, the match is case-sensitive. Default is False.
        matchword (bool): If True, matches only whole words. Default is False.

    Returns:
        bool: True if the cell value matches the query, False otherwise.
    """
    if not case_sensitive:
        cell_value = cell_value.lower()
        query = query.lower()
    
    if matchword:
        # Match only if the query appears as a full word using word boundaries
        pattern = r'\b' + re.escape(query) + r'\b'
        return bool(re.search(pattern, cell_value))
    
    # Basic substring search
    return query in cell_value