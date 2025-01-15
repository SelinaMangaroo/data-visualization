import os
import importlib
import sys
from xhtml2pdf import pisa
from scripts.utils import find_directory

# from .modules.barcharts import generate_bar_charts
# from .modules.coverpage import generate_cover_page
# from .modules.summary import generate_summary
# from .modules.basicDataAnalysis import perform_basic_data_analysis



# def process_and_generate_report(input_path):
#     """
#     Cleans the data, performs analysis, and generates a PDF report for one or more CSV files.
#     Saves processed CSV files with dropped columns into a 'dropped' folder within the 'data' directory.
#     Saves reports in a sibling folder to the 'data' directory.

#     Parameters:
#         input_path (str): Path to a CSV file or a directory containing multiple CSV files.

#     Returns:
#         None
#     """
    
#     # Locate the `data` directory dynamically
#     data_directory = find_directory("data")

#     # Define `reports` and `_dropped` directories
#     reports_folder = os.path.join(os.path.dirname(data_directory), "reports")
#     os.makedirs(reports_folder, exist_ok=True)
    
#     # Check if input is a file or a directory
#     if os.path.isfile(input_path):
#         csv_files = [input_path]
#         pdf_name = os.path.splitext(os.path.basename(input_path))[0] + "_report.pdf"
#         dropped_dir = os.path.join(data_directory, os.path.splitext(os.path.basename(input_path))[0] + "_dropped")
#     elif os.path.isdir(input_path):
#         csv_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".csv")]
#         pdf_name = os.path.basename(os.path.normpath(input_path)) + "_report.pdf"
#         dropped_dir = os.path.join(data_directory, os.path.basename(os.path.normpath(input_path)) + "_dropped")
#     else:
#         raise ValueError(f"The input path '{input_path}' is neither a valid file nor a directory.")

#     os.makedirs(dropped_dir, exist_ok=True)
    
#     # Generate the cover page
#     cover_page_html = generate_cover_page(input_path)

#     # Generate summary HTML content
#     summary_html = ""
#     if os.path.isdir(input_path):
#         summary_html = generate_summary(input_path)
    
#     # Inline the CSS
#     css_path = os.path.join(os.path.dirname(__file__), "../assets/styles.css")
#     with open(css_path, "r") as css_file:
#         inline_styles = f"<style>{css_file.read()}</style>"
    
#     html_report = f"""
#     <html>
#         <head>
#             {inline_styles}
#             <style>
#                 @page {{
#                     size: A4;
#                     margin: 2cm;
#                     @frame footer_frame {{
#                         -pdf-frame-content: footer_content;
#                         bottom: 1cm; 
#                         left: 1cm;
#                         width: 19cm;
#                         height: 1cm;
#                     }}
#                 }}
#             </style>
#         </head>
#         <body>
#             <!-- Cover Page -->
#             {cover_page_html}
            
#             <div style="page-break-before: always;"></div>
            
#             <!-- Footer Definition -->
#             <div id="footer_content" class="footer">
#                 Page <pdf:pageNumber> of <pdf:pageCount>
#             </div>
            
#             <!-- Summary Content -->
#             {summary_html}
            
#             <div style="page-break-before: always;"></div>

#             <!-- Report Content -->
#     """

#     for csv_file_path in csv_files:
#         base_file_name = os.path.splitext(os.path.basename(csv_file_path))[0]

#         # Load CSV data
#         try:
#             df = pd.read_csv(csv_file_path, index_col=0, low_memory=False)
#         except Exception as e:
#             print(f"Error loading file {csv_file_path}: {e}")
#             continue

#         # Perform data analysis
#         original_columns = df.columns.tolist()
#         original_row_count = df.shape[0]
#         empty_row_count = df.isnull().all(axis=1).sum()
#         df = df.dropna(axis=1, how='all')
#         current_columns = df.columns.tolist()
#         dropped_columns = [col for col in original_columns if col not in current_columns]
#         number_of_dropped_columns = len(dropped_columns)
#         number_of_current_columns = len(current_columns)
#         column_value_counts = df.count()
#         unique_values = {col: np.atleast_1d(df[col].unique()) for col in current_columns}
#         columns_with_zeros = {
#             col: (df[col] == 0).sum() > 0 for col in current_columns if not pd.api.types.is_numeric_dtype(df[col])
#         }
        
#         # Save the cleaned DataFrame
#         dropped_csv_path = os.path.join(dropped_dir, f"{base_file_name}_dropped.csv")
#         df.to_csv(dropped_csv_path, index=False)
#         print(f"Saved cleaned CSV: {dropped_csv_path}")
        
