import os
import importlib
from xhtml2pdf import pisa
from utils.convert_files import *
from utils.load_config import load_report_config
from dotenv import load_dotenv
from utils.logger import setup_logger

logger = setup_logger("main")
load_dotenv(override=True)

def process_and_generate_report(report_configs=None, general_options=None):
    """
    Generates a PDF report from specified input and modular components.
    """
    general_options = general_options or {}
    logger.info("Report generation started.")
    # Pull from .env if not passed directly
    raw_path = os.getenv("DATA_PATH")
    input_path, base_name = auto_convert_to_csv(raw_path)
    logger.info(f"Input path resolved to: {input_path}")
    
    reports_folder = os.getenv("REPORTS_DIR", "./reports")
    css_path = os.getenv("REPORT_CSS_PATH", "./assets/styles.css")
    module_path = os.getenv("REPORT_MODULE_PATH", "modules")

    # Validate paths
    if not input_path:
        logger.error("CONVERTED_DATA_PATH not set in .env.")
        raise ValueError("CONVERTED_DATA_PATH not set in .env.")
    if not os.path.exists(css_path):
        logger.error(f"CSS file not found at: {css_path}")
        raise FileNotFoundError(f"CSS file not found at: {css_path}")
    if not report_configs:
        logger.error("No report configurations provided.")
        raise ValueError("No report configurations provided.")
    
    # Ensure reports output directory exists
    os.makedirs(reports_folder, exist_ok=True)

    pdf_name = f"{base_name}_report.pdf"
    
    # Inline the CSS for xhtml2pdf
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

    # Add each modular report section
    for config in report_configs:
        report_type = config.get("report")
        options = config.get("options", {})

        try:
            logger.info(f"Generating report section: {report_type}")
            module = importlib.import_module(f"{module_path}.{report_type}")
            
            # Determine if this module needs a directory (e.g., 'summary')
            if report_type == "summary" and os.path.isfile(input_path):
                input_for_module = os.path.dirname(input_path)
            else:
                input_for_module = input_path

            section_html = module.generate_report_section(input_for_module, options)            
            html_report += section_html
            logger.info(f"Successfully rendered section: {report_type}")
        except ModuleNotFoundError:
            logger.error(f"Report module '{report_type}' not found.")
        except AttributeError:
            logger.error(f"'{report_type}' module missing 'generate_report_section'.")
        except Exception as e:
            logger.exception(f"Failed to generate section '{report_type}': {e}")

        html_report += "<div style='page-break-before: always;'></div>"

    # Optional footer
    if general_options.get("page_numbering", True):
        html_report += """
        <div id="footer_content" class="footer">
            Page <pdf:pageNumber> of <pdf:pageCount>
        </div>
        """

    html_report += "</body></html>"

    # Write the final PDF
    pdf_path = os.path.join(reports_folder, pdf_name)
    with open(pdf_path, "wb") as pdf_file:
        pisa.CreatePDF(html_report, dest=pdf_file)

    logger.info(f"PDF report successfully generated at: {pdf_path}")

if __name__ == "__main__":
    print("Script is running")
    config_path = os.getenv("REPORT_CONFIG_PATH", "report_config.json")
    logger.info(f"Loading report configuration from: {config_path}")

    try:
        process_and_generate_report(
            report_configs=load_report_config(config_path),
            general_options={"page_numbering": os.getenv("PAGE_NUMBERING", "true").lower() == "true"}
        )
    except Exception as e:
        logger.exception(f"Fatal error: {e}")