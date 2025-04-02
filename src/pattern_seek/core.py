import os
import glob
from typing import Dict, List, Union, Optional

from pattern_seek.patterns import find_pattern_matches

def search_file(
    file_path: str,
    pattern_type: Union[str, List[str]],
    context_lines: int = 0
) -> List[Dict]:
    """
    Search a file for patterns of the specified type(s).
    
    Args:
        file_path: Path to the file to search
        pattern_type: Type(s) of patterns to search for
        context_lines: Number of lines to include before and after each match
        
    Returns:
        A list of dictionaries containing information about each match
    """
    
    # python encodings: https://docs.python.org/3.8/library/codecs.html#standard-encodings
    # utf-8 is the most lenient/common encoding and should read the file
    # if it fails, allow the error to propagate
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # find pattern matches
    matches = find_pattern_matches(content, pattern_type)
    
    # Add context if requested
    if context_lines > 0:
        lines = content.splitlines()
        for match in matches:
            line_idx = match["line"] - 1  # Convert to zero-based index
            
            # Get context before the match
            start_idx = max(0, line_idx - context_lines)
            match["context_before"] = lines[start_idx:line_idx]
            
            # Get context after the match
            end_idx = min(len(lines), line_idx + context_lines + 1)
            match["context_after"] = lines[line_idx + 1:end_idx]
    
    return matches

def search_files(
    path: Union[str, List[str]],
    pattern_type: Union[str, List[str]],
    context_lines: int = 0
) -> List[Dict]:
    """
    Search multiple files or directories for patterns of the specified type(s).
    
    Args:
        path: File path, directory path, wildcard pattern, or list of paths
        pattern_type: Type(s) of patterns to search for
        context_lines: Number of lines to include before and after each match
        
    Returns:
        A list of dictionaries, one per file, containing file path and matches
    """
    
    # Handle single path
    if isinstance(path, str):
        # Check if the path is a directory
        if os.path.isdir(path):
            # Search all files in the directory
            file_paths = [
                os.path.join(path, f) for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))
            ]
        # Check if the path contains wildcards
        elif any(c in path for c in ['*', '?', '[']):
            # Expand wildcards
            file_paths = glob.glob(path)
        # Single file
        elif os.path.isfile(path):
            file_paths = [path]
        else:
            raise ValueError(f"Path not found: {path}")
    # Handle list of paths
    else:
        file_paths = path
        
    # Process each file
    results = []
    for file_path in file_paths:
        if os.path.isfile(file_path):
            try:
                matches = search_file(file_path, pattern_type, context_lines)
                results.append({
                    "file": file_path,
                    "matches": matches
                })
            except Exception as e:
                # Skip files that can't be processed
                results.append({
                    "file": file_path,
                    "error": str(e)
                })
    
    return results

