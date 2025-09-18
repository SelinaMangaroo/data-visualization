import os
import pandas as pd
from dotenv import load_dotenv
from weasyprint import HTML, CSS
from utils.convert_files import auto_convert_to_csv 
from utils.logger import setup_logger

logger = setup_logger()
load_dotenv(override=True)

def generate_unique_values_report():
    """
    Generates a PDF containing unique values for specified columns in CSV file(s).
    Automatically converts .xlsx/.xml files if needed. Reads paths from .env if not provided.
    """
    logger.info("Starting unique values report generation.")
    
    # Load from .env if not passed explicitly
    raw_path = os.getenv("DATA_PATH")
    converted_path, base_name = auto_convert_to_csv(raw_path)  # Auto convert if needed

    columns_str = os.getenv("UNIQUE_VALUE_COLUMNS", "")
    column_names = [col.strip() for col in columns_str.split(",") if col.strip()]

    reports_dir = os.getenv("REPORTS_DIR", "./reports")
    css_path = os.getenv("REPORT_CSS_PATH", "./assets/styles.css")

    # Validate
    if not converted_path or not column_names:
        logger.error("CSV path and column names must be provided (either as arguments or in .env)")
        raise ValueError("CSV path and column names must be provided (either as arguments or in .env)")
    if not os.path.exists(converted_path):
        logger.error(f"Converted path not found: {converted_path}")
        raise FileNotFoundError(f"Converted path not found: {converted_path}")
    if not os.path.exists(css_path):
        logger.error(f"CSS file not found: {css_path}")
        raise FileNotFoundError(f"CSS file not found: {css_path}")
    os.makedirs(reports_dir, exist_ok=True)

    # Determine whether path is a file or directory
    csv_files = [converted_path] if os.path.isfile(converted_path) else [
        os.path.join(converted_path, f) for f in os.listdir(converted_path) if f.endswith(".csv")
    ]

    output_pdf = os.path.join(reports_dir, f"{base_name}_unique_vals.pdf")

    html_sections = ""
    for csv_path in csv_files:
        try:
            logger.info(f"Reading CSV file: {csv_path}")
            df = pd.read_csv(csv_path, low_memory=False)
        except Exception as e:
            logger.error(f"Failed to read {csv_path}: {e}")
            continue

        df_cols = {c.strip().lower(): c for c in df.columns}
        try:
            resolved_columns = [df_cols[c.strip().lower()] for c in column_names]
        except KeyError as e:
            logger.warning(f"Column not found in {csv_path}: {e.args[0]}")
            continue

        content_html = ""
        for column in resolved_columns:
            logger.info(f"Processing column: {column}")
            unique_vals = df[column].dropna().unique()
            unique_vals = sorted(unique_vals, key=str)

            rows = ""
            for i in range(0, len(unique_vals), 3):
                row_vals = unique_vals[i:i + 3]
                rows += "<tr>" + "".join(f"<td>{val}</td>" for val in row_vals) + "</tr>"

            content_html += f"""
            <h2 class="sub-header">Unique Values in Column: {column}</h2>
            <table class="unique-values-table">
                <tbody>{rows}</tbody>
            </table>
            """

        file_section = f"""
        <h1 class="header">File: {os.path.basename(csv_path)}</h1>
        {content_html}
        """
        html_sections += file_section + "<div class='page-break'></div>"

    html_report = f"""
    <html>
        <head><link rel="stylesheet" href="{css_path}"></head>
        <body>
            <h1 class="header">Unique Values Report</h1>
            {html_sections}
        </body>
    </html>
    """

    # Generate PDF with WeasyPrint
    HTML(string=html_report).write_pdf(output_pdf, stylesheets=[CSS(css_path)])

    logger.info(f"Unique values PDF generated: {output_pdf}")

if __name__ == "__main__":
    try:
        generate_unique_values_report()
    except Exception as e:
        logger.exception(f"Unhandled error during report generation: {e}")
