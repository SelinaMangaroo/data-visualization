import pandas as pd
import os
import plotly.express as px
import numpy as np
from xhtml2pdf import pisa
import datetime
from io import BytesIO
import base64

# def process_and_generate_report(csv_file_path, output_folder="reports"):
#     """
#     Cleans the data, performs analysis, and generates a PDF report.

#     Parameters:
#         csv_file_path (str): Path to the input CSV file.
#         output_folder (str): Directory where the PDF report will be saved.

#     Returns:
#         None
#     """
#     # Load the dataset
#     df = pd.read_csv(csv_file_path, index_col=0, low_memory=False)
#     print("Original DataFrame Info:")
#     print(df.info())

    # # Data Cleaning and Analysis
    # original_columns = df.columns.tolist()
    # original_row_count = df.shape[0]
    # empty_row_count = df.isnull().all(axis=1).sum()
    # df = df.dropna(axis=1, how='all')
    # current_columns = df.columns.tolist()
    # current_row_count = df.shape[0]
    # dropped_columns = [col for col in original_columns if col not in current_columns]
    # number_of_dropped_columns = len(dropped_columns)
    # number_of_current_columns = len(current_columns)
    # column_value_counts = df.count()
    # # unique_values = {col: df[col].nunique() for col in current_columns}
    # # Ensure unique values are always arrays
    # unique_values = {col: np.atleast_1d(df[col].unique()) for col in current_columns}
    # columns_with_zeros = {
    #     col: (df[col] == 0).sum() > 0 for col in current_columns if not pd.api.types.is_numeric_dtype(df[col])
    # }

    # # Display summary in the notebook
    # # print("\nDropped Columns:", dropped_columns)
    # # print(f"Number of Dropped Columns: {number_of_dropped_columns}")
    # # print("\nCurrent Columns:", current_columns)
    # # print(f"Number of Current Columns: {number_of_current_columns}")
    # # print(f"\nNumber of Rows: {current_row_count}")
    # # print(f"Number of Empty Rows: {empty_row_count}")
    # # print("\nNumber of Values in Each Column:")
    # # print(column_value_counts)
    # # print("\nUnique Values for Each Column:")
    # # for col, unique_count in unique_values.items():
    # #     print(f"{col}: {unique_count}")
    # # print("\nColumns with Zeros (Non-Numerical):")
    # # for col, has_zeros in columns_with_zeros.items():
    # #     if has_zeros:
    # #         print(f"{col}: Contains zeros")
    
#     # Create a Summary DataFrame for Unique Values
#     summary_df = pd.DataFrame({
#         'Column': unique_values.keys(),
#         'Unique Values': [
#             ', '.join(map(str, values[:100])) + ('...' if len(values) > 100 else '') 
#             for values in unique_values.values()
#         ],
#         'Unique Count': [len(values) for values in unique_values.values()]
#     })

#     # Sort the summary DataFrame by Unique Count
#     summary_df = summary_df.sort_values(by='Unique Count', ascending=False)

#     # Display summary in the notebook
#     # print("\nSummary DataFrame:")
#     # print(summary_df)

#     # Interactive Bar Chart for Unique Count
#     fig = px.bar(summary_df, x='Column', y='Unique Count', text='Unique Count', title='Unique Count of Values per Column')
#     fig.update_traces(textposition='outside')
#     fig.show()
    
#     # Save the chart as an image
#     os.makedirs(output_folder, exist_ok=True)
#     base_file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
#     chart_image_path = os.path.join(output_folder, f"{base_file_name}_unique_count_chart.png")
#     fig.write_image(chart_image_path, format='png')
#     print(f"Bar chart image saved: {chart_image_path}")
    

#     # Generate PDF Report
#     class PDF(FPDF):
#         def header(self):
#             self.set_font('Arial', 'B', 12)
#             self.cell(0, 10, 'Data Analysis Report', align='C', ln=1)

#         def footer(self):
#             self.set_y(-15)
#             self.set_font('Arial', 'I', 8)
#             self.cell(0, 10, f'Page {self.page_no()}', align='C')

#     pdf = PDF()
#     pdf.add_page()
#     pdf.set_font('Arial', size=10)
    
#     # Add Analysis Details with Spacing and Bold Titles
#     def add_section_title(pdf, title):
#         pdf.set_font('Arial', 'B', 10)
#         pdf.cell(0, 10, title, ln=1)
#         pdf.ln(5)  # Add space after the title
#         pdf.set_font('Arial', size=10)

