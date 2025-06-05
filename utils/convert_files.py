import os
import re
import shutil
import pandas as pd
import xml.etree.ElementTree as ET
from collections import OrderedDict
from dotenv import load_dotenv
load_dotenv()

csv_dir = os.getenv("CSV_DIR", "")

def zap_gremlins(file_path):
    """
        Cleans the content of an XML file by removing non-printable or malformed characters.
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Remove control characters except newlines and tabs
    cleaned_content = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', content)

    # Overwrite the file with cleaned content
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)
        
def xml_to_csv(xml_directory, csv_directory=None):
    """
        Converts XML files in the specified directory to CSV files in another directory.

        Parameters:
        xml_directory (str): Path to the directory containing XML files.
        csv_directory (str): Optional Path to the directory where CSV files will be saved.
    """
    
    # Determine the CSV directory if not provided
    if not csv_directory:
        # csv_directory = f"{xml_directory.rstrip(os.sep)}_csv"
        csv_directory = csv_dir

    # Ensure the CSV directory exists
    os.makedirs(csv_directory, exist_ok=True)

    for filename in os.listdir(xml_directory):
        xml_file_path = os.path.join(xml_directory, filename)
        if os.path.isfile(xml_file_path):
            print(f"Processing file: {xml_file_path}")
            
            # Clean the XML file
            zap_gremlins(xml_file_path)

            try:
                # Parse the cleaned XML file
                tree = ET.parse(xml_file_path)
                root = tree.getroot()
                
                cols = []
                rows = []

                for x in root:
                    d = {}
                    for y in x:
                        cols.append(y.tag)
                        d["{0}".format(y.tag)] = y.text
                    rows.append(d)

                # Remove repeated columns
                cols = list(OrderedDict.fromkeys(cols))

                # Create DataFrame
                df = pd.DataFrame(rows, columns=cols)

                # Drop first column and row
                df = df.iloc[1:]
                df = df.iloc[:, 1:]

                # Generate output CSV file path
                base_filename = os.path.splitext(filename)[0]
                csv_file_path = os.path.join(csv_directory, f'{base_filename}.csv')

                # Write DataFrame to CSV
                df.to_csv(csv_file_path, index=False)

                print(f"Converted {xml_file_path} to {csv_file_path}")

            except ET.ParseError as e:
                # Log the error and skip the file
                print(f"Error parsing {xml_file_path}: {e}")
                continue  # Skip to the next file

def convert_excel_to_csv(directory, output_directory=None):
    """
        Converts all .xls and .xlsx files in a directory to CSV format.
    """            
    if not output_directory:
        output_directory = csv_dir

    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path) and filename.endswith(('.xls', '.xlsx')):
            print(f"Processing file: {file_path}")
            
            try:
                # Use openpyxl for .xlsx files and fallback to xlrd for .xls
                engine = 'openpyxl' if filename.endswith('.xlsx') else 'xlrd'
                df = pd.read_excel(file_path, engine=engine)
                                
                base_filename = os.path.splitext(filename)[0]
                output_file = os.path.join(output_directory, f"{base_filename}.csv")
                
                df.to_csv(output_file, index=False)
                print(f"Converted {file_path} to {output_file}")
            
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

def auto_convert_to_csv(path):
    """
    Converts supported file types (Excel/XML) to CSV.
    Returns (converted_path, base_name).
    """
    csv_root = os.getenv("CSV_DIR", "data_csv")
    os.makedirs(csv_root, exist_ok=True)

    if os.path.isfile(path):
        base_name = os.path.splitext(os.path.basename(path))[0]
        subfolder = os.path.join(csv_root, base_name)
        os.makedirs(subfolder, exist_ok=True)

        if path.endswith(('.xls', '.xlsx')):
            convert_excel_to_csv_all_sheets(path, subfolder)
            return subfolder, base_name
        elif path.endswith('.xml'):
            xml_to_csv(os.path.dirname(path), subfolder)
            return subfolder, base_name
        elif path.endswith('.csv'):
            dest_path = os.path.join(subfolder, os.path.basename(path))
            if path != dest_path:
                shutil.copy2(path, dest_path)
            return dest_path, base_name
        else:
            raise ValueError(f"Unsupported file format: {path}")

    elif os.path.isdir(path):
        base_name = os.path.basename(os.path.normpath(path))
        out_dir = os.path.join(csv_root, base_name)
        os.makedirs(out_dir, exist_ok=True)

        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                if file.endswith(('.xls', '.xlsx')):
                    convert_excel_to_csv_all_sheets(full_path, out_dir)
                elif file.endswith('.xml'):
                    xml_to_csv(path, out_dir)
                elif file.endswith('.csv'):
                    dest_path = os.path.join(out_dir, file)
                    if full_path != dest_path:
                        shutil.copy2(full_path, dest_path)

        return out_dir, base_name

    else:
        raise FileNotFoundError(f"Path does not exist: {path}")


def convert_excel_to_csv_all_sheets(file_path, output_directory):
    """
        Converts all sheets of an Excel file into separate CSV files.
    """
    excel_file = pd.ExcelFile(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    os.makedirs(output_directory, exist_ok=True)

    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)
        safe_sheet = re.sub(r'[^a-zA-Z0-9_-]', '_', sheet_name)
        output_path = os.path.join(output_directory, f"{base_name}_{safe_sheet}.csv")
        df.to_csv(output_path, index=False)
        print(f"Converted sheet '{sheet_name}' from {file_path} to {output_path}")