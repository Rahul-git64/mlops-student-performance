# Use an official, lightweight Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for clean scikit-learn/numpy/pandas builds
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code and configuration files
COPY app.py .
COPY params.yaml .
# Note: Models folder and dataset will be generated/pulled during training/pipeline execution
# Copy existing models directory if present for self-contained image distribution
COPY models/ ./models/

# Expose port 8501 for Streamlit access
EXPOSE 8501

# Define environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Set the command to run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py"]
