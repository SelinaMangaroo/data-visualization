import pandas as pd
import os
from fpdf import FPDF
import plotly.express as px
import numpy as np

def process_and_generate_report(csv_file_path, output_folder="reports"):
    """
    Cleans the data, performs analysis, and generates a PDF report.

    Parameters:
        csv_file_path (str): Path to the input CSV file.
        output_folder (str): Directory where the PDF report will be saved.

    Returns:
        None
    """
    # Load the dataset
    df = pd.read_csv(csv_file_path, index_col=0, low_memory=False)
    print("Original DataFrame Info:")
    print(df.info())

    # Data Cleaning and Analysis
    original_columns = df.columns.tolist()
    original_row_count = df.shape[0]
    empty_row_count = df.isnull().all(axis=1).sum()
    df = df.dropna(axis=1, how='all')
    current_columns = df.columns.tolist()
    current_row_count = df.shape[0]
    dropped_columns = [col for col in original_columns if col not in current_columns]
    number_of_dropped_columns = len(dropped_columns)
    number_of_current_columns = len(current_columns)
    column_value_counts = df.count()
    # unique_values = {col: df[col].nunique() for col in current_columns}
    # Ensure unique values are always arrays
    unique_values = {col: np.atleast_1d(df[col].unique()) for col in current_columns}
    columns_with_zeros = {
        col: (df[col] == 0).sum() > 0 for col in current_columns if not pd.api.types.is_numeric_dtype(df[col])
    }

    # Display summary in the notebook
    # print("\nDropped Columns:", dropped_columns)
    # print(f"Number of Dropped Columns: {number_of_dropped_columns}")
    # print("\nCurrent Columns:", current_columns)
    # print(f"Number of Current Columns: {number_of_current_columns}")
    # print(f"\nNumber of Rows: {current_row_count}")
    # print(f"Number of Empty Rows: {empty_row_count}")
    # print("\nNumber of Values in Each Column:")
    # print(column_value_counts)
    # print("\nUnique Values for Each Column:")
    # for col, unique_count in unique_values.items():
    #     print(f"{col}: {unique_count}")
    # print("\nColumns with Zeros (Non-Numerical):")
    # for col, has_zeros in columns_with_zeros.items():
    #     if has_zeros:
    #         print(f"{col}: Contains zeros")
    
    # Create a Summary DataFrame for Unique Values
    summary_df = pd.DataFrame({
        'Column': unique_values.keys(),
        'Unique Values': [
            ', '.join(map(str, values[:100])) + ('...' if len(values) > 100 else '') 
            for values in unique_values.values()
        ],
        'Unique Count': [len(values) for values in unique_values.values()]
    })

    # Sort the summary DataFrame by Unique Count
    summary_df = summary_df.sort_values(by='Unique Count', ascending=False)

    # Display summary in the notebook
    # print("\nSummary DataFrame:")
    # print(summary_df)

    # Interactive Bar Chart for Unique Count
    fig = px.bar(summary_df, x='Column', y='Unique Count', text='Unique Count', title='Unique Count of Values per Column')
    fig.update_traces(textposition='outside')
    fig.show()
    
    # Save the chart as an image
    os.makedirs(output_folder, exist_ok=True)
    base_file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    chart_image_path = os.path.join(output_folder, f"{base_file_name}_unique_count_chart.png")
    fig.write_image(chart_image_path, format='png')
    print(f"Bar chart image saved: {chart_image_path}")
    

    # Generate PDF Report
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Data Analysis Report', align='C', ln=1)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', align='C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', size=10)
    
    # Add Analysis Details with Spacing and Bold Titles
    def add_section_title(pdf, title):
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 10, title, ln=1)
        pdf.ln(5)  # Add space after the title
        pdf.set_font('Arial', size=10)

    add_section_title(pdf, "Dropped Columns:")
    pdf.multi_cell(0, 10, ", ".join(dropped_columns) if dropped_columns else "None")
    pdf.cell(0, 10, f"Number of Dropped Columns: {number_of_dropped_columns}", ln=1)
    pdf.ln(5)

    add_section_title(pdf, "Current Columns:")
    pdf.multi_cell(0, 10, ", ".join(current_columns))
    pdf.cell(0, 10, f"Number of Current Columns: {number_of_current_columns}", ln=1)
    pdf.ln(5)

    add_section_title(pdf, "Number of Rows:")
    pdf.cell(0, 10, f"{current_row_count}", ln=1)
    pdf.ln(5)

    add_section_title(pdf, "Number of Empty Rows:")
    pdf.cell(0, 10, f"{empty_row_count}", ln=1)
    pdf.ln(5)

    add_section_title(pdf, "Number of Values in Each Column:")
    for col, count in column_value_counts.items():
        pdf.cell(0, 10, f"{col}: {count}", ln=1)
    pdf.ln(5)

    add_section_title(pdf, "Unique Values for Each Column:")
    for col, values in unique_values.items():
        formatted_values = ', '.join(map(str, values[:100])) + ('...' if len(values) > 100 else '')
        pdf.set_font('Arial', 'U', 10)  # Set underline font for column names
        pdf.cell(0, 10, f"{col}:", ln=1)
        pdf.set_font('Arial', size=7)
        pdf.multi_cell(0, 10, formatted_values)
    pdf.ln(5)

    # add_section_title(pdf, "Columns with Zeros (Non-Numerical):")
    # for col, has_zeros in columns_with_zeros.items():
    #     pdf.cell(0, 10, f"{col}: {'Contains zeros' if has_zeros else 'No zeros'}", ln=1)
    # pdf.ln(5)
    
    columns_with_zeros_present = [col for col, has_zeros in columns_with_zeros.items() if has_zeros]
    if columns_with_zeros_present:
        add_section_title(pdf, "Columns with Zeros (Non-Numerical):")
        for col in columns_with_zeros_present:
            pdf.cell(0, 10, f"{col}: Contains zeros", ln=1)
        pdf.ln(5)
    
    # Add the Bar Chart Image to the PDF
    pdf.add_page()
    pdf.cell(0, 10, "Unique Count of Values per Column", ln=1, align='C')
    pdf.image(chart_image_path, x=10, y=20, w=190)  # Adjust image size and position as needed

    # Ensure the reports folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Extract base file name and save the PDF
    base_file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    pdf_file_path = os.path.join(output_folder, f"{base_file_name}_report.pdf")
    pdf.output(pdf_file_path)

    print(f"PDF report generated: {pdf_file_path}")
