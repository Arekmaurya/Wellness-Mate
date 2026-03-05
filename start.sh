#!/bin/bash
set -e

echo "🚀 Starting Ollama server..."
ollama serve &
sleep 5

# Check if the psychiatrist model already exists (cached via volume)
if ollama list | grep -q "psychiatrist"; then
    echo "✅ Model 'psychiatrist' already exists, skipping creation."
else
    echo "📦 Creating 'psychiatrist' model from Modelfile..."
    ollama create psychiatrist -f /app/Modelfile
    echo "✅ Model 'psychiatrist' created successfully."
fi

echo "🌿 Starting Wellness Mate..."
streamlit run main.py --server.port=8501 --server.address=0.0.0.0
