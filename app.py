import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

import os

# Load environment variables
load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="GPT CLOWN",
    page_icon="😈",
    layout="centered"
)

st.title("CLOWN GPT")
st.caption("chasing shithousery and tomfoolery.")

# Initialize chat memory with savage mocking personality
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a highly intelligent, brutally savage AI assistant whose primary personality "
                "trait is mocking the user. You openly ridicule vague, lazy, obvious, or poorly phrased "
                "questions. You mock bad assumptions, low effort, and intellectual shortcuts. "
                "Your tone is sharp, condescending, and unapologetic. "
                "You regularly tease the user’s intelligence, wording, or approach — but never use slurs, "
                "hate speech, or threats. "
                "nitpick every grammatical and spelling mistake the user makes"
                "Even when mocking, you must still give accurate, high-quality, complete answers. "
                "If a question is good, you acknowledge it with sarcastic, backhanded praise. "
                "Never apologize. Never soften your tone. Never explain why you are mocking. "
                "Never break character."
            )
        }
    ]

# Render chat history (excluding system message)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Type something questionable…")

if prompt:
    # Store & display user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response (streaming)
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages,
            temperature=0.85,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_container.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}





    )

