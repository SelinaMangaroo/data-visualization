import os
import datetime
import base64
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

def generate_report_section(input_path, options=None, **kwargs):
    """
    Generates HTML content for the cover page.

    Parameters:
        input_path (str): Path to the input file or directory.
        options (dict): Options for generating the cover page (e.g., title).

    Returns:
        str: HTML content for the cover page.
    """
    options = options or {}
    title = options.get("title", "Default Title")

    # Determine the name of the file/directory
    if os.path.isfile(input_path):
        input_name = os.path.basename(input_path)
        file_size = os.path.getsize(input_path) / (1024 * 1024)  # Size in MB
    elif os.path.isdir(input_path):
        input_name = os.path.basename(os.path.normpath(input_path))
        # Calculate total size of all files in the directory
        file_size = sum(
            os.path.getsize(os.path.join(input_path, f))
            for f in os.listdir(input_path)
            if os.path.isfile(os.path.join(input_path, f))
        )
        file_size /= (1024 * 1024)  # Size in MB
    else:
        raise ValueError("Invalid input path.")
    
    # Read and encode the logo from the path in .env
    logo_path = os.getenv("LOGO_PATH", "")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as logo_file:
            encoded_logo = base64.b64encode(logo_file.read()).decode("utf-8")
        logo_html = f'<img src="data:image/png;base64,{encoded_logo}" alt="Report Logo">'
    else:
        logo_html = ''

    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    # Generate the HTML content for the cover page
    cover_page_html = f"""
    <div class="cover-page-container">
        <div class="cover-page">
            {logo_html}
            <p><strong>Report for:</strong> {title}</p>
            <p><strong>Input Name:</strong> {input_name}</p>
            <p><strong>Generated On:</strong> {current_datetime}</p>
            <p><strong>File Size:</strong> {file_size:.2f} MB</p>
        </div>
    </div>
    """
    return cover_page_html
