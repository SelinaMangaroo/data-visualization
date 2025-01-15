import os
import plotly.express as px
import pandas as pd
from io import BytesIO
import base64

# def generate_bar_charts(chart_df, x_axis, y_axis, base_title="", chunk_size=40, xaxis_label="X-Axis", yaxis_label="Y-Axis"):
#     """
#     Generates bar charts in chunks and returns the HTML content for embedding in the report.

#     Parameters:
#         chart_df (DataFrame): DataFrame containing the data to chart.
#         x_axis (str): The column name to use for the x-axis.
#         y_axis (str): The column name to use for the y-axis.
#         base_title (str): Base title for the charts.
#         chunk_size (int): Maximum number of bars per chart.
#         xaxis_label (str): Label for the x-axis.
#         yaxis_label (str): Label for the y-axis.

#     Returns:
#         str: HTML content with embedded bar charts.
#     """
#     charts_html = ""
#     for i in range(0, len(chart_df), chunk_size):
#         chunk = chart_df.iloc[i:i + chunk_size]
#         part_number = (i // chunk_size) + 1

#         # Generate the bar chart
#         fig = px.bar(
#             chunk,
#             x=x_axis,
#             y=y_axis,
#             text=y_axis,
#             title=f"{base_title} (Part {part_number})"
#         )
#         fig.update_traces(textposition="outside")
#         fig.update_layout(
#             xaxis=dict(tickangle=-45),
#             height=600,
#             margin=dict(l=50, r=50, t=50, b=150),
#             xaxis_title=xaxis_label,
#             yaxis_title=yaxis_label,
#         )

#         # Save the chart image to memory as Base64
#         buffer = BytesIO()
#         fig.write_image(buffer, format="png")
#         buffer.seek(0)
#         image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
#         buffer.close()

#         # Append the chart to the charts_html string
#         charts_html += f"""
#             <h2 class="sub-header"></h2>
#             <img src="data:image/png;base64,{image_base64}" alt="Bar Chart Part {part_number}">
#         """
#     return charts_html

import os
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64


import os
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64


def generate_report_section(input_path, options=None, **kwargs):
    """
    Generates bar charts for one or more datasets and returns HTML content for embedding in a report.

    Parameters:
        input_path (str): Path to the CSV file or directory containing CSV files.
        options (dict): Options for customizing the bar charts.

    Returns:
        str: HTML content with embedded bar charts.
    """
    options = options or {}
    chunk_size = options.get("chunk_size", 40)
    xaxis_label = options.get("xaxis_label", "Column Names")
    yaxis_label = options.get("yaxis_label", "Unique Count")
    base_title = options.get("base_title", "Bar Chart")

    # Check if the input path is a file or directory
    if os.path.isfile(input_path):
        csv_files = [input_path]
    elif os.path.isdir(input_path):
        csv_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".csv")]
    else:
        raise ValueError("The input path must be a CSV file or a directory containing CSV files.")

    charts_html = ""

    # Process each CSV file
    for csv_file_path in csv_files:
        try:
            # Load CSV data
            df = pd.read_csv(csv_file_path, index_col=0, low_memory=False)

            # Prepare data for bar chart
            unique_values = {
                col: df[col].unique() for col in df.columns if pd.api.types.is_numeric_dtype(df[col])
            }
            chart_df = pd.DataFrame({
                "Column": unique_values.keys(),
                "Unique Count": [len(values) for values in unique_values.values()],
            }).sort_values(by="Unique Count", ascending=False)

            # Generate bar charts
            for i in range(0, len(chart_df), chunk_size):
                chunk = chart_df.iloc[i:i + chunk_size]
                part_number = (i // chunk_size) + 1

                # Generate the bar chart
                fig = px.bar(
                    chunk,
                    x="Column",
                    y="Unique Count",
                    text="Unique Count",
                    title=f"{base_title} ({os.path.basename(csv_file_path)} - Part {part_number})"
                )
                fig.update_traces(textposition="outside")
                fig.update_layout(
                    xaxis=dict(tickangle=-45),
                    height=600,
                    margin=dict(l=50, r=50, t=50, b=150),
                    xaxis_title=xaxis_label,
                    yaxis_title=yaxis_label,
                )

                # Save the chart image to memory as Base64
                buffer = BytesIO()
                fig.write_image(buffer, format="png")
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
                buffer.close()

                # Append the chart to the charts_html string
                charts_html += f"""
                    <h2 class="sub-header">Bar Chart (Part {part_number})</h2>
                    <img src="data:image/png;base64,{image_base64}" alt="Bar Chart Part {part_number}">
                """

        except Exception as e:
            print(f"Error processing file {csv_file_path}: {e}")
            continue

    return charts_html
