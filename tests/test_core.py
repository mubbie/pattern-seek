import os
import tempfile
import pytest
from pattern_seek.core import search_file, search_files

class TestFileSearch:
    def setup_method(self):
        # Create temporary test files
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create a test file with various patterns
        self.test_file_path = os.path.join(self.temp_dir.name, "test_data.txt")
        with open(self.test_file_path, "w") as f:
            f.write("""Line 1: This is a test file.
Line 2: Contact us at support@example.com for assistance.
Line 3: Order ID: 550e8400-e29b-41d4-a716-446655440000
Line 4: Dated on 2023-02-15
Line 5: Visit our website at https://example.com
Line 6: Server IP: 192.168.1.1
Line 7: Nothing interesting here
Line 8: Another email: user@example.org
""")
        
        # Create a second test file with no patterns
        self.empty_file_path = os.path.join(self.temp_dir.name, "empty_data.txt")
        with open(self.empty_file_path, "w") as f:
            f.write("""
                This file contains no pattern matches.
                Just some random text.
                Nothing to see here.
                """)
        
    def teardown_method(self):
        # Clean up temporary files
        self.temp_dir.cleanup()
        
    def test_search_file_single_pattern(self):
        # Test searching for emails
        results = search_file(self.test_file_path, pattern_type="email")
        assert len(results) == 2
        assert results[0]["match"] == "support@example.com"
        assert results[0]["line"] == 2
        assert results[1]["match"] == "user@example.org"
        assert results[1]["line"] == 8
        
        # Test searching for GUIDs
        results = search_file(self.test_file_path, pattern_type="guid")
        assert len(results) == 1
        assert results[0]["match"] == "550e8400-e29b-41d4-a716-446655440000"
        assert results[0]["line"] == 3
        
    def test_search_file_multiple_patterns(self):
        # Test searching for multiple pattern types
        results = search_file(
            self.test_file_path, 
            pattern_type=["email", "url", "ip"]
        )
        
        assert len(results) == 4
        
        # Count results by type
        type_counts = {}
        for result in results:
            type_counts[result["type"]] = type_counts.get(result["type"], 0) + 1
            
        assert type_counts["email"] == 2
        assert type_counts["url"] == 1
        assert type_counts["ip"] == 1
        
    def test_search_file_with_context(self):
        # Test searching with context lines
        results = search_file(
            self.test_file_path,
            pattern_type="email",
            context_lines=1
        )
        
        assert len(results) == 2
        assert "context_before" in results[0]
        assert "context_after" in results[0]
        
        # Check context content
        assert results[0]["context_before"] == ["Line 1: This is a test file."]
        assert results[0]["context_after"] == ["Line 3: Order ID: 550e8400-e29b-41d4-a716-446655440000"]
        
    def test_search_file_no_matches(self):
        # Test searching file with no matches
        results = search_file(self.empty_file_path, pattern_type="email")
        assert len(results) == 0
        
    def test_search_files(self):
        # Test searching multiple files
        results = search_files(
            [self.test_file_path, self.empty_file_path],
            pattern_type="email"
        )
        
        assert len(results) == 2
        assert results[0]["file"] == self.test_file_path
        assert len(results[0]["matches"]) == 2
        assert results[1]["file"] == self.empty_file_path
        assert len(results[1]["matches"]) == 0
        
    def test_search_directory(self):
        # Test searching a directory
        results = search_files(
            self.temp_dir.name,
            pattern_type="email"
        )
        
        assert len(results) == 2
        # Files might be in any order, so check contents instead
        assert any(r["file"] == self.test_file_path and len(r["matches"]) == 2 for r in results)
        assert any(r["file"] == self.empty_file_path and len(r["matches"]) == 0 for r in results)
        
    def test_search_with_wildcards(self):
        # Test searching with wildcards
        results = search_files(
            os.path.join(self.temp_dir.name, "*.txt"),
            pattern_type="email"
        )
        
        assert len(results) == 2