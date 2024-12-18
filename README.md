# Data Visualization Project

This project focuses on cleaning, processing, and visualizing datasets using Python. The goal is to build a structured workflow for handling raw data, standardizing it, and extracting meaningful insights through visualization. Below is an overview of the project setup, functionality, and usage instructions.

---

## Project Structure

```
data-visualization/
├── assets/                       # Static assets (CSS, images, logos)
│   ├── styles.css                # Stylesheet for PDF reports
│   ├── CA_Logo.png               # Logo for the report cover page
├── data/                         # Datasets to be processed
├── notebooks/
│   ├── clean_files.ipynb         # Notebook for cleaning data
│   ├── visualize_files.ipynb     # Notebook for visualizing data
├── scripts/
│   ├── __init__.py               # Marks the directory as a module
│   ├── convert_to_csv.py         # Script for converting XML and Excel files to CSV
│   ├── data_processing.py        # Main script for processing and generating reports
├── reports/                      # Generated reports (PDF)
├── venv/                         # Virtual environment (not tracked in version control)
├── .gitignore                    # Specifies files/directories to exclude from Git
├── README.md                     # Project documentation
├── requirements.txt              # List of dependencies
```

---

## Features

### 1. **Data Cleaning**
- **Notebook**: `clean_files.ipynb`
- **Purpose**: Prepares raw datasets for further analysis.
- **Key Tasks**:
  - Removes columns with missing or irrelevant values.
  - Standardizes specific column values (e.g., correcting column inconsistencies).
  - Fills `NaN` values with defaults (e.g., `0`).
  - Outputs a cleaned dataset for further processing.

### 2. **Data Visualization**
- **Notebook**: `visualize_files.ipynb`
- **Purpose**: Provides insights into datasets through summary statistics and visualizations.
- **Key Tasks**:
  - Visualizes unique value distributions across columns.
  - Generates interactive and static bar charts using `plotly`.
  - Filters datasets for specific columns of interest.

### 3. **File Conversion**
- **Script**: `convert_to_csv.py`
- **Purpose**: Converts raw data files into a CSV format for easier processing.
- **Key Features**:
  - Cleans malformed characters in XML files (`zap_gremlins`).
  - Converts XML files to CSV (`xml_to_csv`).
  - Converts Excel files (`.xls` and `.xlsx`) to CSV (`convert_excel_to_csv`).

### 4. **PDF Report Generation**
- **Script**: `data_processing.py`
- **Purpose**: Processes datasets, generates analysis, and compiles results into a PDF report.
- **Key Features**:
  - Cover Page: Displays the file/directory name, report generation date, and file size.
  - Summary Section: Includes statistics like the number of rows, current columns, dropped columns, and a column presence table.
  - Numerous data insights.
  - Processed Files: Saves datasets with dropped columns in the data/{input_name}_dropped folder.

---

## Installation

### Prerequisites
- Python 3.8+
- `pip` (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd data-visualization
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Running Notebooks
- Open Jupyter Notebook:
  ```bash
  jupyter notebook
  ```
- Navigate to the `notebooks/` directory and run:
  - `clean_files.ipynb` for data cleaning.
  - `visualize_files.ipynb` for data visualization.

### 2. Using Scripts
- Convert files using the provided script:
  ```python
  from scripts.convert_to_csv import xml_to_csv, convert_excel_to_csv

  # Convert XML to CSV
  xml_to_csv("file path")

  # Convert Excel files to CSV
  convert_excel_to_csv("file path")
  ```

- Generate the report
  ```python
  from scripts.data_processing import process_and_generate_report

  # For a single file
  process_and_generate_report("data/example.csv")

  # For a directory containing multiple CSV files
  process_and_generate_report("data/")
  ```

---

## Dependencies

- `pandas`: For data manipulation and analysis.
- `xhtml2pdf`: Generates PDFs from HTML content.
- `matplotlib`: For creating static visualizations.
- `plotly`: For creating interactive visualizations.
- `tabulate`: For formatting data summaries as tables.
- `openpyxl`: For handling `.xlsx` files.
- `xlrd`: For handling `.xls` files.

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## Output Structure
- All datasets should be stored in the `data` directory.
- Ensure file paths are updated accordingly in notebooks and scripts if custom locations are used.
- Processed PDF reports will be saved in the reports directory.
- Processed datasets with dropped columns are saved in:
  ```
  data/{input_name}_dropped/
  ```
- Assets such as logos and stylesheets are located in the assets directory.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---