#         # Generate Columns with Zeros section
#         columns_with_zeros_list = [col for col, has_zeros in columns_with_zeros.items() if has_zeros]
#         columns_with_zeros = ""
#         if columns_with_zeros_list:
#             columns_with_zeros = f"""
#                 <h2 class="sub-header">Columns with Zeros:</h2>
#                 <p>{', '.join(columns_with_zeros_list)}</p>
#             """
        
#         # Generate bar charts for unique counts
#         chart_df = pd.DataFrame({
#             "Column": unique_values.keys(),
#             "Unique Count": [len(values) for values in unique_values.values()],
#         }).sort_values(by="Unique Count", ascending=False)
#         charts_html = generate_bar_charts(
#             chart_df, 
#             x_axis="Column", 
#             y_axis="Unique Count", 
#             base_title=f"Unique Count of Values for {base_file_name}",
#             xaxis_label="Column Names",
#             yaxis_label="Unique Count"
#         )
        
#         # Generate table rows for column value counts
#         col_value_table_rows = ""
#         for col, count in column_value_counts.items():
#             col_value_table_rows += f"""
#             <tr>
#                 <td>{col}</td>
#                 <td>{count}</td>
#             </tr>
#             """

#         # Add column value counts table
#         column_counts_table = f"""
#         <h2 class="sub-header">Column Value Counts:</h2>
#         <table class="value-counts-table">
#             <thead>
#                 <tr>
#                     <th>Column</th>
#                     <th>Value Count</th>
#                 </tr>
#             </thead>
#             <tbody>
#                 {col_value_table_rows}
#             </tbody>
#         </table>
#         """

#         # Append analysis details to the report
#         html_report += f"""
#             <h1 class="header">Report for {base_file_name}</h1>
#             <h2 class="sub-header">Dropped Columns ({number_of_dropped_columns}):</h2>
#             <p>{', '.join(dropped_columns) if dropped_columns else "None"}</p>
#             <h2 class="sub-header">Current Columns ({number_of_current_columns}):</h2>
#             <p>{', '.join(current_columns)}</p>
#             <h2 class="sub-header">Number of Rows:</h2>
#             <p>{original_row_count}</p>
#             <h2 class="sub-header">Number of Empty Rows:</h2>
#             <p>{empty_row_count}</p>
#             {column_counts_table}
#             {columns_with_zeros}
#             {charts_html}
#             <div style="page-break-before: always;"></div>
#         """
    
#     html_report += """
#         </body>
#     </html>
#     """

#     # Create the final PDF
#     pdf_path = os.path.join(reports_folder, pdf_name)
#     with open(pdf_path, "wb") as pdf_file:
#         pisa.CreatePDF(html_report, dest=pdf_file)

#     print(f"PDF report generated: {pdf_path}")



# def process_and_generate_report(input_path, report_configs, general_options=None):
#     """
#     Cleans the data, performs analysis, and generates a customizable PDF report.

#     Parameters:
#         input_path (str): Path to a CSV file or a directory containing multiple CSV files.
#         report_configs (list): A list of dictionaries specifying report sections and their options.
#         general_options (dict): General report options like page numbering, margins, etc.

#     Returns:
#         None
#     """
    
#     # Locate the `data` directory dynamically
#     data_directory = find_directory("data")

#     # Define `reports` and `_dropped` directories
#     reports_folder = os.path.join(os.path.dirname(data_directory), "reports")
#     os.makedirs(reports_folder, exist_ok=True)
    
#     # Check if input is a file or a directory
#     if os.path.isfile(input_path):
#         csv_files = [input_path]
#         pdf_name = os.path.splitext(os.path.basename(input_path))[0] + "_report.pdf"
#         dropped_dir = os.path.join(data_directory, os.path.splitext(os.path.basename(input_path))[0] + "_dropped")
#     elif os.path.isdir(input_path):
#         csv_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".csv")]
#         pdf_name = os.path.basename(os.path.normpath(input_path)) + "_report.pdf"
#         dropped_dir = os.path.join(data_directory, os.path.basename(os.path.normpath(input_path)) + "_dropped")
#     else:
#         raise ValueError(f"The input path '{input_path}' is neither a valid file nor a directory.")

#     os.makedirs(dropped_dir, exist_ok=True)
    
    
#     # Default general options
#     if general_options is None:
#         general_options = {}


#     # Inline the CSS
#     css_path = os.path.join(os.path.dirname(__file__), "../assets/styles.css")
#     with open(css_path, "r") as css_file:
#         inline_styles = f"<style>{css_file.read()}</style>"

#     html_report = f"""
#     <html>
#         <head>
#             {inline_styles}
#             <style>
#                 @page {{
#                     size: A4;
#                     margin: 2cm;
#                     @frame footer_frame {{
#                         -pdf-frame-content: footer_content;
#                         bottom: 1cm; 
#                         left: 1cm;
#                         width: 19cm;
#                         height: 1cm;
#                     }}
#                 }}
#             </style>
#         </head>
#         <body>

