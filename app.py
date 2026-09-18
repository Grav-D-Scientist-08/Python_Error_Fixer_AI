import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get Groq API Key
api_key = os.getenv("GROQ_API_KEY")

# Check API Key
if not api_key:
    st.error("❌ Groq API key not found in .env file")
    st.stop()

# Create Groq client
client = Groq(api_key=api_key)

# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(
    page_title="Python Error Fixer AI",
    page_icon="🐍",
    layout="centered"
)

st.title("🐍 Python Error Fixer AI")
st.write("Enter your Python error and code. AI will explain and fix the error.")

# Error input
error_message = st.text_area(
    "🔴 Enter Python Error",
    height=150,
    placeholder="Example: NameError: name 'x' is not defined"
)

# Code input
code_input = st.text_area(
    "💻 Paste Your Python Code",
    height=250,
    placeholder="Paste your Python code here..."
)

# Fix Error Button
if st.button("🔧 Fix Error", use_container_width=True):

    if not error_message.strip():
        st.warning("⚠️ Please enter a Python error.")

    elif not code_input.strip():
        st.warning("⚠️ Please paste your Python code.")

    else:

        # Prompt for AI
        prompt = f"""
You are an expert Python debugging assistant.

Analyze the following Python error and code.

Python Error:
{error_message}

Python Code:
{code_input}

Your task:

1. Explain the error in simple language.
2. Identify the exact cause of the error.
3. Provide the corrected Python code.
4. Explain what was changed.
5. Give one simple tip to avoid this error in the future.

Keep the explanation beginner-friendly.
"""

        try:

            # Groq API call
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="openai/gpt-oss-20b",
                temperature=0.3,
                max_tokens=800
            )

            # Get AI response
            response = chat_completion.choices[0].message.content

            # Display result
            st.success("✅ Error Analysis Complete!")

            st.markdown("### 🤖 AI Solution")

            st.markdown(response)

        except Exception as e:

            st.error("❌ Something went wrong while connecting to Groq.")

            st.code(str(e))