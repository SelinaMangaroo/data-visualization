import os
import pandas as pd
import numpy as np

# def perform_basic_data_analysis(csv_file_path, dropped_dir):
#     """
#     Performs basic data analysis on a CSV file and generates HTML content for the report.

#     Parameters:
#         csv_file_path (str): Path to the CSV file to analyze.
#         dropped_dir (str): Directory to save the cleaned CSV file.

#     Returns:
#         str: HTML content for the analysis report.
#     """
#     try:
#         # Load CSV data
#         df = pd.read_csv(csv_file_path, index_col=0, low_memory=False)
#     except Exception as e:
#         raise ValueError(f"Error loading file {csv_file_path}: {e}")

#     # Perform data analysis
#     original_columns = df.columns.tolist()
#     original_row_count = df.shape[0]
#     empty_row_count = df.isnull().all(axis=1).sum()
#     df = df.dropna(axis=1, how="all")
#     current_columns = df.columns.tolist()
#     dropped_columns = [col for col in original_columns if col not in current_columns]
#     column_value_counts = df.count()
#     unique_values = {col: np.atleast_1d(df[col].unique()) for col in current_columns}
#     columns_with_zeros = {
#         col: (df[col] == 0).sum() > 0
#         for col in current_columns
#         if not pd.api.types.is_numeric_dtype(df[col])
#     } 

#     # Save the cleaned DataFrame
#     base_file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
#     dropped_csv_path = os.path.join(dropped_dir, f"{base_file_name}_dropped.csv")
#     df.to_csv(dropped_csv_path, index=False)

#     # Generate table rows for column value counts
#     col_value_table_rows = "".join(
#         f"<tr><td>{col}</td><td>{count}</td></tr>"
#         for col, count in column_value_counts.items()
#     )

#     # Column counts table
#     column_counts_table = f"""
#     <h2 class="sub-header">Column Value Counts:</h2>
#     <table class="value-counts-table">
#         <thead>
#             <tr>
#                 <th>Column</th>
#                 <th>Value Count</th>
#             </tr>
#         </thead>
#         <tbody>
#             {col_value_table_rows}
#         </tbody>
#     </table>
#     """

#     # Columns with Zeros section
#     columns_with_zeros_list = [
#         col for col, has_zeros in columns_with_zeros.items() if has_zeros
#     ]
#     columns_with_zeros_html = (
#         f"<h2 class='sub-header'>Columns with Zeros:</h2><p>{', '.join(columns_with_zeros_list)}</p>"
#         if columns_with_zeros_list
#         else ""
#     )

#     # Combine all sections into HTML
#     analysis_html = f"""
#     <h1 class="header">Report for {base_file_name}</h1>
#     <h2 class="sub-header">Dropped Columns ({len(dropped_columns)}):</h2>
#     <p>{', '.join(dropped_columns) if dropped_columns else "None"}</p>
#     <h2 class="sub-header">Current Columns ({len(current_columns)}):</h2>
#     <p>{', '.join(current_columns)}</p>
#     <h2 class="sub-header">Number of Rows:</h2>
#     <p>{original_row_count}</p>
#     <h2 class="sub-header">Number of Empty Rows:</h2>
#     <p>{empty_row_count}</p>
#     {column_counts_table}
#     {columns_with_zeros_html}
#     """

#     return analysis_html


def generate_report_section(input_path, options=None, **kwargs):
    """
    Performs basic data analysis on CSV files and generates HTML content for the report.

    Parameters:
        input_path (str): Path to the CSV file or directory containing CSV files.
        options (dict): Additional options for customization.

    Returns:
        str: HTML content for the analysis report.
    """
    options = options or {}

    # Define the dropped directory logic
    if os.path.isfile(input_path):
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        data_directory = os.path.dirname(input_path)
    elif os.path.isdir(input_path):
        base_name = os.path.basename(os.path.normpath(input_path))
        data_directory = input_path
    else:
        raise ValueError("The input path must be a CSV file or a directory containing CSV files.")

    dropped_dir = os.path.join(data_directory, f"{base_name}_dropped")
    os.makedirs(dropped_dir, exist_ok=True)

    # Check if the input path is a file or directory
    csv_files = [input_path] if os.path.isfile(input_path) else [
        os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".csv")
    ]

    analysis_html = ""

    # Process each CSV file
    for csv_file_path in csv_files:
        try:
            # Load CSV data
            df = pd.read_csv(csv_file_path, index_col=0, low_memory=False)

            # Perform data analysis
            original_columns = df.columns.tolist()
            original_row_count = df.shape[0]
            empty_row_count = df.isnull().all(axis=1).sum()
            df = df.dropna(axis=1, how="all")
            current_columns = df.columns.tolist()
            dropped_columns = [col for col in original_columns if col not in current_columns]
            column_value_counts = df.count()
            unique_values = {col: np.atleast_1d(df[col].unique()) for col in current_columns}
            columns_with_zeros = {
                col: (df[col] == 0).sum() > 0
                for col in current_columns
                if pd.api.types.is_numeric_dtype(df[col])
            }

            # Save the cleaned DataFrame
            base_file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
            cleaned_csv_path = os.path.join(dropped_dir, f"{base_file_name}_cleaned.csv")
            df.to_csv(cleaned_csv_path, index=False)

            # Generate table rows for column value counts
            col_value_table_rows = "".join(
                f"<tr><td>{col}</td><td>{count}</td></tr>"
                for col, count in column_value_counts.items()
            )

            # Column counts table
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

            # Columns with Zeros section
            columns_with_zeros_list = [
                col for col, has_zeros in columns_with_zeros.items() if has_zeros
            ]
            columns_with_zeros_html = (
                f"<h2 class='sub-header'>Columns with Zeros:</h2><p>{', '.join(columns_with_zeros_list)}</p>"
                if columns_with_zeros_list
                else ""
            )

            # Combine all sections into HTML
            analysis_html += f"""
            <h1 class="header">Report for {base_file_name}</h1>
            <h2 class="sub-header">Dropped Columns ({len(dropped_columns)}):</h2>
            <p>{', '.join(dropped_columns) if dropped_columns else "None"}</p>
            <h2 class="sub-header">Current Columns ({len(current_columns)}):</h2>
            <p>{', '.join(current_columns)}</p>
            <h2 class="sub-header">Number of Rows:</h2>
            <p>{original_row_count}</p>
            <h2 class="sub-header">Number of Empty Rows:</h2>
            <p>{empty_row_count}</p>
            {column_counts_table}
            {columns_with_zeros_html}
            <div style="page-break-before: always;"></div>
            """

        except Exception as e:
            print(f"Error processing file {csv_file_path}: {e}")
            continue

    return analysis_html
