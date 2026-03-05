# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY main.py .
COPY background.png .
COPY Modelfile .
COPY start.sh .
RUN chmod +x start.sh

# Expose Streamlit port
EXPOSE 8501

# Persist Ollama model data across container runs
VOLUME /root/.ollama

# Start Ollama, create model if needed, then launch the app
CMD ["bash", "start.sh"]