#     add_section_title(pdf, "Dropped Columns:")
#     pdf.multi_cell(0, 10, ", ".join(dropped_columns) if dropped_columns else "None")
#     pdf.cell(0, 10, f"Number of Dropped Columns: {number_of_dropped_columns}", ln=1)
#     pdf.ln(5)

#     add_section_title(pdf, "Current Columns:")
#     pdf.multi_cell(0, 10, ", ".join(current_columns))
#     pdf.cell(0, 10, f"Number of Current Columns: {number_of_current_columns}", ln=1)
#     pdf.ln(5)

#     add_section_title(pdf, "Number of Rows:")
#     pdf.cell(0, 10, f"{current_row_count}", ln=1)
#     pdf.ln(5)

#     add_section_title(pdf, "Number of Empty Rows:")
#     pdf.cell(0, 10, f"{empty_row_count}", ln=1)
#     pdf.ln(5)

#     add_section_title(pdf, "Number of Values in Each Column:")
#     for col, count in column_value_counts.items():
#         pdf.cell(0, 10, f"{col}: {count}", ln=1)
#     pdf.ln(5)

#     add_section_title(pdf, "Unique Values for Each Column:")
#     for col, values in unique_values.items():
#         formatted_values = ', '.join(map(str, values[:100])) + ('...' if len(values) > 100 else '')
#         pdf.set_font('Arial', 'U', 10)  # Set underline font for column names
#         pdf.cell(0, 10, f"{col}:", ln=1)
#         pdf.set_font('Arial', size=7)
#         pdf.multi_cell(0, 10, formatted_values)
#     pdf.ln(5)

#     # add_section_title(pdf, "Columns with Zeros (Non-Numerical):")
#     # for col, has_zeros in columns_with_zeros.items():
#     #     pdf.cell(0, 10, f"{col}: {'Contains zeros' if has_zeros else 'No zeros'}", ln=1)
#     # pdf.ln(5)
    
#     columns_with_zeros_present = [col for col, has_zeros in columns_with_zeros.items() if has_zeros]
#     if columns_with_zeros_present:
#         add_section_title(pdf, "Columns with Zeros (Non-Numerical):")
#         for col in columns_with_zeros_present:
#             pdf.cell(0, 10, f"{col}: Contains zeros", ln=1)
#         pdf.ln(5)
    
#     # Add the Bar Chart Image to the PDF
#     pdf.add_page()
#     pdf.cell(0, 10, "Unique Count of Values per Column", ln=1, align='C')
#     pdf.image(chart_image_path, x=10, y=20, w=190)  # Adjust image size and position as needed

#     # Ensure the reports folder exists
#     os.makedirs(output_folder, exist_ok=True)

#     # Extract base file name and save the PDF
#     base_file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
#     pdf_file_path = os.path.join(output_folder, f"{base_file_name}_report.pdf")
#     pdf.output(pdf_file_path)

#     print(f"PDF report generated: {pdf_file_path}")

def generate_cover_page(input_path):
    """
    Generates HTML content for the cover page.

    Parameters:
        input_path (str): Path to the input file or directory.

    Returns:
        str: HTML content for the cover page.
    """
    # Determine the name of the file/directory
    if os.path.isfile(input_path):
        input_name = os.path.basename(input_path)
        file_size = os.path.getsize(input_path) / (1024 * 1024)  # Size in MB
    elif os.path.isdir(input_path):
        input_name = os.path.basename(os.path.normpath(input_path))
        # Calculate total size of all files in the directory
        file_size = sum(os.path.getsize(os.path.join(input_path, f)) 
        for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)))
        file_size /= (1024 * 1024)  # Size in MB
    else:
        raise ValueError("Invalid input path.")

    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate the HTML content for the cover page
    cover_page_html = f"""
    <div class="cover-page-container">
        <div class="cover-page">
            <img src="../assets/CA_Logo.png" alt="Collective Access Logo">
            <p><strong>Report for:</strong> {input_name}</p>
            <p><strong>Generated On:</strong> {current_datetime}</p>
            <p><strong>File Size:</strong> {file_size:.2f} MB</p>
        </div>
    </div>
    """
    return cover_page_html

