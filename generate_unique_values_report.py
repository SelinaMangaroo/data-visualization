import os
import pandas as pd
from dotenv import load_dotenv
from xhtml2pdf import pisa
from utils.convert_files import auto_convert_to_csv 

load_dotenv()

def generate_unique_values_report(input_csv=None, column_names=None):
    """
    Generates a PDF containing unique values for specified columns in CSV file(s).
    Automatically converts .xlsx/.xml files if needed. Reads paths from .env if not provided.
    """
    # Load from .env if not passed explicitly
    raw_path = input_csv or os.getenv("DATA_PATH")
    converted_path, base_name = auto_convert_to_csv(raw_path)  # Auto convert if needed

    columns_str = os.getenv("UNIQUE_VALUE_COLUMNS", "")
    column_names = column_names or [col.strip() for col in columns_str.split(",") if col.strip()]

    reports_dir = os.getenv("REPORTS_DIR", "./reports")
    css_path = os.getenv("REPORT_CSS_PATH", "./assets/styles.css")

    # Validate
    if not converted_path or not column_names:
        raise ValueError("CSV path and column names must be provided (either as arguments or in .env)")
    if not os.path.exists(converted_path):
        raise FileNotFoundError(f"Converted path not found: {converted_path}")
    if not os.path.exists(css_path):
        raise FileNotFoundError(f"CSS file not found: {css_path}")
    os.makedirs(reports_dir, exist_ok=True)

    # Determine whether path is a file or directory
    csv_files = [converted_path] if os.path.isfile(converted_path) else [
        os.path.join(converted_path, f) for f in os.listdir(converted_path) if f.endswith(".csv")
    ]

    # base_name = os.path.splitext(os.path.basename(converted_path.rstrip("/")))[0]
    output_pdf = os.path.join(reports_dir, f"{base_name}_unique_vals.pdf")

    # Read CSS
    with open(css_path, "r") as f:
        inline_css = f"<style>{f.read()}</style>"

    html_sections = ""
    for csv_path in csv_files:
        try:
            df = pd.read_csv(csv_path, low_memory=False)
        except Exception as e:
            print(f"[ERROR] Failed to read {csv_path}: {e}")
            continue

        df_cols = {c.strip().lower(): c for c in df.columns}
        try:
            resolved_columns = [df_cols[c.strip().lower()] for c in column_names]
        except KeyError as e:
            print(f"[ERROR] Column not found in {csv_path}: {e.args[0]}")
            continue

        content_html = ""
        for column in resolved_columns:
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
        html_sections += file_section + "<div style='page-break-before: always;'></div>"

    html_report = f"""
    <html>
        <head>{inline_css}</head>
        <body>
            <h1 class="header">Unique Values Report</h1>
            {html_sections}
        </body>
    </html>
    """

    with open(output_pdf, "wb") as pdf_file:
        pisa.CreatePDF(html_report, dest=pdf_file)

    print(f"Unique values PDF generated: {output_pdf}")

if __name__ == "__main__":
    try:
        generate_unique_values_report()
    except Exception as e:
        print(f"[ERROR] {e}")