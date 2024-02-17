FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

# Copy requirements.txt and install dependencies
COPY requirements.txt /opt/dagster/app/
WORKDIR /opt/dagster/app
RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml setup.py /opt/dagster/app/

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

EXPOSE 3000

# Specify the entrypoint command to start the Dagster web server
#ENTRYPOINT ["dagster-webserver", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]
ENTRYPOINT ["dagster", "dev", "-m", "pipelines", "-h", "0.0.0.0", "-p", "3000"]