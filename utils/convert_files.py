import os
import re
import shutil
import pandas as pd
import xml.etree.ElementTree as ET
from collections import OrderedDict
from dotenv import load_dotenv
load_dotenv(override=True)

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

def xml_to_csv(xml_directory, csv_dir):
    """
    Converts XML files in the specified directory to CSV files.

    Parameters:
        xml_directory (str): Directory containing XML files.
        csv_dir (str): Directory to save CSV files. Defaults to `csv_dir`.
    """

    os.makedirs(csv_dir, exist_ok=True)

    for filename in os.listdir(xml_directory):
        xml_path = os.path.join(xml_directory, filename)
        if not os.path.isfile(xml_path):
            continue

        print(f"Processing file: {xml_path}")
        zap_gremlins(xml_path)

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            rows = []
            for item in root:
                row = {child.tag: child.text for child in item}
                rows.append(row)

            if not rows:
                print(f"No data found in {xml_path}")
                continue

            # Create DataFrame and clean
            df = pd.DataFrame(rows)
            df = df.iloc[1:, 1:]  # Drop first row and first column

            # Save CSV
            base_name = os.path.splitext(filename)[0]
            csv_path = os.path.join(csv_dir, f"{base_name}.csv")
            df.to_csv(csv_path, index=False)

            print(f"Converted {xml_path} to {csv_path}")

        except ET.ParseError as e:
            print(f"Error parsing {xml_path}: {e}")

def convert_excel_to_csv(excel_directory, csv_dir):
    """
        Converts all .xls and .xlsx files in a directory to CSV format.
    """            
    os.makedirs(csv_dir, exist_ok=True)

    for filename in os.listdir(excel_directory):
        file_path = os.path.join(excel_directory, filename)
        
        if os.path.isfile(file_path) and filename.endswith(('.xls', '.xlsx')):
            print(f"Processing file: {file_path}")
            
            try:
                # Use openpyxl for .xlsx files and fallback to xlrd for .xls
                engine = 'openpyxl' if filename.endswith('.xlsx') else 'xlrd'
                df = pd.read_excel(file_path, engine=engine)
                                
                base_filename = os.path.splitext(filename)[0]
                output_file = os.path.join(csv_dir, f"{base_filename}.csv")
                
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

    def process_file(file_path, output_dir):
        if file_path.endswith(('.xls', '.xlsx')):
            convert_excel_to_csv_all_sheets(file_path, output_dir)
        elif file_path.endswith('.xml'):
            xml_to_csv(os.path.dirname(file_path), output_dir)
        elif file_path.endswith('.csv'):
            dest = os.path.join(output_dir, os.path.basename(file_path))
            if file_path != dest:
                shutil.copy2(file_path, dest)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

    if os.path.isfile(path):
        base_name = os.path.splitext(os.path.basename(path))[0]
        out_dir = os.path.join(csv_root, base_name)
        os.makedirs(out_dir, exist_ok=True)
        process_file(path, out_dir)
        return (out_dir if not path.endswith('.csv') else os.path.join(out_dir, os.path.basename(path)), base_name)

    elif os.path.isdir(path):
        base_name = os.path.basename(os.path.normpath(path))
        out_dir = os.path.join(csv_root, base_name)
        os.makedirs(out_dir, exist_ok=True)
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                process_file(full_path, out_dir)
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