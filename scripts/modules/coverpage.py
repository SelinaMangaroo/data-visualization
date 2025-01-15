import os
import datetime

# def generate_cover_page(input_path, title="Default Title"):
#     """
#     Generates HTML content for the cover page.

#     Parameters:
#         input_path (str): Path to the input file or directory.

#     Returns:
#         str: HTML content for the cover page.
#     """
#     # Determine the name of the file/directory
#     if os.path.isfile(input_path):
#         input_name = os.path.basename(input_path)
#         file_size = os.path.getsize(input_path) / (1024 * 1024)  # Size in MB
#     elif os.path.isdir(input_path):
#         input_name = os.path.basename(os.path.normpath(input_path))
#         # Calculate total size of all files in the directory
#         file_size = sum(os.path.getsize(os.path.join(input_path, f)) 
#         for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)))
#         file_size /= (1024 * 1024)  # Size in MB
#     else:
#         raise ValueError("Invalid input path.")

#     # Get the current date and time
#     current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # Generate the HTML content for the cover page
#     cover_page_html = f"""
#     <div class="cover-page-container">
#         <div class="cover-page">
#             <img src="../assets/CA_Logo.png" alt="Collective Access Logo">
#             <p><strong>Report for:</strong> {title}</p>
#             <p><strong>Generated On:</strong> {current_datetime}</p>
#             <p><strong>File Size:</strong> {file_size:.2f} MB</p>
#         </div>
#     </div>
#     """
#     return cover_page_html


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

    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate the HTML content for the cover page
    cover_page_html = f"""
    <div class="cover-page-container">
        <div class="cover-page">
            <img src="../assets/CA_Logo.png" alt="Collective Access Logo">
            <p><strong>Report for:</strong> {title}</p>
            <p><strong>Input Name:</strong> {input_name}</p>
            <p><strong>Generated On:</strong> {current_datetime}</p>
            <p><strong>File Size:</strong> {file_size:.2f} MB</p>
        </div>
    </div>
    """
    return cover_page_html
