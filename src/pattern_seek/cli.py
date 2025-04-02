import os
import sys
import click
from typing import List, Optional

from pattern_seek.core import search_files
from pattern_seek.output import print_matches

@click.command()
@click.argument('paths', nargs=-1, required=True)
@click.option(
    '--pattern', '-p', 
    type=click.Choice(['email', 'guid', 'date', 'url', 'ip', 'all']),
    multiple=True,
    default=['all'],
    help='Pattern types to search for'
)
@click.option(
    '--context', '-c',
    type=int,
    default=0,
    help='Number of context lines to include before and after matches'
)
@click.option(
    '--no-color',
    is_flag=True,
    help='Disable colored output'
)
def main(
    paths: List[str],
    pattern: List[str],
    context: int,
    no_color: bool
) -> None:
    """
    Pattern-seek: Search text files for specific patterns.
    
    PATHS: One or more files or directories to search.
    Wildcards are supported, e.g., *.txt
    """
    
     # Determine which patterns to search for
    if 'all' in pattern:
        pattern_types = ['email', 'guid', 'date', 'url', 'ip']
    else:
        pattern_types = list(pattern)
        
    # Process each path
    all_results = []
    for path in paths:
        click.echo(f"Processing {path}...")
        try:
            results = search_files(path, pattern_types, context)
            all_results.extend(results)
        except Exception as e:
            click.echo(f"Error processing {path}: {str(e)}", err=True)
            
    # Print results
    if all_results:
        print_matches(all_results, colored=not no_color, include_file_info=True)
    else:
        click.echo("No matches found.")
        
    # Return non-zero exit code if no matches were found
    has_matches = any(
        len(result.get("matches", [])) > 0 
        for result in all_results
    )
    if not has_matches:
        sys.exit(1)
        
if __name__ == "__main__":
    main()