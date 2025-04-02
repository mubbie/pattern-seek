import sys
from typing import Dict, List, TextIO, Optional, Union
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

# Color mapping for different pattern types
COLOR_MAP = {
    "email": Fore.BLUE,
    "guid": Fore.GREEN,
    "date": Fore.YELLOW,
    "url": Fore.MAGENTA,
    "ip": Fore.CYAN,
    "default": Fore.WHITE
}

def format_matches(
    matches: Union[List[Dict], List[Dict[str, Union[str, List[Dict]]]]],
    colored: bool = True,
    include_file_info: bool = False
) -> str:
    result = []
    
    # Check if we're dealing with file matches
    if include_file_info:
        for file_entry in matches:
            file_path = file_entry["file"]
            result.append(f"\n{Fore.WHITE}{Style.BRIGHT}File: {file_path}{Style.RESET_ALL}")
            
            if "error" in file_entry:
                result.append(f"  {Fore.RED}Error: {file_entry['error']}{Style.RESET_ALL}")
                continue
                
            file_matches = file_entry["matches"]
            if not file_matches:
                result.append(f"  {Fore.YELLOW}No matches found{Style.RESET_ALL}")
                continue
                
            # Format matches for this file
            file_result = format_matches(file_matches, colored, include_file_info=False)
            
            # Indent all lines
            indented = "\n".join(f"  {line}" for line in file_result.splitlines())
            result.append(indented)
    else:
        # Format individual matches
        for match in matches:
            # Get match color based on type
            color = COLOR_MAP.get(match["type"], COLOR_MAP["default"]) if colored else ""
            reset = Style.RESET_ALL if colored else ""
            
            # Add context before match if available
            if "context_before" in match:
                for i, line in enumerate(match["context_before"]):
                    context_line_num = match["line"] - len(match["context_before"]) + i
                    result.append(f"Line {context_line_num}: {line}")
            
            # Get the full line if available
            line_num = match["line"]
            match_text = match["match"]
            line_content = None
            
            # If we have context information, try to extract the original line
            if "context_before" in match or "context_after" in match:
                all_context_lines = []
                if "context_before" in match:
                    all_context_lines.extend(match["context_before"])
                
                # The current line should be at this position
                current_line_idx = len(match.get("context_before", []))
                if "context_line" in match:
                    # Use the stored context line if available
                    line_content = match["context_line"]
                else:
                    # Try to find the match in context lines
                    for i, line in enumerate(all_context_lines):
                        if match_text in line:
                            line_content = line
                            break
            
            # If we couldn't find the original line, just use the match text
            if line_content is None:
                line_content = match_text
            
            # Highlight the match in the line
            start = line_content.find(match_text)
            if start >= 0:
                end = start + len(match_text)
                highlighted = (
                    line_content[:start] + 
                    f"{color}{Style.BRIGHT}{match_text}{reset}" + 
                    line_content[end:]
                )
                result.append(f"Line {line_num}: {highlighted}")
            else:
                # If we can't find the match in the line, just show the line
                result.append(f"Line {line_num}: {line_content}")
            
            # Add context after match if available
            if "context_after" in match:
                for i, line in enumerate(match["context_after"]):
                    context_line_num = match["line"] + i + 1
                    result.append(f"Line {context_line_num}: {line}")
                    
            # Add a separator between matches
            result.append("")
    
    return "\n".join(result)

def print_matches(
    matches: Union[List[Dict], List[Dict[str, Union[str, List[Dict]]]]],
    colored: bool = True,
    include_file_info: bool = False,
    output: TextIO = sys.stdout
) -> None:
    """
    Print formatted search matches to the specified output.
    
    Args:
        matches: List of match dictionaries, or list of file match dictionaries
        colored: Whether to use ANSI color codes in the output
        include_file_info: Whether matches include file information
        output: Output stream to print to (default: sys.stdout)
    """
    
    formatted = format_matches(matches, colored, include_file_info)
    print(formatted, file=output)