# NYC Zoning Timeline

The Python script extracts titles and last amended dates from multiple PDF files.

## Features

- Processes multiple PDF files in a batch (Article01.pdf to Article14.pdf)
- Extracts titles and last amended dates using regular expressions
- Identifies font information (StoneSansBold or not). This can be used for validation
- Provides page numbers for each extracted title
- Generates two output files: one for results and one for debugging information

## Requirements

- Python 3.6+
- pdfplumber library

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.
2. Install the required library using pip:

   ```
   pip install pdfplumber
   ```

3. Download the `extract.py` script to your local machine.

## Usage

1. Place the `extract.py` script in the same directory as your PDF files (Article01.pdf through Article14.pdf).

2. Open a terminal or command prompt and navigate to the directory containing the script and PDF files.

3. Run the script using Python:

   ```
   python pdf_title_extractor.py
   ```

4. The script will process all available PDF files from Article01.pdf to Article14.pdf. It will skip any files that are not found.

5. After processing, check the following output files:
   - `all_outputs.txt`: Contains the extracted titles and dates from all PDFs.
   - `all_debug_outputs.txt`: Contains debugging information for all PDFs.

## Output Format

The `all_outputs.txt` file will contain entries in the following format:

```
Results for Article01.pdf:
123-456 - EXAMPLE TITLE
LAST AMENDED 01/01/2024
Found on page 1
Font: StoneSansBold

Results for Article02.pdf:
...
```

The `all_debug_outputs.txt` file will contain more detailed information about each extraction, including cases where titles were found without dates.

## Customization

- To process a different range of PDF files, modify the `start_num` and `end_num` variables in the script.
- The regular expression pattern for title and date extraction can be adjusted in the `extract_titles_and_dates()` function if needed.

## Troubleshooting

- If you encounter any "File not found" messages, ensure that all expected PDF files are present in the same directory as the script.
- Note that when you download the files from the NY Zoning Code website, the files are numbered with Roman numerals. They'll need to be renumbered before using this script.
- For any issues related to PDF reading, make sure you have the latest version of the pdfplumber library installed.

## License

This script is provided "as is", without warranty of any kind. You are free to modify and distribute it as needed.

## Contributing

Contributions to improve the script are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.
