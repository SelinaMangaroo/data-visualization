import pandas as pd
import os

# def generate_summary(directory):
#     """
#     Generates the HTML content for a summary page using xhtml2pdf.

#     Parameters:
#         directory (str): Path to the directory containing multiple CSV files.
#     Returns:
#         str: HTML content for the summary.
#     """
#     # Ensure the directory exists and contains CSV files
#     if not os.path.isdir(directory):
#         raise ValueError(f"The directory '{directory}' does not exist or is not a directory.")

#     csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")]
#     if not csv_files:
#         raise ValueError(f"No CSV files found in the directory '{directory}'.")

#     # Initialize summary data
#     all_columns = set()
#     file_columns = {}
#     stats = []

#     # Collect data from all files
#     for csv_file_path in csv_files:
#         base_file_name = os.path.basename(csv_file_path)

#         # Load the dataset
#         try:
#             df = pd.read_csv(csv_file_path, index_col=0, low_memory=False)
#         except Exception as e:
#             print(f"Error loading file {csv_file_path}: {e}")
#             continue

#         # Collect columns and compute stats
#         total_columns = df.columns.tolist()
#         dropped_columns = len(df.columns[df.isnull().all()])
#         number_of_rows = df.shape[0]

#         file_columns[base_file_name] = total_columns
#         all_columns.update(total_columns)

#         stats.append({
#             "File": base_file_name,
#             "Total Columns": len(total_columns),
#             "Dropped Columns": dropped_columns,
#             "Rows": number_of_rows,
#         })

#     # Generate HTML content
#     html_content = f"""
#     <h1 class="header">Summary of Processed Files</h1>
#     <h2 class="sub-header">Summary Statistics:</h2>
#     <table class="summary-table">
#         <thead>
#             <tr>
#                 <th>File</th>
#                 <th>Total Columns</th>
#                 <th>Dropped Columns</th>
#                 <th>Number of Rows</th>
#             </tr>
#         </thead>
#         <tbody>
#     """

#     for stat in stats:
#         html_content += f"""
#             <tr>
#                 <td>{stat['File']}</td>
#                 <td>{stat['Total Columns']}</td>
#                 <td>{stat['Dropped Columns']}</td>
#                 <td>{stat['Rows']}</td>
#             </tr>
#         """
    
#     html_content += """
#         </tbody>
#     </table>
#     <h2 class="sub-header">Column Presence Across Files:</h2>
#     <table class="column-table">
#         <thead>
#             <tr>
#                 <th>Column</th>
#                 <th>Files Containing Column</th>
#             </tr>
#         </thead>
#         <tbody>
#     """

#     for column in sorted(all_columns):
#         files_with_column = [file for file, cols in file_columns.items() if column in cols]
#         html_content += f"""
#         <tr>
#             <td>{column}</td>
#             <td>{', '.join(files_with_column)}</td>
#         </tr>
#         """

#     html_content += """
#         </tbody>
#     </table>
#     """
#     return html_content

def generate_report_section(input_path, options=None, **kwargs):
    """
    Generates the HTML content for a summary page.

    Parameters:
        input_path (str): Path to the directory containing multiple CSV files.
        options (dict): Options for customizing the summary generation.

    Returns:
        str: HTML content for the summary.
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
