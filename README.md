<h1 align="center">
  <br>
  <a href="https://github.com/jspenaq/Kratio"><img src="Kratio Logo.jpg" alt="Kratio" width="200"></a>
  <br>
  Kratio
  <br>
</h1>

<h4 align="center">A keyword density analyzer for local files.</h4>


<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

## Key Features

*   Analyzes local files to compute word frequencies and keyword density.
*   Identifies common keywords and visualizes keyword distribution.
*   Provides both word-based and noun chunk-based analysis.
*   Generates bar chart visualizations of top keywords/noun chunks.
*   Offline-first application (no internet connection required for core functionality).

## How To Use

To run this application, you'll need [Python 3.12](https://www.python.org/downloads/) installed on your computer. You'll also need to install the required libraries:

```bash
# Clone the repository
git clone https://github.com/jspenaq/Kratio.git
cd Kratio

# Install dependencies
pip install uv
uv sync
uv pip install pip
uv run spacy download en_core_web_sm
```

From your command line:

```bash
# Run the app
uv run src/kratio/main.py <file_path> --analysis_type <words|sentences> --top_n <number_of_keywords>
```

For example:

```bash
uv run src/kratio/main.py example.txt --analysis_type words
uv run src/kratio/main.py example.txt --analysis_type sentences --top_n 20
```

## Credits

This software uses the following open source packages:

- [spaCy](https://spacy.io/)
- [pandas](https://pandas.pydata.org/)
- [Seaborn](https://seaborn.pydata.org/)

## License

[MIT License](LICENSE)