def generate_summary_with_xhtml2pdf(directory):
    """
    Generates the HTML content for a summary page using xhtml2pdf.

    Parameters:
        directory (str): Path to the directory containing multiple CSV files.
    Returns:
        str: HTML content for the summary.
    """
    # Ensure the directory exists and contains CSV files
    if not os.path.isdir(directory):
        raise ValueError(f"The directory '{directory}' does not exist or is not a directory.")

    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")]
    if not csv_files:
        raise ValueError(f"No CSV files found in the directory '{directory}'.")

    # Initialize summary data
    all_columns = set()
    file_columns = {}
    stats = []

    # Collect data from all files
    for csv_file_path in csv_files:
        base_file_name = os.path.basename(csv_file_path)

        # Load the dataset
        try:
            df = pd.read_csv(csv_file_path, index_col=0, low_memory=False)
        except Exception as e:
            print(f"Error loading file {csv_file_path}: {e}")
            continue

        # Collect columns and compute stats
        total_columns = df.columns.tolist()
        dropped_columns = len(df.columns[df.isnull().all()])
        number_of_rows = df.shape[0]

        file_columns[base_file_name] = total_columns
        all_columns.update(total_columns)

        stats.append({
            "File": base_file_name,
            "Total Columns": len(total_columns),
            "Dropped Columns": dropped_columns,
            "Rows": number_of_rows,
        })

    # Generate HTML content
    html_content = f"""
    <h1 class="header">Summary of Processed Files</h1>
    <h2 class="sub-header">Summary Statistics:</h2>
    <table class="summary-table">
        <thead>
            <tr>
                <th>File</th>
                <th>Total Columns</th>
                <th>Dropped Columns</th>
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
            <td>{', '.join(files_with_column)}</td>
        </tr>
        """

    html_content += """
        </tbody>
    </table>
    """
    return html_content


