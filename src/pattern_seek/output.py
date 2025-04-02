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
    """
    Format search matches as a string.
    
    Args:
        matches: List of match dictionaries, or list of file match dictionaries
        colored: Whether to use ANSI color codes in the output
        include_file_info: Whether matches include file information
        
    Returns:
        Formatted string representation of the matches
    """
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
            
            # Add the match line
            line_num = match["line"]
            match_text = match["match"]
            
            # Get the full line if available
            if "context_before" in match or "context_after" in match:
                # The line must be one of the context lines
                all_lines = []
                if "context_before" in match:
                    all_lines.extend(match["context_before"])
                if "context_after" in match:
                    all_lines.extend(match["context_after"])
                    
                # We need to find the line that contains the match
                for line in all_lines:
                    if match_text in line:
                        full_line = line
                        break
                else:
                    # If not found, just use the match itself
                    full_line = match_text
            else:
                full_line = match_text
            
            # Highlight the match in the line
            start = full_line.find(match_text)
            if start >= 0:
                end = start + len(match_text)
                highlighted = (
                    full_line[:start] + 
                    f"{color}{Style.BRIGHT}{match_text}{reset}" + 
                    full_line[end:]
                )
                result.append(f"Line {line_num}: {highlighted}")
            else:
                # If we can't find the match in the line, just show the match
                result.append(f"Line {line_num}: {color}{Style.BRIGHT}{match_text}{reset}")
            
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