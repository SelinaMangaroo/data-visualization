import pandas as pd
import os
from xhtml2pdf import pisa
from scripts.utils import find_directory

def generate_unique_values_report(input_csv, column_names):
    """
    Generates a PDF containing unique values for specified columns in a CSV file.

    Parameters:
        input_csv (str): Path to the input CSV file.
        column_names (list): List of column names to extract unique values for.

    Returns:
        None
    """
    
    # Locate the `data` directory dynamically
    data_directory = find_directory("data")
    
    reports_folder = os.path.join(os.path.dirname(data_directory), "reports")
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)

    # Generate the output PDF path
    base_name = os.path.splitext(os.path.basename(input_csv))[0]
    output_pdf = os.path.join(reports_folder, f"{base_name}_unique_vals.pdf")

    # Load the CSV file
    try:
        df = pd.read_csv(input_csv, low_memory=False)
    except Exception as e:
        raise ValueError(f"Error reading the CSV file: {e}")

    # Validate column names
    missing_columns = [col for col in column_names if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following columns are missing in the CSV file: {', '.join(missing_columns)}")

    # Extract unique values
    unique_values_html = ""
    for column in column_names:
        unique_values = df[column].dropna().unique()
        unique_values.sort()

        # Format unique values into rows of three columns
        rows = ""
        for i in range(0, len(unique_values), 3):
            row = unique_values[i:i+3]
            rows += "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"

        # Add the table for this column to the HTML
        unique_values_html += f"""
        <h2 class="sub-header">Unique Values in Column: {column}</h2>
        <table class="unique-values-table">
            <tbody>
                {rows}
            </tbody>
        </table>
        """

    # Generate the HTML report
    html_report = f"""
    <html>
        <head>
            <link rel="stylesheet" href="../assets/styles.css">
        </head>
        <body>
            <h1 class="header">Unique Values Report</h1>
            <h2 class="sub-header">File: {os.path.basename(input_csv)}</h2>
            {unique_values_html}
        </body>
    </html>
    """

    # Create the PDF
    with open(output_pdf, "wb") as pdf_file:
        pisa.CreatePDF(html_report, dest=pdf_file)
    print(f"PDF report generated: {output_pdf}")