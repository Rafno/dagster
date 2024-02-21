FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

# Copy requirements.txt and install dependencies
COPY pyproject.toml setup.py setup.cfg /opt/dagster/dagster_home/

WORKDIR /opt/dagster/dagster_home

RUN pip install .

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

EXPOSE 3000

# Specify the entrypoint command to start the Dagster web server
#ENTRYPOINT ["dagster-webserver", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]
ENTRYPOINT ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000"]