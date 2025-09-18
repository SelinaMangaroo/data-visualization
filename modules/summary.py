import pandas as pd
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger("report")
load_dotenv(override=True)

drop_empty_columns = os.getenv("DROP_EMPTY_COLUMNS", "true").lower() == "true"

def generate_report_section(input_path, options=None, **kwargs):
    """
    Generates the HTML content for a summary page.
    """
    options = options or {}

    # Ensure the directory exists and contains CSV files
    if not os.path.isdir(input_path):
        raise ValueError(f"The directory '{input_path}' does not exist or is not a directory.")

    csv_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".csv")]
    if not csv_files:
        raise ValueError(f"No CSV files found in the directory '{input_path}'.")

    # Initialize summary data
    all_columns = set()
    file_columns = {}
    stats = []

    for csv_file_path in csv_files:
        base_file_name = os.path.basename(csv_file_path)

        try:
            df = pd.read_csv(csv_file_path, index_col=0, low_memory=False)
        except Exception as e:
            logger.exception(f"Error loading file {csv_file_path}: {e}")
            continue

        total_columns = df.columns.tolist()
        if drop_empty_columns:
            dropped_columns = len(df.columns[df.isnull().all()])
            populated_columns = len(df.columns) - dropped_columns
        else:
            dropped_columns = 0
            populated_columns = len(df.columns)

        number_of_rows = df.shape[0]
        file_columns[base_file_name] = total_columns
        all_columns.update(total_columns)

        stats.append({
            "File": base_file_name.replace("_", "_<br>"),
            "Total Columns": len(total_columns),
            "Dropped Columns": dropped_columns,
            "Populated Columns": populated_columns,
            "Rows": number_of_rows,
        })

    # Build HTML
    html_content = f"""
    <div class="section-block">
        <h1 class="header">Summary of Processed Files</h1>
        <p><strong>Empty Column Dropping:</strong> {"Enabled" if drop_empty_columns else "Disabled"}</p>
        <h2 class="sub-header">Summary Statistics:</h2>
        <table class="summary-table">
            <thead>
                <tr>
                    <th style="width: 250px;">File</th>
                    <th>Total Columns</th>
                    <th>Dropped Columns</th>
                    <th>Populated Columns</th>
                    <th>Number of Rows</th>
                </tr>
            </thead>
            <tbody>
    """

    for stat in stats:
        html_content += f"""
            <tr>
                <td>{stat['File']}</td>
                <td>{stat['Total Columns']}</td>
                <td>{stat['Dropped Columns']}</td>
                <td>{stat['Populated Columns']}</td>
                <td>{stat['Rows']}</td>
            </tr>
        """
    
    html_content += """
        </tbody>
    </table>
    <h2 class="sub-header">Column Presence Across Files:</h2>
    <table class="column-table">
        <thead>
            <tr>
                <th>Column</th>
                <th>Files Containing Column</th>
            </tr>
        </thead>
        <tbody>
    """

    for column in sorted(all_columns):
        files_with_column = [file for file, cols in file_columns.items() if column in cols]
        html_content += f"""
        <tr>
            <td>{column}</td>
            <td>{"<br>".join(files_with_column)}</td>
        </tr>
        """

    html_content += """
            </tbody>
        </table>
    </div>
    """

    return html_content + "<div class='page-break'></div>"
