<h1 align="center">
  <br>
  <a href="https://github.com/jspenaq/Kratio"><img src="Kratio Logo.jpg" alt="Kratio" width="200"></a>
  <br>
  Kratio
  <br>
</h1>

<h4 align="center">A powerful keyword density analyzer for content optimization</h4>

<p align="center">
  <a href="#about">About</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#examples">Examples</a> •
  <a href="#output-formats">Output Formats</a> •
  <a href="#development">Development</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

## About

Kratio is a sophisticated keyword density analyzer that helps content creators, SEO specialists, and marketers optimize their content. It analyzes text files to identify the most frequently used words and noun phrases, providing valuable insights for content optimization and SEO strategy.

## Key Features

* **Comprehensive Analysis**: Analyzes text files to compute word frequencies and keyword density
* **Multiple Analysis Types**:
  * Word-based analysis - identifies individual keywords and their frequency
  * Noun chunk analysis - identifies phrases and compound terms
* **Visualization**: Generates bar chart visualizations of top keywords/noun chunks
* **Multiple Output Formats**: Supports table, CSV, and JSON output formats
* **Batch Processing**: Analyze multiple files in a directory at once
* **File Format Support**: Works with various text-based file formats (.txt, .md, .py, .html, .js)
* **Watch Mode**: Monitor files or directories and automatically re-analyze on changes
* **Offline-First**: No internet connection required for core functionality (except for initial spaCy model download)

## Installation

To run Kratio, you'll need [Python 3.12+](https://www.python.org/downloads/) installed on your computer.

```bash
# Clone the repository
git clone https://github.com/jspenaq/Kratio.git
cd Kratio

# Install dependencies using uv (recommended)
pip install uv
uv sync
uv pip install -e .

# Download the required spaCy model
uv run python -m spacy download en_core_web_sm
```

Alternatively, you can install using pip directly:

```bash
# Clone the repository
git clone https://github.com/jspenaq/Kratio.git
cd Kratio

# Install the package and dependencies
pip install -e .

# Download the required spaCy model
python -m spacy download en_core_web_sm
```

## Usage

Kratio can be used as a command-line tool:

```bash
# Basic usage
kratio <file_path> [options]

# Analyze a directory
kratio <directory_path> [options]
```

### Command-line Options

```
positional arguments:
  path                  The path to the text file or directory to analyze.

options:
  -h, --help            show this help message and exit
  --analysis_type {words,noun_chunks}
                        The type of analysis to perform (words or noun_chunks, default: words).
  --top_n TOP_N         The number of top keywords/noun chunks to display (default: 10).
  --output OUTPUT       Output file path to dump the DataFrame (CSV or JSON format).
  --save-plot SAVE_PLOT
                        Path to save the visualization plot (e.g., path.png).
  --no-visualization    Disable visualization output.
  --format {json,csv,table}
                        Output format for the analysis results (json, csv, or table, default: table).
  --silent              Suppress all non-essential output, including logging messages.
  --watch               Monitor the file or directory and re-run analysis on every change.
  --debug               Enable debug logging for troubleshooting.
```

## Examples

### Analyze a single file for word frequency

```bash
kratio example.txt --analysis_type words
```

### Analyze a file for noun chunks and display top 20 results

```bash
kratio example.txt --analysis_type noun_chunks --top_n 20
```

### Analyze a file and save results to CSV

```bash
kratio example.txt --output results.csv
```

### Analyze a file and save visualization

```bash
kratio example.txt --save-plot keyword_density.png
```

### Analyze a directory of files

```bash
kratio ./content/ --analysis_type words
```

### Output results in JSON format

```bash
kratio example.txt --format json
```

### Watch a file for changes and re-analyze automatically

```bash
kratio example.txt --watch
```

### Watch with debug logging enabled

```bash
kratio example.txt --watch --debug
```

### Watch a directory for changes

```bash
kratio ./content/ --watch
```

## Output Formats

Kratio supports multiple output formats:

1. **Table** (default): Displays results in a formatted table in the terminal
2. **CSV**: Exports results to a CSV file for spreadsheet analysis
3. **JSON**: Exports results to a JSON file for programmatic use

## Development

### Project Structure

```
kratio/
├── docs/                 # Documentation
├── src/                  # Source code
│   └── kratio/
│       ├── cli/          # Command-line interface
│       ├── core/         # Core analysis functionality
│       ├── io/           # Input/output operations
│       ├── utils/        # Utility functions
│       └── visualization/ # Visualization components
└── tests/                # Test suite
    ├── integration/      # Integration tests
    └── unit/             # Unit tests
```

### Running Tests

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests with coverage
coverage run -m pytest
coverage report
coverage html  # Generates HTML report
```

## Roadmap

Kratio is actively being developed with several exciting features planned:

1. **Competitive Analysis Module**: Compare keyword densities across multiple documents
2. **SEO Optimization Integration**: Connect with SEO APIs for actionable insights
3. **Content Quality Assessment**: Add readability scoring and writing quality analysis
4. **Multi-language Support**: Expand analysis capabilities to multiple languages
5. **Interactive Web Interface**: Create a user-friendly web interface

See [Feature Enhancement Ideas](docs/feature_enhancement_ideas.md) for more details on upcoming features.

## Credits

This software uses the following open source packages:

- [spaCy](https://spacy.io/) - Industrial-strength Natural Language Processing
- [pandas](https://pandas.pydata.org/) - Data analysis and manipulation tool
- [Seaborn](https://seaborn.pydata.org/) - Statistical data visualization
- [Matplotlib](https://matplotlib.org/) - Comprehensive library for creating visualizations
- [Loguru](https://github.com/Delgan/loguru) - Python logging made simple
- [Tabulate](https://github.com/astanin/python-tabulate) - Pretty-print tabular data
- [Watchdog](https://github.com/gorakhargosh/watchdog) - API and shell utilities to monitor file system events

## License

[MIT License](LICENSE)

---

> [github.com/jspenaq](https://github.com/jspenaq) &nbsp;&middot;&nbsp;
> LinkedIn [@jspenaq](https://www.linkedin.com/in/juan-sebastian-pe%C3%B1a-quintero/)