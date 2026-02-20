import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Groq API key not found in .env file")
    st.stop()

client = Groq(api_key=api_key)

st.title("🐍 Python Error Fixing Tool (FREE Llama via Groq)")

error_message = st.text_area("Enter Python Error")
code_input = st.text_area("Paste Your Code")

if st.button("Fix Error"):

    prompt = f"""
You are a Python debugging expert.

Error:
{error_message}

Code:
{code_input}

Explain the error simply and provide corrected code.
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=500
    )

    st.write(chat_completion.choices[0].message.content)