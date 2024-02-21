from io import BytesIO

import pandas as pd
import requests

from dagster import AssetExecutionContext, AssetMaterialization, MetadataValue, asset


@asset
def read_excel_file(context):
    file_url = "https://www.lyfjastofnun.is/wp-content/uploads/2024/02/lyf-med-markadsleyfi-0224.xlsx"
    response = requests.get(file_url)
    df = pd.read_excel(BytesIO(response.content))
    context.log.info(f"Read {len(df)} rows from Excel file.")

    # Convert DataFrame to Markdown
    markdown_str = df.head(5).to_markdown()  # Convert first 5 rows to Markdown

    # Log metadata and materialize the asset
    metadata_dict = {
        # "column_names": list(df.columns),
        "row_count": len(df),
        "preview": MetadataValue.md(markdown_str),
    }
    context.add_output_metadata(metadata=metadata_dict)
    context.log.info("Exported DataFrame to Markdown format")

    return df