def process_and_generate_report(input_path):
    """
    Cleans the data, performs analysis, and generates a PDF report for one or more CSV files.
    Saves processed CSV files with dropped columns into a 'dropped' folder within the 'data' directory.
    Saves reports in a sibling folder to the 'data' directory.

    Parameters:
        input_path (str): Path to a CSV file or a directory containing multiple CSV files.

    Returns:
        None
    """
    
    # Locate the `data` directory dynamically
    root_dir = os.getcwd()
    data_directory = None
    while root_dir != os.path.dirname(root_dir):  # Stop when reaching the root directory
        if "data" in os.listdir(root_dir):
            data_directory = os.path.join(root_dir, "data")
            break
        root_dir = os.path.dirname(root_dir)
    if not data_directory:
        raise ValueError("Could not find 'data' directory in the path hierarchy.")

    # Define `reports` and `_dropped` directories
    reports_folder = os.path.join(os.path.dirname(data_directory), "reports")
    os.makedirs(reports_folder, exist_ok=True)
    
    # Check if input is a file or a directory
    if os.path.isfile(input_path):
        csv_files = [input_path]
        pdf_name = os.path.splitext(os.path.basename(input_path))[0] + "_report.pdf"
        dropped_dir = os.path.join(data_directory, os.path.splitext(os.path.basename(input_path))[0] + "_dropped")
    elif os.path.isdir(input_path):
        csv_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".csv")]
        pdf_name = os.path.basename(os.path.normpath(input_path)) + "_report.pdf"
        dropped_dir = os.path.join(data_directory, os.path.basename(os.path.normpath(input_path)) + "_dropped")
    else:
        raise ValueError(f"The input path '{input_path}' is neither a valid file nor a directory.")

    # os.makedirs(output_folder, exist_ok=True)
    os.makedirs(dropped_dir, exist_ok=True)
    
    # Generate the cover page
    cover_page_html = generate_cover_page(input_path)

    # Generate summary HTML content
    summary_html = ""
    if os.path.isdir(input_path):
        summary_html = generate_summary_with_xhtml2pdf(input_path)
    
    # Inline the CSS
    css_path = os.path.join(os.path.dirname(__file__), "../assets/styles.css")
    with open(css_path, "r") as css_file:
        inline_styles = f"<style>{css_file.read()}</style>"
    
    html_report = f"""
    <html>
        <head>
            {inline_styles}
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                    @frame footer_frame {{
                        -pdf-frame-content: footer_content;
                        bottom: 1cm; 
                        left: 1cm;
                        width: 19cm;
                        height: 1cm;
                    }}
                }}
            </style>
        </head>
        <body>
            <!-- Cover Page -->
            {cover_page_html}
            
            <div style="page-break-before: always;"></div>
            
            <!-- Footer Definition -->
            <div id="footer_content" class="footer">
                Page <pdf:pageNumber> of <pdf:pageCount>
            </div>
            
            <!-- Summary Content -->
            {summary_html}
            
            <div style="page-break-before: always;"></div>

            <!-- Report Content -->
    """

    for csv_file_path in csv_files:
        base_file_name = os.path.splitext(os.path.basename(csv_file_path))[0]

        # Load CSV data
        try:
            df = pd.read_csv(csv_file_path, index_col=0, low_memory=False)
        except Exception as e:
            print(f"Error loading file {csv_file_path}: {e}")
            continue

        # Perform data analysis
        original_columns = df.columns.tolist()
        original_row_count = df.shape[0]
        empty_row_count = df.isnull().all(axis=1).sum()
        df = df.dropna(axis=1, how='all')
        current_columns = df.columns.tolist()
        dropped_columns = [col for col in original_columns if col not in current_columns]
        number_of_dropped_columns = len(dropped_columns)
        number_of_current_columns = len(current_columns)
        column_value_counts = df.count()
        unique_values = {col: np.atleast_1d(df[col].unique()) for col in current_columns}
        columns_with_zeros = {
            col: (df[col] == 0).sum() > 0 for col in current_columns if not pd.api.types.is_numeric_dtype(df[col])
        }
        
        # Save the cleaned DataFrame
        dropped_csv_path = os.path.join(dropped_dir, f"{base_file_name}_dropped.csv")
        df.to_csv(dropped_csv_path, index=False)
        print(f"Saved cleaned CSV: {dropped_csv_path}")
        
        # Data Cleaning and Analysis
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
        
        
        # Generate Columns with Zeros section
        columns_with_zeros_list = [col for col, has_zeros in columns_with_zeros.items() if has_zeros]
        columns_with_zeros = ""
        if columns_with_zeros_list:
            columns_with_zeros = f"""
                <h2 class="sub-header">Columns with Zeros:</h2>
                <p>{', '.join(columns_with_zeros_list)}</p>
            """

        # Generate bar charts in chunks if needed
        chunk_size = 40  # Maximum number of bars per chart
        chart_df = pd.DataFrame({
            'Column': unique_values.keys(),
            'Unique Count': [len(values) for values in unique_values.values()]
        })
        chart_df = chart_df.sort_values(by='Unique Count', ascending=False)

        # Generate charts and embed directly in HTML
        charts_html = ""  # Accumulate all charts' HTML here
        for i in range(0, len(chart_df), chunk_size):
            chunk = chart_df.iloc[i:i + chunk_size]
            part_number = (i // chunk_size) + 1

            # Generate the bar chart
            fig = px.bar(chunk, x='Column', y='Unique Count', text='Unique Count', title=f'Unique Count of Values for {base_file_name} (Part {part_number})')
            fig.update_traces(textposition='outside')
            fig.update_layout(
                xaxis=dict(tickangle=-45),
                height=600,
                margin=dict(l=50, r=50, t=50, b=150),
                xaxis_title='Column Names',
                yaxis_title='Unique Count',
            )

            # Save the chart image to memory as Base64
            buffer = BytesIO()
            fig.write_image(buffer, format="png")
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
            buffer.close()
            # Append the chart to the charts_html string
            
            charts_html += f"""
                <h2 class="sub-header"></h2>
                <img src="data:image/png;base64,{image_base64}" alt="Bar Chart Part {part_number}">
            """
        
        # Generate table rows for column value counts
        col_value_table_rows = ""
        for col, count in column_value_counts.items():
            col_value_table_rows += f"""
            <tr>
                <td>{col}</td>
                <td>{count}</td>
            </tr>
            """

        # Add column value counts table
        column_counts_table = f"""
        <h2 class="sub-header">Column Value Counts:</h2>
        <table class="value-counts-table">
            <thead>
                <tr>
                    <th>Column</th>
                    <th>Value Count</th>
                </tr>
            </thead>
            <tbody>
                {col_value_table_rows}
            </tbody>
        </table>
        """

        # Append analysis details to the report
        html_report += f"""
            <h1 class="header">Report for {base_file_name}</h1>
            <h2 class="sub-header">Dropped Columns ({number_of_dropped_columns}):</h2>
            <p>{', '.join(dropped_columns) if dropped_columns else "None"}</p>
            <h2 class="sub-header">Current Columns ({number_of_current_columns}):</h2>
            <p>{', '.join(current_columns)}</p>
            <h2 class="sub-header">Number of Rows:</h2>
            <p>{original_row_count}</p>
            <h2 class="sub-header">Number of Empty Rows:</h2>
            <p>{empty_row_count}</p>
            {column_counts_table}
            {columns_with_zeros}
            {charts_html}
            <div style="page-break-before: always;"></div>
        """
    
    html_report += """
        </body>
    </html>
    """

    # Create the final PDF
    pdf_path = os.path.join(reports_folder, pdf_name)
    with open(pdf_path, "wb") as pdf_file:
        pisa.CreatePDF(html_report, dest=pdf_file)

    print(f"PDF report generated: {pdf_path}")
