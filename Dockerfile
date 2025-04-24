FROM python:3.10

# Update package lists and pip
RUN apt-get update && \
    pip install -U pip

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 8000

# Set entrypoint to run Streamlit app
ENTRYPOINT ["streamlit", "run", "streamlit_demo/streamlit_mockup.py", "--server.port=8000"]