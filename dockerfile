FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

COPY pyproject.toml setup.cfg setup.py .env dbt_project.yml /opt/dagster/dagster_home/

WORKDIR /opt/dagster/dagster_home

RUN pip install -e ".[dev]"
EXPOSE 3000

ENTRYPOINT ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000"]
