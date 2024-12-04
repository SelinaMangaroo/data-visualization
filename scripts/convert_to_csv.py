import os
import xml.etree.ElementTree as ET
import pandas as pd
from collections import OrderedDict
import re

"""
    Cleans the content of an XML file by removing non-printable or malformed characters.
"""
def zap_gremlins(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    
        # print(f"zapping gremlins: {file_path}")

    # Remove control characters except newlines and tabs
    cleaned_content = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', content)

    # Overwrite the file with cleaned content
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)
        
        
        
"""
    Converts XML files in the specified directory to CSV files in another directory.

    Parameters:
    xml_directory (str): Path to the directory containing XML files.
    csv_directory (str): Optional Path to the directory where CSV files will be saved.
"""
def xml_to_csv(xml_directory, csv_directory=None):
    
    # Determine the CSV directory if not provided
    if not csv_directory:
        csv_directory = f"{xml_directory.rstrip(os.sep)}_csv"

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

"""
    Converts all .xls and .xlsx files in a directory to CSV format.
"""            
def convert_excel_to_csv(directory, output_directory=None):
    if not output_directory:
        output_directory = f"{directory.rstrip(os.sep)}_csv"

    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path) and filename.endswith(('.xls', '.xlsx')):
            print(f"Processing file: {file_path}")
            
            try:
                # Use openpyxl for .xlsx files and fallback to xlrd for .xls
                engine = 'openpyxl' if filename.endswith('.xlsx') else 'xlrd'
                df = pd.read_excel(file_path, engine=engine)
                
                # df = pd.read_excel(file_path, engine='xlrd')
                
                base_filename = os.path.splitext(filename)[0]
                output_file = os.path.join(output_directory, f"{base_filename}.csv")
                
                df.to_csv(output_file, index=False)
                print(f"Converted {file_path} to {output_file}")
            
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                