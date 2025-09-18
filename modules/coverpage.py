import os
import datetime
import base64
import mimetypes
import logging
from dotenv import load_dotenv

logger = logging.getLogger("report")
load_dotenv(override=True)

def generate_report_section(input_path, options=None, **kwargs):
    """
    Generates HTML content for the cover page.
    """
    options = options or {}
    title = options.get("title", "Default Title")

    # Determine the name of the file/directory
    if os.path.isfile(input_path):
        input_name = os.path.basename(input_path)
        file_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
    elif os.path.isdir(input_path):
        input_name = os.path.basename(os.path.normpath(input_path))
        file_size = sum(
            os.path.getsize(os.path.join(input_path, f))
            for f in os.listdir(input_path)
            if os.path.isfile(os.path.join(input_path, f))
        ) / (1024 * 1024)
    else:
        raise ValueError("Invalid input path.")
    
    # Read and encode logo from .env path
    logo_path = os.getenv("LOGO_PATH", "")
    logo_html = ""
    if os.path.exists(logo_path):
        mime_type, _ = mimetypes.guess_type(logo_path)
        if mime_type:
            with open(logo_path, "rb") as logo_file:
                encoded_logo = base64.b64encode(logo_file.read()).decode("utf-8")
            logo_html = f'<img src="data:{mime_type};base64,{encoded_logo}" alt="Report Logo">'
        else:
            logger.warning(f"Could not determine MIME type for logo: {logo_path}")

    # Current datetime
    current_datetime = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    # Generate HTML
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
    <div class="page-break"></div>
    """

    logger.info("Cover page generated successfully.")
    return cover_page_html
