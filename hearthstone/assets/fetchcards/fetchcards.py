from io import BytesIO

import pandas as pd
import requests
from . import hearthstone_api
from dagster import AssetExecutionContext, AssetMaterialization, MetadataValue, asset


@asset
def get_hearthstone_cards(context):
    deck = hearthstone_api.get_all_hearthstone_cards(context)
    first_card = deck['cards'][0]
    context.log.info(first_card)

    markdown_list = "\n".join([f"- {key}" for key in first_card.keys()])

    metadata_dict = {
        "key_values": MetadataValue.md(markdown_list),
        "example_image_url": MetadataValue.md(f"![Card Image]({first_card['image']['en_US']})")
    }
    context.add_output_metadata(metadata=metadata_dict)


# @asset
# def get_hearthstone_cards(context):
#     file_url = "https://www.lyfjastofnun.is/wp-content/uploads/2024/02/lyf-med-markadsleyfi-0224.xlsx"
#     response = requests.get(file_url)
#     df = pd.read_excel(BytesIO(response.content))
#     context.log.info(f"Read {len(df)} rows from Excel file.")

#     # Convert DataFrame to Markdown
#     markdown_str = df.head(5).to_markdown()  # Convert first 5 rows to Markdown

#     # Log metadata and materialize the asset
#     metadata_dict = {
#         # "column_names": list(df.columns),
#         "row_count": len(df),
#         "preview": MetadataValue.md(markdown_str),
#     }
#     context.add_output_metadata(metadata=metadata_dict)
#     context.log.info("Exported DataFrame to Markdown format")

#     return df


