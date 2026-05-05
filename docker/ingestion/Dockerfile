FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY data/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ingestion/ ./ingestion/

#Command to run the application
CMD ["python", "ingestion/generator.py"]
