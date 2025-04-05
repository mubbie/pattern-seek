import os
import sys
import click
from typing import List, Optional

from pattern_seek.core import search_files
from pattern_seek.output import print_matches
from pattern_seek.transform import (
    transform_csv, 
    print_csv_matches, 
    save_csv_matches
)

@click.command()
@click.argument('paths', nargs=-1, required=True)
@click.option(
    '--pattern', '-p', 
    type=click.Choice(['email', 'guid', 'date', 'url', 'ip', 'text', 'all']),
    multiple=True,
    default=['all'],
    help='Pattern types to search for'
)
@click.option(
    '--text', '-t',
    type=str,
    help='Text pattern to search for when using the "text" pattern type'
)
@click.option(
    '--case-sensitive', '-c',
    is_flag=True,
    help='Make text search case-sensitive'
)
@click.option(
    '--whole-word', '-w',
    is_flag=True,
    help='Match whole words only for text search'
)
@click.option(
    '--context', '-C',
    type=int,
    default=0,
    help='Number of context lines to include before and after matches'
)
@click.option(
    '--no-color',
    is_flag=True,
    help='Disable colored output'
)
@click.option(
    '--transform', '-TT',
    type=click.Choice(['csv',]),
    help='Transform structured file formats (e.g., CSV) based on query'
)
@click.option(
    '--query', '-q',
    type=str,
    help='Search query for transform mode'
)
@click.option(
    '--column', '-col',
    type=str,
    help='Column name to search in for transform mode'
)
@click.option(
    '--matchword', '-m',
    is_flag=True,
    help='Match whole words only for transform mode'
)
@click.option(
    '--save', '-s',
    is_flag=True,
    help='Save transformed results to a new file'
)
def main(
    paths: List[str],
    pattern: List[str],
    text: Optional[str],
    case_sensitive: bool,
    whole_word: bool,
    context: int,
    no_color: bool,
    transform: Optional[str],
    query: Optional[str],
    column: Optional[str],
    matchword: bool,
    save: bool
) -> None:
    """
    Pattern-seek: Search text files for specific patterns.
    
    PATHS: One or more files or directories to search.
    Wildcards are supported, e.g., *.txt
    """

    # Handle --transform option
    if transform == 'csv':
        if not query:
            click.echo("Error: --query must be provided when using --transform csv", err=True)
            sys.exit(1)

        for path in paths:
            try:
                result = transform_csv(
                    path,
                    query=query,
                    column=column,
                    case_sensitive=case_sensitive,
                    matchword=matchword,
                    save=save
                )
                
                if not save:
                    print_csv_matches(result)

            except Exception as e:
                click.echo(f"Error transforming {path}: {str(e)}", err=True)

        return # Skip the rest of the pattern-based logic
    
    # Determine which patterns to search for
    if 'all' in pattern:
        pattern_types = ['email', 'guid', 'date', 'url', 'ip']
    else:
        pattern_types = list(pattern)
        
    # Check if text search is required but no pattern provided
    if 'text' in pattern_types and not text:
        click.echo("Error: Text pattern must be provided when searching for 'text' pattern type.", err=True)
        sys.exit(1)
        
    # Process each path
    all_results = []
    fall_results = []
    for path in paths:
        try:
            results = search_files(
                path, 
                pattern_types, 
                context_lines=context,
                text_pattern=text,
                case_sensitive=case_sensitive,
                whole_word=whole_word
            )
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