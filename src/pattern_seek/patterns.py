import re
from typing import Dict, List, Union, Optional
from pattern_seek.regex_patterns import GUID_PATTERN, EMAIL_PATTERN, DATE_PATTERN, URL_PATTERN, IPV4_PATTERN, IPV6_PATTERN

# pattern type mapping
PATTERN_MAP = {
    "guid": GUID_PATTERN,
    "email": EMAIL_PATTERN,
    "date": DATE_PATTERN,
    "url": URL_PATTERN,
    "ip": f"({IPV4_PATTERN}|{IPV6_PATTERN})"
    # add text patterns dynamically
}

# Pre-compile patterns for potential small performance gains
# Resources:
    # https://www.theserverside.com/tip/The-benefits-of-using-compiled-regex-in-Python-and-Java
    # https://stackoverflow.com/questions/452104/is-it-worth-using-pythons-re-compile
    # https://pynative.com/python-regex-compile/
    # 
COMPILED_PATTERNS = {
    pattern_type: re.compile(pattern) 
    for pattern_type, pattern in PATTERN_MAP.items()
}

def find_pattern_matches(
    text: str, 
    pattern_type: Union[str, List[str]],
    line_numbers: bool = True,
    text_pattern: Optional[str] = None,
    case_sensitive: bool = False,
    whole_word: bool = False
) -> List[Dict]:
    """
    Find all matches of the specified pattern type(s) in the text.
    
    Args:
        text: The text to search in
        pattern_type: Either a string or a list of strings specifying the pattern types to search for
        line_numbers: Whether to include line numbers in the results
        text_pattern: Optional text to search for (for regular text search)
        case_sensitive: Whether text search should be case-sensitive
        whole_word: Whether to match whole words only for text search
        
    Returns:
        A list of dictionaries containing information about each match:
        {
            "type": pattern type (e.g., "email"),
            "match": the matched text,
            "line": line number (if line_numbers is True),
            "start": start index of the match in the line,
            "end": end index of the match in the line
        }
    """
    results = []
    
    # Convert single pattern type to list
    if isinstance(pattern_type, str):
        pattern_type = [pattern_type]
        
    # if text search is requested, create a pattern for it
    if "text" in pattern_type and text_pattern:
        if whole_word:
            text_search_pattern = fr'\b{re.escape(text_pattern)}\b'
        else:
            text_search_pattern = re.escape(text_pattern)
            
        # Compile with appropriate flags
        flags = 0 if case_sensitive else re.IGNORECASE
        COMPILED_PATTERNS["text"] = re.compile(text_search_pattern, flags)
    elif "text" in pattern_type and not text_pattern:
        raise ValueError("Text pattern must be provided when searching for 'text'")
        
        
    # Validate pattern types
     # Validate pattern types
    for pt in pattern_type:
        if pt not in COMPILED_PATTERNS and pt != "text":
            raise ValueError(f"Unknown pattern type: {pt}")
        if pt == "text" and pt not in COMPILED_PATTERNS:
            raise ValueError("Text pattern must be provided when searching for 'text'")
    
    # Process text line by line
    lines = text.splitlines()
    for line_idx, line in enumerate(lines):
        for pt in pattern_type:
            for match in COMPILED_PATTERNS[pt].finditer(line):
                result = {
                    "type": pt,
                    "match": match.group(0),
                    "start": match.start(),
                    "end": match.end(),
                }
                if line_numbers:
                    result["line"] = line_idx + 1
                    
                results.append(result)
                
    return results
