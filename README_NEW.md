# Data Visualization and Reporting Pipeline

This project streamlines the process of converting, analyzing, and generating reports for datasets in XML, Excel, or CSV formats. It offers an automated and modular reporting workflow that supports multiple input types, structured outputs, and configurable behavior using `.env` and `report_config.json` files.

---

## Features

### Auto File Conversion

* Automatically converts `.xml`, `.xls`, and `.xlsx` files to CSV.
* Each Excel tab is exported as an individual CSV.
* Cleaned and structured CSVs are stored in the `data_csv/` directory.

### Modular Report Generation

* Uses a configuration-driven approach via `report_config.json`.
* Supported modules:

  * **coverpage**: Title, metadata, and logo.
  * **summary**: Dataset overview.
  * **barcharts**: Charts showing distribution of unique values.
  * **basicDataAnalysis**: Column profiling and cleanup.
* Fully extensible for future modules with minimal code changes.

### Optional Unique Values Report

* Generates a PDF showing unique values per column across one or more CSV files.
* Columns specified via `.env` using `UNIQUE_VALUE_COLUMNS`.

### Configurable via Environment Variables and JSON

* `.env` holds paths and defaults.
* `report_config.json` holds report module configurations.

---

## Project Structure

```
data-visualization/
├── assets/                  # Static assets for reports
│   ├── styles.css                # Stylesheet for PDF reports
│   ├── CA_Logo.png               # Logo for the report cover page
├── data/                    # Raw input files
├── data_csv/                # Auto-generated CSVs after conversion
├── modules/                 # Modular report components
│   ├── barcharts.py              # Bar chart generation module
│   ├── basicDataAnalysis.py      # Basic data analysis module
│   ├── coverpage.py              # Cover page generation module
│   ├── summary.py                # Summary generation module
├── reports/                 # Final PDF reports
├── utils/                   # Helper utilities
│   ├── convert_files.py          # Function for file conversion
│   ├── load_config.py            # Functon to load the configuration file
├── generate_report.py       # Report generation logic
├── generate_unique_values_report.py  # Unique values report generator
├── report_config.json       # Config for report modules
├── .env                     # Environment variables
├── venv/                    # Virtual environment (not tracked in version control)
├── .gitignore               # Specifies files/directories to exclude from Git
├── README.md                # Project documentation
├── requirements.txt         # List of dependencies
```

---

## Installation

```bash
# Clone the repo
git clone <repository-url>
cd data-visualization

# Set up environment
python -m venv venv
source venv/bin/activate     # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### 1. Configure `.env`

```ini
DATA_PATH=data/FILE_PATH              # Path to your input data (can be a file or directory)
DROP_EMPTY_COLUMNS=True               # Whether to drop columns that are entirely empty (True/False)
UNIQUE_VALUE_COLUMNS=col1,col2,col3   # Comma-separated list of columns to analyze for unique values (generate_unique_values.py)
REPORT_CONFIG_PATH=report_config.json # Path to the JSON config file defining which modules to run and their options
REPORT_TITLE=Title of Report          # Global title used on the report cover page
CHUNK_SIZE=40                         # Chunk size for bar chart grouping (relevant for the barchart.py module)
XAXIS_LABEL=Columns                   # X-axis label for generated bar charts (relevant for the barchart.py module)
YAXIS_LABEL=Unique Values             # Y-axis label for generated bar charts (relevant for the barchart.py module)
PAGE_NUMBERING=True                   # Whether to include page numbers in the final PDF report
REPORTS_DIR=reports                   # Output directory where reports are saved
CSV_DIR=data_csv                      # Intermediate directory where converted CSV files are stored
REPORT_MODULE_PATH=modules            # Path to the folder containing report generation modules (e.g., summary, coverpage)
LOGO_PATH=assets/CA_Logo.png          # Path to the logo image used on the cover page
REPORT_CSS_PATH=assets/styles.css     # Path to the CSS file used to style the report HTML

```

### 2. Configure `report_config.json`

The environment variable for reports are used here

```json
[
    {
        "report": "coverpage",
        "options": {"title": "${REPORT_TITLE}"}
    },
    {
        "report": "summary",
        "options": {}
    },
    {
        "report": "barcharts",
        "options": { "chunk_size": "${CHUNK_SIZE}", "xaxis_label": "${XAXIS_LABEL}", "yaxis_label": "${YAXIS_LABEL}"}
    },
    {
        "report": "basicDataAnalysis",
        "options": {}
    }
]
```

### 3. Run Reports

```bash
# Generate main report (auto-conversion + modular sections)
python generate_report.py

# Generate unique values report
python generate_unique_values_report.py
```

---

## Output

* PDFs are saved in `reports/`.
* Converted CSVs are stored in `data_csv/{source}`.
* Supports nested directories and multi-sheet Excel files.

---

## Extensibility

* Add new modules under `modules/`.
* Register them via `report_config.json`.
* Access new options using `.env` or pass directly via the config file.

---

## License

MIT License. See `LICENSE` for more information.
