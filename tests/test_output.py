import pytest
from io import StringIO
from pattern_seek.output import format_matches, print_matches

class TestOutputFormatting:
    def test_format_matches_simple(self):
        # Test basic match formatting
        matches = [
            {"type": "email", "match": "test@example.com", "line": 5},
            {"type": "url", "match": "https://example.com", "line": 10},
        ]
        
        formatted = format_matches(matches)
        
        assert "Line 5" in formatted
        assert "test@example.com" in formatted
        assert "Line 10" in formatted
        assert "https://example.com" in formatted
        
    def test_format_matches_with_context(self):
        # Test formatting with context lines
        matches = [
            {
                "type": "email", 
                "match": "test@example.com", 
                "line": 5,
                "context_before": ["Line 4: Some content"],
                "context_after": ["Line 6: More content"]
            }
        ]
        
        formatted = format_matches(matches)
        
        assert "Line 4" in formatted
        assert "Line 5" in formatted
        assert "Line 6" in formatted
        assert "test@example.com" in formatted
        
    def test_format_matches_with_file_info(self):
        # Test formatting with file information
        file_matches = [
            {
                "file": "test.txt",
                "matches": [
                    {"type": "email", "match": "test@example.com", "line": 5},
                ]
            }
        ]
        
        formatted = format_matches(file_matches, include_file_info=True)
        
        assert "test.txt" in formatted
        assert "Line 5" in formatted
        assert "test@example.com" in formatted
        
    def test_print_matches(self):
        # Test printing matches to a stream
        matches = [
            {"type": "email", "match": "test@example.com", "line": 5},
        ]
        
        output = StringIO()
        print_matches(matches, output=output)
        
        result = output.getvalue()
        assert "Line 5" in result
        assert "test@example.com" in result