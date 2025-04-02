# Pattern-Seek

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line utility for searching text files using pattern recognition. Pattern-Seek helps you find specific types of data like emails, GUIDs, dates, URLs, and IP addresses within your files.

As the project evolves, I'll add more features, improve the code, tests, and documentation.

Currently, it only supports plain text files/files that can be encoded in UTF-8. Other formats are currently not supported, and feedback on how to support is much welcome.

## Features

- **Pattern-based search**: Find various data types using regex patterns
  - GUID/UUID
  - Email addresses
  - Dates (multiple formats)
  - URLs
  - IP addresses (IPv4 and IPv6)
- **Regular text search**: Find any text string with customizable options
  - Case-sensitive matching
  - Whole word matching
- **Multi-file/directory search**: Search across individual files, multiple files, directories, or with wildcards
- **Context display**: Show surrounding lines for each match
- **Colored output**: Highlight matches with color coding
- **Flexible CLI**: User-friendly command-line interface

## Installation

### Prerequisites

- Python 3.8 or higher

### Install from source

```bash
# Clone the repository
git clone https://github.com/mubbie/pattern-seek.git
cd pattern-seek

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

```bash
# Basic usage: search all supported patterns in a file
pattern-seek filename.txt

# Search for specific pattern types
pattern-seek --pattern email --pattern url filename.txt

# Search for regular text
pattern-seek --pattern text --text "def" *.py

# Case-sensitive text search
pattern-seek --pattern text --text "Class" --case-sensitive src/*.py

# Whole word text search
pattern-seek --pattern text --text "import" --whole-word *.py

# Search with context lines
pattern-seek --pattern email --context 2 filename.txt

# Search multiple files
pattern-seek file1.txt file2.txt

# Search all Python files in current directory
pattern-seek *.py

# Search recursively in a directory
pattern-seek /path/to/directory/

# Show help
pattern-seek --help
```

### Command-line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--pattern` | `-p` | Pattern types to search for: email, guid, date, url, ip, text, all (default) |
| `--text` | `-t` | Text pattern to search for when using the "text" pattern type |
| `--case-sensitive` | `-c` | Make text search case-sensitive |
| `--whole-word` | `-w` | Match whole words only for text search |
| `--context` | `-C` | Number of context lines to include before and after matches |
| `--no-color` |  | Disable colored output |
| `--help` | `-h` | Show help message |

### Examples

#### Finding emails in a log file with context

```bash
pattern-seek --pattern email --context 2 application.log
```

#### Searching for GUIDs and IPs in all Python files

```bash
pattern-seek --pattern guid --pattern ip *.py
```

#### Searching for specific text in Python files

```bash
pattern-seek --pattern text --text "def main" *.py
```

#### Searching for whole words with case sensitivity

```bash
pattern-seek --pattern text --text "Class" --case-sensitive --whole-word src/*.py
```

#### Searching in a directory with multiple pattern types

```bash
pattern-seek --pattern url --pattern date /path/to/project/
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=pattern_seek
```

## License

MIT

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

### Development Plan

You can see the development plan and features planned for future versions in the [plan.md](planning/plan.md) file.

### Change Log

Each version has its own dedicated change log file. You can see the change log for the latest version in the [change-log/v0.1.0.md](./change-log/v0.1.0.md) file.

## Feedback

I'd love to hear from you! Please open an issue, submit a pull request, or contact me directly at [midoko.dev@gmail.com](mailto:midoko.dev@gmail.com).
