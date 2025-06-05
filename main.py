# import os
# import sys
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Add project to sys.path
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# from utils.convert_files import *
# from report import *

# # Get env variables
# data_path = os.getenv("DATA_PATH")
# converted_data_path = os.getenv("CONVERTED_DATA_PATH")

# # Report options
# report_title = os.getenv("REPORT_TITLE", "Data Report")
# chunk_size = int(os.getenv("CHUNK_SIZE", 40))
# xaxis_label = os.getenv("XAXIS_LABEL", "Column")
# yaxis_label = os.getenv("YAXIS_LABEL", "Unique Count")
# page_numbering = os.getenv("PAGE_NUMBERING", "True").lower() == "true"

# # Generate full PDF report
# process_and_generate_report(
#     input_path=converted_data_path,
#     report_configs=[
#         {"report": "coverpage", "options": {"title": report_title}},
#         {"report": "summary", "options": {}},
#         {"report": "barcharts", "options": {
#             "chunk_size": chunk_size,
#             "xaxis_label": xaxis_label,
#             "yaxis_label": yaxis_label
#         }},
#         {"report": "basicDataAnalysis", "options": {}}
#     ],
#     general_options={"page_numbering": page_numbering}
# )