import openai
import os
import streamlit as st

# Fetch the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
else:
    st.write("API key is set and its length is:", len(api_key))
    openai.api_key = api_key

def analyze_text(text):
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You are an assistant who helps craft social media posts."},
        {"role": "user", "content": f"Please help me write a social media post based on the following:\n{text}"}
    ]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {e}")
        return "An error occurred."

user_input = st.text_area("Enter a brief for your post:", "How should you maintain a deployed model?", key="post_input_unique")
if st.button('Generate Post Content'):
    post_text = analyze_text(user_input)
    st.write(post_text)

