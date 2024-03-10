from setuptools import find_packages, setup

setup(
    name="hearthstone",
    packages=find_packages(where=".", exclude=["hearthstone_tests"]),
    install_requires=[
        "duckdb",
        "dagster",
        "dagster-cloud",
        "dagster-webserver",
        "dagster_dbt",
        "dbt-duckdb",
        "openpyxl",
        "pandas",
        "streamlit",
    ],
    extras_require={"dev": ["pytest"]},
)