#     """

#     # Generate each report section based on the configuration
#     for config in report_configs:
#         report_type = config.get("report")
#         options = config.get("options", {})

#         if report_type == "coverpage":
#             title = options.get("title", "Default Title")
#             html_report += generate_cover_page(input_path, title)

#         elif report_type == "summary":
#             if os.path.isdir(input_path):
#                 html_report += generate_summary(input_path)
        
#         elif report_type == "barcharts":
#             bar_chart_settings = {
#                 "chunk_size": options.get("chunk_size", 40),
#                 "xaxis_label": options.get("xaxis_label", "Column Names"),
#                 "yaxis_label": options.get("yaxis_label", "Unique Count"),
#             }
#             for csv_file_path in csv_files:
#                 # Load CSV data
#                 try:
#                     df = pd.read_csv(csv_file_path, index_col=0, low_memory=False)
#                 except Exception as e:
#                     print(f"Error loading file {csv_file_path}: {e}")
#                     continue

#                 # Prepare data for bar chart
#                 unique_values = {col: df[col].unique() for col in df.columns if pd.api.types.is_numeric_dtype(df[col])}
#                 chart_df = pd.DataFrame({
#                     "Column": unique_values.keys(),
#                     "Unique Count": [len(values) for values in unique_values.values()],
#                 }).sort_values(by="Unique Count", ascending=False)

#                 # Generate bar charts
#                 charts_html = generate_bar_charts(
#                     chart_df,
#                     x_axis="Column",
#                     y_axis="Unique Count",
#                     base_title=f"Unique Count of Values for {os.path.basename(csv_file_path)}",
#                     **bar_chart_settings
#                 )
#                 html_report += charts_html
        
#         elif report_type == "basicDataAnalysis":
#             for csv_file_path in csv_files:
#                 try:
#                     html_report += perform_basic_data_analysis(csv_file_path, dropped_dir)
#                 except ValueError as e:
#                     print(e)
#                     continue

#         html_report += "<div style='page-break-before: always;'></div>"

#     # Footer for page numbering (if enabled in general options)
#     if general_options.get("page_numbering", True):
#         html_report += """
#         <div id="footer_content" class="footer">
#             Page <pdf:pageNumber> of <pdf:pageCount>
#         </div>
#         """

#     # Closing HTML tags
#     html_report += "</body></html>"

#     # Create the final PDF
#     pdf_path = os.path.join(reports_folder, pdf_name)
#     with open(pdf_path, "wb") as pdf_file:
#         pisa.CreatePDF(html_report, dest=pdf_file)

#     print(f"PDF report generated: {pdf_path}")




def process_and_generate_report(input_path, report_configs, general_options=None):
    """
    Cleans the data, performs analysis, and generates a customizable PDF report.

    Parameters:
        input_path (str): Path to a CSV file or a directory containing multiple CSV files.
        report_configs (list): A list of dictionaries specifying report sections and their options.
        general_options (dict): General report options like page numbering, margins, etc.

    Returns:
        None
    """
    
    # Locate the `data` directory dynamically
    data_directory = find_directory("data")
    reports_folder = os.path.join(os.path.dirname(data_directory), "reports")
    os.makedirs(reports_folder, exist_ok=True)

    if os.path.isfile(input_path):
        pdf_name = os.path.splitext(os.path.basename(input_path))[0] + "_report.pdf"
    elif os.path.isdir(input_path):
        pdf_name = os.path.basename(os.path.normpath(input_path)) + "_report.pdf"
    else:
        raise ValueError(f"The input path '{input_path}' is neither a valid file nor a directory.")

    # Default general options
    if general_options is None:
        general_options = {}

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
    """

    # Generate each report section dynamically
    for config in report_configs:
        report_type = config.get("report")
        options = config.get("options", {})

        try:
            # Dynamically load the module
            module = importlib.import_module(f"scripts.modules.{report_type}")
            # Call the standardized function
            section_html = module.generate_report_section(input_path, options)
            html_report += section_html
        except ModuleNotFoundError:
            print(f"Module for report type '{report_type}' not found.")
        except AttributeError:
            print(f"Module '{report_type}' does not define 'generate_report_section'.")

        html_report += "<div style='page-break-before: always;'></div>"

    # Footer for page numbering (if enabled in general options)
    if general_options.get("page_numbering", True):
        html_report += """
        <div id="footer_content" class="footer">
            Page <pdf:pageNumber> of <pdf:pageCount>
        </div>
        """

    # Closing HTML tags
    html_report += "</body></html>"

    # Create the final PDF
    pdf_path = os.path.join(reports_folder, pdf_name)
    with open(pdf_path, "wb") as pdf_file:
        pisa.CreatePDF(html_report, dest=pdf_file)

    print(f"PDF report generated: {pdf_path}")
