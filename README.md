---
title: Wellness Mate
emoji: 🌿
colorFrom: green
colorTo: pink
sdk: docker
app_port: 7860
---

# 🌿 Wellness Mate

A compassionate AI wellness chatbot powered by a fine-tuned **psychiatrist LLM** (LLaMA 3.1 8B). Built with **Streamlit** and **Ollama**.

![Wellness Mate](background.png)

## ✨ Features

- 💬 **AI Chat** — Talk to a fine-tuned psychiatrist model for mental health support
- 🌞 **Positive Affirmations** — Get uplifting affirmations on demand
- 🧘 **Guided Meditation** — Receive calming meditation scripts

## 🚀 Quick Start

### Run with Docker (Recommended)
```bash
docker pull harshmaurya2002/wellness-mate:latest
docker run -p 8501:8501 harshmaurya2002/wellness-mate
```
Then open [http://localhost:8501](http://localhost:8501)

### Run Locally
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Make sure Ollama is running with the psychiatrist model
ollama create psychiatrist -f Modelfile

# 3. Run the app
streamlit run main.py
```

## 🧠 Model

Uses a fine-tuned [psychiatrist-llama-3.1-8b-gguf](https://huggingface.co/Arekmaurya/psychiatrist-llama-3.1-8b-gguf) model hosted on Hugging Face, served locally via Ollama.

## 🐳 Docker Hub

[harshmaurya2002/wellness-mate](https://hub.docker.com/r/harshmaurya2002/wellness-mate)

## 🤗 Hugging Face Spaces

[Arekmaurya/wellness-mate](https://huggingface.co/spaces/Arekmaurya/wellness-mate)

## 📁 Project Structure

```
├── main.py           # Streamlit app
├── Modelfile         # Ollama model configuration
├── Dockerfile        # Docker build file
├── start.sh          # Container startup script
├── requirements.txt  # Python dependencies
├── background.png    # UI background image
├── .gitignore        # Git ignore rules
└── .dockerignore     # Docker ignore rules
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM Backend**: Ollama + Fine-tuned LLaMA 3.1 8B
- **Containerization**: Docker
- **Model Hosting**: Hugging Face

## 👨‍💻 Author

Developed by [Harsh Maurya](https://www.linkedin.com/in/harsh-mauryaa/)

## 📄 License

MIT License
