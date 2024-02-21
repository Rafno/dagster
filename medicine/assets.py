import pandas as pd
from dagster import AssetExecutionContext, AssetMaterialization, MetadataValue, asset


@asset
def get_meds(context: AssetExecutionContext) -> None:
    """
    Get data
    """
    # Load data using Pandas
    meds_df = pd.read_csv("/opt/dagster/data/meds.csv", header=1, skiprows=0)

    context.log.info(f"Read {len(meds_df)} rows from meds.csv")

    # Convert DataFrame to Markdown
    markdown_str = meds_df.head(5).to_markdown()  # Convert first 5 rows to Markdown

    # Log metadata and materialize the asset
    metadata_dict = {
        "column_names": list(meds_df.columns),
        "row_count": len(meds_df),
        "preview": MetadataValue.md(markdown_str),
    }
    context.add_output_metadata(metadata=metadata_dict)
    context.log.info("Exported DataFrame to Markdown format")


@asset(deps=[get_meds])
def eng_meds(context: AssetExecutionContext) -> pd.DataFrame:
    meds_df = pd.read_csv("/opt/dagster/data/meds.csv", header=2, skiprows=0)
    context.log.info(f"Read {len(meds_df)} rows from meds.csv")

    # Convert DataFrame to Markdown
    markdown_str = meds_df.head(5).to_markdown()  # Convert first 5 rows to Markdown

    # Log metadata and materialize the asset
    metadata_dict = {
        "column_names": list(meds_df.columns),
        "row_count": len(meds_df),
        "preview": MetadataValue.md(markdown_str),
    }
    context.add_output_metadata(metadata=metadata_dict)
    context.log.info("Exported DataFrame to Markdown format")

    return meds_df
