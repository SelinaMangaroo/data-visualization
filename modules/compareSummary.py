import os
import pandas as pd
from collections import defaultdict
from dotenv import load_dotenv
import logging

logger = logging.getLogger("report")
load_dotenv(override=True)

def generate_report_section(input_path, options=None, **kwargs):
    """
    Compares column value counts across multiple CSV files and outputs a summary table
    highlighting only the columns where counts differ.
    """
    options = options or {}

    if os.path.isfile(input_path):
        return "<p>compareSummary requires a directory input with multiple CSV files.</p>"

    csv_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".csv")]
    if len(csv_files) < 2:
        return "<p>Not enough CSV files to compare.</p>"

    column_counts = defaultdict(dict)
    all_columns = set()

    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, index_col=0, low_memory=False)
            file_name = os.path.basename(csv_file)
            value_counts = df.count()  # Non-null count per column

            for col in df.columns:
                count = value_counts.get(col, 0)
                column_counts[col][file_name] = count
                all_columns.add(col)

        except Exception as e:
            logger.exception(f"Error reading {csv_file}: {e}")
            continue

    # Filter only columns with differing counts
    differing_columns = {
        col: counts for col, counts in column_counts.items()
        if len(set(counts.values())) > 1
    }

    if not differing_columns:
        return "<p>All columns have consistent value counts across files.</p>"

    sorted_files = sorted({file for counts in differing_columns.values() for file in counts})
    
    # Build HTML table
    header_row = "<tr><th>Column</th>" + "".join(f"<th>{f}</th>" for f in sorted_files) + "</tr>"
    body_rows = ""

    for col, counts in sorted(differing_columns.items()):
        row = f"<tr><td>{col}</td>" + "".join(
            f"<td>{counts.get(f, 0)}</td>" for f in sorted_files
        ) + "</tr>"
        body_rows += row

    html = f"""
    <div class="section-block">
        <h1 class="header">Compare Summary: Column Value Count Differences</h1>
        <table class="value-counts-table">
            <thead>{header_row}</thead>
            <tbody>{body_rows}</tbody>
        </table>
    </div>
    """

    return html + "<div class='page-break'></div>"