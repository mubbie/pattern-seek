import pytest
from pattern_seek.patterns import find_pattern_matches

class TestPatternMatching:
    def test_find_guid_matches(self):
        # Test GUID pattern matching
        text = """
        Valid GUIDs:
        550e8400-e29b-41d4-a716-446655440000
        550E8400-E29B-41D4-A716-446655440000
        550e8400e29b41d4a716446655440000
        F47AC10B-58CC-4372-A567-0E02B2C3D479
        e3af0274-fe74-484c-bb6e-f182f1fd8558
        
        Invalid GUIDs:
        550e8400-e29b-41d4-a716-44665544000  # too short
        550e8400-e29b-41d4-a716-4466554400000  # too long
        550e8400-e29b-41d4-a716_446655440000  # invalid character
        not-a-guid
        ZZZZZZZZ-ZZZZ-ZZZZ-ZZZZ-ZZZZZZZZZZZZ  # invalid hex digits
        """
        
        results = find_pattern_matches(text, pattern_type="guid")
        
        # Should match 5 valid GUIDs
        assert len(results) == 5
        
        # Check specific matches
        matched_values = [r["match"] for r in results]
        assert "550e8400-e29b-41d4-a716-446655440000" in matched_values
        assert "550E8400-E29B-41D4-A716-446655440000" in matched_values
        assert "550e8400e29b41d4a716446655440000" in matched_values
        assert "F47AC10B-58CC-4372-A567-0E02B2C3D479" in matched_values
        assert "e3af0274-fe74-484c-bb6e-f182f1fd8558" in matched_values
        
        # Make sure none of the invalid GUIDs were matched
        for match in matched_values:
            assert len(match.replace("-", "")) == 32  # Valid GUID/UUID length
    
    def test_guid_edge_cases(self):
        # More edge cases for GUIDs
        text = """
        Edge case GUIDs:
        # Valid but unusual:
        00000000-0000-0000-0000-000000000000
        FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF
        01234567-89ab-cdef-ABCD-EF0123456789
        
        # Invalid variants:
        550e84000-e29b-41d4-a716-446655440000  # extra digit
        550e8400--e29b-41d4-a716-446655440000  # double hyphen
        """
        
        results = find_pattern_matches(text, pattern_type="guid")
        
        # Should match the 3 valid GUIDs
        assert len(results) == 3
        
        # Check specific matches
        matched_values = [r["match"] for r in results]
        assert "00000000-0000-0000-0000-000000000000" in matched_values
        assert "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF" in matched_values
        assert "01234567-89ab-cdef-ABCD-EF0123456789" in matched_values
            
    def test_find_email_matches(self):
        # Test email pattern matching
        text = """
        Valid emails:
        user@example.com
        first.last@example.co.uk
        user+tag@example.org
        user.name@subdomain.example.com
        very.common@example.com
        disposable.style.email.with+tag@example.com
        other.email-with-hyphen@example.com
        fully-qualified-domain@example.com
        user.name+tag+sorting@example.com
        x@example.com
        example-indeed@strange-example.com
        example@s.example
        
        Invalid emails:
        user@
        @example.com
        user@.com
        user@example
        user@example.
        user@exam_ple.com
        Abc.example.com

        Technically invalid, but should match since we kinda want to catch emails that are weirdly formatted:
        A@b@c@example.com
        a"b(c)d,e:f;g<h>i[j\\k]l@example.com
        just"not"right@example.com
        """
        
        results = find_pattern_matches(text, pattern_type="email")
        
        # Should match 15 emails results
        assert len(results) == 15
        
        # Check specific matches
        matched_values = [r["match"] for r in results]
        assert "user@example.com" in matched_values
        assert "first.last@example.co.uk" in matched_values
        assert "user+tag@example.org" in matched_values
        assert "user.name@subdomain.example.com" in matched_values
        assert "example@s.example" in matched_values  # Valid with 1-char subdomain
        
        # Edge case emails
        assert "x@example.com" in matched_values  # Single-letter local part
        
        # Check pattern characteristics for all matches
        for email in matched_values:
            assert "@" in email
            assert "." in email
            assert email.count("@") == 1
    
    def test_find_date_matches(self):
        # Test date pattern matching
        text = """
        Valid dates:
        2023-01-15
        01/15/2023
        15/01/2023
        Jan 15, 2023
        January 15 2023
        15 Jan 2023
        2023-12-31
        12/31/2023
        01-30-2023
        2023-01-01
        Feb 29, 2024
        February 28 2023
        
        Invalid dates:
        2023-13-15  # invalid month
        01/32/2023  # invalid day
        not-a-date
        Feb 30, 2023  # Invalid date (no Feb 30)
        13/01/2023  # invalid month or international format
        00/00/0000
        """
        
        results = find_pattern_matches(text, pattern_type="date")
        
        # Should match all syntactically valid dates (not checking semantic validity)
        assert len(results) >= 12
        
        # Check specific matches
        matched_values = [r["match"] for r in results]
        assert "2023-01-15" in matched_values
        assert "01/15/2023" in matched_values
        assert "15/01/2023" in matched_values
        assert "Jan 15, 2023" in matched_values
        assert "January 15 2023" in matched_values
        assert "15 Jan 2023" in matched_values
    
    def test_find_url_matches(self):
        # Test URL pattern matching
        text = """
        Valid URLs:
        https://example.com
        http://example.org/path
        https://subdomain.example.co.uk/path?query=value
        http://example.com:8080
        www.example.com
        https://example.com/path/to/page.html
        https://api.example.org/v1/users?id=123&format=json
        www.example.org/products#featured
        
        Invalid URLs:
        example.com
        https://
        http:/example.com  # missing slash
        http:example.com
        not-a-url
        ftp://example.com  # different protocol
        //example.com
        """
        
        results = find_pattern_matches(text, pattern_type="url")
        
        # Our pattern only matches URLs starting with http://, https://, or www.
        expected_count = 8
        assert len(results) == expected_count
        
        # Check specific matches
        matched_values = [r["match"] for r in results]
        assert "https://example.com" in matched_values
        assert "http://example.org/path" in matched_values
        assert "https://subdomain.example.co.uk/path?query=value" in matched_values
        assert "http://example.com:8080" in matched_values
        assert "www.example.com" in matched_values
        
        # All matches should start with http://, https://, or www.
        for url in matched_values:
            assert url.startswith(("http://", "https://", "www."))
            
    def test_find_ip_address_matches(self):
        # Test IP address pattern matching
        text = """
        Valid IPv4 addresses:
        192.168.1.1
        10.0.0.1
        255.255.255.255
        0.0.0.0
        127.0.0.1
        
        Valid IPv6 addresses:
        2001:0db8:85a3:0000:0000:8a2e:0370:7334
        2001:db8:85a3:0:0:8a2e:370:7334
        ::1
        ::
        2001:db8::
        
        Invalid IP addresses:
        192.168.1  # missing octet
        192.168.1.256  # octet out of range
        192.168.1.1.1  # too many octets
        not-an-ip
        2001:db8:::1  # invalid IPv6
        :::1  # invalid IPv6
        """
        
        results = find_pattern_matches(text, pattern_type="ip")
        
        # Should match valid IPv4 addresses at minimum
        assert len(results) >= 5
        
        # Check specific IPv4 matches
        matched_values = [r["match"] for r in results]
        assert "192.168.1.1" in matched_values
        assert "10.0.0.1" in matched_values
        assert "255.255.255.255" in matched_values
        assert "0.0.0.0" in matched_values
        assert "127.0.0.1" in matched_values
    
    def test_find_pattern_matches_multiple_types(self):
        test_text = """
        User email: user@example.com
        Order ID: 550e8400-e29b-41d4-a716-446655440000
        Date: 2023-01-15
        Website: https://example.com
        Server IP: 192.168.1.1
        """
        
        # Test with multiple pattern types
        multi_matches = find_pattern_matches(
            test_text, pattern_type=["email", "url", "ip"]
        )
        assert len(multi_matches) == 3
        
        # Check that we found one of each expected type
        types = [m["type"] for m in multi_matches]
        assert "email" in types
        assert "url" in types
        assert "ip" in types
        
        # Check specific matches
        assert any(m["type"] == "email" and m["match"] == "user@example.com" for m in multi_matches)
        assert any(m["type"] == "url" and m["match"] == "https://example.com" for m in multi_matches)
        assert any(m["type"] == "ip" and m["match"] == "192.168.1.1" for m in multi_matches)
    
    def test_line_numbers(self):
        # Test line number tracking
        text = """Line 1: nothing here
        Line 2: email@example.com
        Line 3: nothing here
        Line 4: https://example.com
        Line 5: nothing here"""
        
        results = find_pattern_matches(text, pattern_type=["email", "url"])
        
        # Check line numbers
        assert len(results) == 2
        assert any(r["type"] == "email" and r["line"] == 2 for r in results)
        assert any(r["type"] == "url" and r["line"] == 4 for r in results)
    
    def test_pattern_in_context(self):
        # Test patterns within surrounding text
        text = """This is an email: contact@example.com embedded in text.
                The order ID is 550e8400-e29b-41d4-a716-446655440000 which needs processing.
                Please visit our website at https://example.com for more information.
                Our server (192.168.1.1) needs to be updated by 2023-12-31."""
        
        results = find_pattern_matches(
            text, pattern_type=["email", "guid", "url", "ip", "date"]
        )
        
        # Should find all 5 patterns
        assert len(results) == 5
        
        # Check all pattern types were found
        pattern_types = {r["type"] for r in results}
        assert pattern_types == {"email", "guid", "url", "ip", "date"}
        
        # Check specific matches
        assert any(r["match"] == "contact@example.com" for r in results)
        assert any(r["match"] == "550e8400-e29b-41d4-a716-446655440000" for r in results)
        assert any(r["match"] == "https://example.com" for r in results)
        assert any(r["match"] == "192.168.1.1" for r in results)
        assert any(r["match"] == "2023-12-31" for r in results)
        
    def test_multiple_matches_per_line(self):
        # Test finding multiple matches in a single line
        text = "Multiple emails: first@example.com, second@example.com, third@example.com"
        
        results = find_pattern_matches(text, pattern_type="email")
        
        # Should find all 3 emails
        assert len(results) == 3
        assert "first@example.com" in [r["match"] for r in results]
        assert "second@example.com" in [r["match"] for r in results]
        assert "third@example.com" in [r["match"] for r in results]
    
    def test_pattern_at_line_boundaries(self):
        # Test patterns at the start and end of lines
        text = """
        https://start.example.com is at the start
        The end has user@example.com
        192.168.1.1
        www.example.com/path
        end@example.com"""
        
        results = find_pattern_matches(
            text, pattern_type=["url", "email", "ip"]
        )
        
        # Should find all 5 patterns
        assert len(results) == 5
        
        # Check specific matches including standalone patterns
        matched_values = [r["match"] for r in results]
        assert "https://start.example.com" in matched_values
        assert "user@example.com" in matched_values
        assert "192.168.1.1" in matched_values
        assert "www.example.com/path" in matched_values
        assert "end@example.com" in matched_values
    
    def test_empty_input(self):
        # Test with empty input
        text = ""
        
        results = find_pattern_matches(text, pattern_type="email")
        
        # Should find no matches
        assert len(results) == 0
    
    def test_no_matches(self):
        # Test with no matches
        text = "This text contains no patterns that we're looking for."
        
        results = find_pattern_matches(
            text, pattern_type=["email", "guid", "url", "ip", "date"]
        )
        
        # Should find no matches
        assert len(results) == 0
        
    def test_invalid_pattern_type(self):
        # Test with invalid pattern type
        text = "Some text"
        
        with pytest.raises(ValueError):
            find_pattern_matches(text, pattern_type="invalid_pattern")
            
    def test_text_search(self):
        """Test searching for regular text"""
        text = """
        This is a sample text with some keywords.
        We want to find the word 'python' in this text.
        Python is case-insensitive by default.
        We also want to match 'Python3' as a partial word.
        """
        
        # Test case-insensitive search
        results = find_pattern_matches(
            text, 
            pattern_type="text",
            text_pattern="python",
            case_sensitive=False
        )
        
        # Should find 3 matches: 'python' and 'Python' * 2
        assert len(results) == 3
        assert all(r["type"] == "text" for r in results)
        
        # Test whole word search
        results = find_pattern_matches(
            text, 
            pattern_type="text",
            text_pattern="python",
            case_sensitive=False,
            whole_word=True
        )
        
        # Should only find the standalone 'python' and 'Python', not 'Python3'
        assert len(results) == 2
        
        # Test case-sensitive search
        results = find_pattern_matches(
            text, 
            pattern_type="text",
            text_pattern="python",
            case_sensitive=True
        )
        
        # Should only find 'python', not 'Python'
        assert len(results) == 1        
    