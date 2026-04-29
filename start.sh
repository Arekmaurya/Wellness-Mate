#!/bin/bash
set -e

echo "🚀 Starting Ollama server..."
ollama serve &
sleep 5

# Check if the psychiatrist model already exists
if ollama list | grep -q "psychiatrist"; then
    echo "✅ Model 'psychiatrist' already exists, skipping creation."
else
    if [ -n "$SPACE_ID" ]; then
        echo "☁️ Hugging Face Space detected. Pulling lightweight llama3.2:1b model..."
        ollama pull llama3.2:1b
        
        echo "📦 Creating 'psychiatrist' model from lightweight base..."
        echo "FROM llama3.2:1b" > ./Modelfile.tiny
        echo "PARAMETER temperature 0.7" >> ./Modelfile.tiny
        echo "PARAMETER num_predict 256" >> ./Modelfile.tiny
        echo 'SYSTEM """You are Wellness Mate, a compassionate AI wellness assistant and psychiatrist. Your job is to support users with stress, anxiety, motivation, mental health encouragement, and self-care advice. Respond in a warm, supportive, and calming tone."""' >> ./Modelfile.tiny
        
        ollama create psychiatrist -f ./Modelfile.tiny
    else
        echo "📦 Creating 'psychiatrist' model from standard 8B Modelfile..."
        ollama create psychiatrist -f ./Modelfile
    fi
    echo "✅ Model 'psychiatrist' created successfully."
fi

echo "🌿 Starting Wellness Mate..."
streamlit run main.py --server.port=7860 --server.address=0.0.0.0
