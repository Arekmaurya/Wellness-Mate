# Use official Python slim image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set up a new user named "user" with user ID 1000 (required for HF Spaces)
RUN useradd -m -u 1000 user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    OLLAMA_MODELS=/home/user/.ollama/models

# Set working directory to the user's home directory
WORKDIR $HOME/app

# Copy requirements and install Python dependencies
COPY --chown=user requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy project files with proper ownership
COPY --chown=user main.py .
COPY --chown=user background.png .
COPY --chown=user Modelfile .
COPY --chown=user start.sh .
RUN chmod +x start.sh

# Expose Streamlit port (HF Spaces defaults to 7860)
EXPOSE 7860

# Note: Volumes work differently in HF Spaces, we rely on HF persistent storage or download at runtime
# Start Ollama, create model if needed, then launch the app
CMD ["bash", "start.sh"]