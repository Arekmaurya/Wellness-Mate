import streamlit as st
import ollama
import base64
import os
import html as html_module

# Page setup
st.set_page_config(page_title="Wellness Mate Chatbot")


# Load local background image or fallback to online image
def get_base64(background):
    try:
        with open(background, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        print("⚠️ Background image failed to load:", e)
        return None


# ✅ Fix: use abspath to handle empty __file__ dirname in Docker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "background.png")

bin_str = get_base64(image_path)

if bin_str:
    background_style = f'background-image: url("data:image/png;base64,{bin_str}");'
else:
    background_style = 'background-image: url("https://images.unsplash.com/photo-1616627988466-43b93fc2aa2e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80");'

# CSS styling
st.markdown(
    f"""
    <style>
        [data-testid="stAppViewContainer"] > .main {{
            {background_style}
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        [data-testid="stHeader"], [data-testid="stToolbar"] {{
            background: rgba(0,0,0,0);
            visibility: hidden;
        }}

        .block-container {{
            padding-top: 2rem;
            background: rgba(255, 182, 193, 0.7);
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            color: #4e4e4e;
        }}

        h1 {{
            text-align: center;
            color: #d16d8c;
            font-size: 2.5rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }}

        .stButton button {{
            background-color: #4CAF50;
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            font-weight: bold;
            border: none;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .stButton button:hover {{
            background-color: #45A049;
            color: #f0f0f0;
        }}

        .stTextInput > div > input {{
            background-color: #ffe6e6;
            color: #4e4e4e;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #f1a7b0;
        }}
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize conversation
st.session_state.setdefault("conversation_history", [])


# Chat response
def generate_response(user_input):
    st.session_state["conversation_history"].append(
        {"role": "user", "content": user_input}
    )

    system_prompt = {
        "role": "system",
        "content": (
            "You are Wellness Mate, a compassionate AI wellness assistant. "
            "Your job is to support users with stress, anxiety, motivation, "
            "mental health encouragement, and self-care advice. "
            "Respond in a warm, supportive, and calming tone."
        ),
    }

    recent_history = st.session_state["conversation_history"][-6:]
    messages = [system_prompt] + recent_history

    try:
        response = ollama.chat(
            model="psychiatrist",
            messages=messages,
            options={"num_predict": 256},
        )
        ai_response = response.get("message", {}).get("content", "I'm here for you.")
    except Exception as e:
        ai_response = "⚠️ Sorry, something went wrong. Please try again."
        print("Chat error:", e)

    st.session_state["conversation_history"].append(
        {"role": "assistant", "content": ai_response}
    )

    return ai_response


# Affirmation
def generate_affirmation():
    messages = [
        {
            "role": "system",
            "content": "You are a motivational wellness coach. Provide short, powerful positive affirmations.",
        },
        {
            "role": "user",
            "content": "Give me a positive affirmation for stress relief.",
        },
    ]

    try:
        response = ollama.chat(model="psychiatrist", messages=messages, options={"num_predict": 256})
        return response["message"]["content"]
    except Exception as e:
        print("Affirmation error:", e)
        return "⚠️ Could not generate an affirmation."


# Meditation
def generate_meditation_guide():
    messages = [
        {
            "role": "system",
            "content": (
                "You are a calm meditation guide. "
                "Provide a gentle, slow, relaxing 5-minute guided meditation script. "
                "Use soothing language."
            ),
        },
        {
            "role": "user",
            "content": "Give me a 5-minute guided meditation for stress relief.",
        },
    ]

    try:
        response = ollama.chat(model="psychiatrist", messages=messages, options={"num_predict": 256})
        return response["message"]["content"]
    except Exception as e:
        print("Meditation guide error:", e)
        return "⚠️ Could not generate a meditation guide."


# Title
st.title("🌿 WELLNESS MATE")

# Chat display
for msg in st.session_state["conversation_history"]:
    if msg["role"] == "user":
        safe_content = html_module.escape(msg['content'])
        st.markdown(
            f"""
        <div style="background-color:#89c9b8; padding:10px; margin:10px 0; border-radius:10px; max-width:80%; text-align:right;">
            <b>You:</b> {safe_content}
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        safe_content = html_module.escape(msg['content'])
        st.markdown(
            f"""
        <div style="background-color:#ccc; padding:10px; margin:10px 0; border-radius:10px; max-width:80%;">
            <b>AI:</b> {safe_content}
        </div>
        """,
            unsafe_allow_html=True,
        )

# Input field
user_message = st.text_input("💬 How can I help you today?")

if user_message:
    with st.spinner("🤔 Thinking..."):
        generate_response(user_message)
    st.rerun()

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🌞 Give me a Positive Affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**💬 Affirmation:** {affirmation}")

with col2:
    if st.button("🧘 Start a Guided Meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**🧘 Guided Meditation:** {meditation_guide}")

# Footer
st.markdown(
    """
<hr style="margin-top:50px">
<div style='text-align: center; color: black; font-size: 12px;'>
    Wellness Mate © 2025 | Built with 💙 using Streamlit & Ollama
    <footer>
        <div class="container">
            WELLNESS MATE. All rights reserved.
            <p>
                Developed by 
                <a href="https://www.linkedin.com/in/harsh-mauryaa/" style="color: red;">Harsh Maurya</a> |
                <a href="#" style="color: red;">Contact Us</a>
            </p>
        </div>
    </footer>
</div>
""",
    unsafe_allow_html=True,
)
