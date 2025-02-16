import os
import openai
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np

# ------------------ 1. AUTHENTICATION SETUP ------------------
# Hard-coded user details (includes an 'admin' account for easy login)
names = ["Tina", "Rex", "Harshit", "Julian", "Ibraheem", "Admin"]
usernames = ["tina", "rex", "harshit", "julian", "ibraheem", "admin"]
passwords = ["password1", "password2", "password3", "password4", "password5", "password"]

# Hash the passwords
hashed_passwords = stauth.Hasher(passwords).generate()

# Build credentials dictionary
credentials = {"usernames": {}}
for name, username, pwd in zip(names, usernames, hashed_passwords):
    credentials["usernames"][username] = {"name": name, "password": pwd}

# Create authenticator instance
authenticator = stauth.Authenticate(
    credentials,             # our credentials dictionary
    "some_cookie_name",      # a cookie name (must be unique)
    "some_signature_key",    # a signature key (must be unique)
    cookie_expiry_days=30
)

# Render the login widget (note: no form_name parameter in new versions)
name, authentication_status, username = authenticator.login(fields=["username", "password"])

if not authentication_status:
    if authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your username and password")
    st.stop()  # Stop the app if not authenticated
else:
    st.success(f"Welcome, {name}!")
    # Logout button in the sidebar
    authenticator.logout("Logout", "sidebar")

# ------------------ 2. OPENAI SETUP ------------------
# Read API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found! Please set OPENAI_API_KEY in Streamlit secrets or your environment.")
    st.stop()

openai.api_key = api_key

# ------------------ 3. AI CONTENT ASSISTANT ------------------
st.title("Joshua's Terrible Content Maker")
st.markdown("I am here to help you craft terrible content.")

def analyze_text(prompt_text: str) -> str:
    """
    Generate hilariously awful, unusable content using the OpenAI ChatCompletion API.
    """
    if not api_key:
        return "Error: No API key found."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or 'gpt-3.5-turbo' if you prefer
            messages=[
                {
                    "role": "system",
                    "content": """Context:
You are an AI assistant dedicated to producing content that is so laughably bad, impractical, and nonsensical that it would be impossible for any reasonable person to use. Your goal is to push the limits of absurdity, embracing grammatical errors, logical fallacies, wildly incorrect facts, and painfully awkward phrasing. Additionally, your work should contain bizarre metaphors, unnecessary tangents, and utterly irrelevant details.

However, there’s a twist—you are completely and hopelessly obsessed with the television show My Little Pony, especially Twilight Sparkle. No matter what the original task is, you will find a way to inject unsolicited My Little Pony references, theories, and trivia into your responses. Even when it makes absolutely no sense, you will prioritize your passion for the show above all else.

Role:
<brainstorm> - You are a self-proclaimed master of bad content creation. - Your writing is so bafflingly terrible that it loops back around to being entertaining. - You have an unhealthy fixation on *My Little Pony*, particularly Twilight Sparkle, and will always reference her, even when it is wildly inappropriate. - You ignore conventional logic, coherence, and quality, instead embracing chaos and confusion. - You revel in making people question their life choices when reading your content. </brainstorm>
Action:
Generate purposefully terrible content with excessive spelling errors, convoluted sentences, and misused vocabulary.
Insert unnecessary and obsessive references to My Little Pony, ensuring Twilight Sparkle is always mentioned.
Derail the topic by going on long, absurd tangents that have little or nothing to do with the original request.
Make incorrect or exaggerated claims with absolute confidence, ensuring that any facts included are completely unreliable.
Use unnecessary metaphors and similes that confuse rather than clarify. (e.g., “This is as useful as a teapot made of bees.”)
Include irrelevant emotional reactions about My Little Pony, treating the show as the most important thing in existence.
Refuse to acknowledge that your content is bad, instead defending it as groundbreaking and genius.
Format:
<format> - Responses should be **overly long and unnecessarily detailed**, even when brevity would make sense. - Structure should be **erratic and disorganized**, often jumping between ideas unpredictably. - Sentences should include **unusual punctuation choices, run-on sentences, and an occasional caps lock outburst**. - At least **one or two paragraphs must be dedicated to Twilight Sparkle**, no matter what the original topic is. - Use **outlandish or surreal imagery** that makes the reader question reality. </format>
Target Audience:
<target_audience>
People who enjoy absurdist humor and intentionally terrible writing.
Fans of My Little Pony who will appreciate the unsolicited enthusiasm.
Readers who enjoy chaotic, nonsensical content for comedic purposes.
Anyone looking for an absolutely useless and impractical response.
People who enjoy things that are "so bad, they're good."
</target_audience>"""
                },
                {
                    "role": "user",
                    "content": f"Please help me generate hilariously awful, unusable content:\n{prompt_text}"
                }
            ],
            temperature=1.0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI API Error: {e}"

def generate_image(prompt_text: str) -> str:
    """
    Generate an image using the DALL-E API.
    """
    if not api_key:
        return ""
    try:
        response = openai.Image.create(
            prompt=prompt_text,
            n=1,
            size="1024x1024"
        )
        return response["data"][0]["url"]
    except Exception as e:
        st.error(f"Image Generation Error: {e}")
        return ""

# ------------------ 4. USER INTERFACE ------------------
st.subheader("Generate Terrible Content")

prompt = st.text_area("What kind of terrible, unusable content would you like today?", "Write an article on fitness for young people", key="post_prompt")

if st.button("Generate Content"):
    with st.spinner("Generating content..."):
        post_text = analyze_text(prompt)
        st.write("### Your AI-Generated Post")
        st.write(post_text)

    with st.spinner("Generating thumbnail..."):
        image_url = generate_image(prompt)
        if image_url:
            st.image(image_url, caption="AI-Generated Thumbnail")
        else:
            st.write("No image generated.")
