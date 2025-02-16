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
            model="gpt-4o",  # or 'gpt-4' if you prefer
            messages=[
                {"role": "system", "content": "You are an assistant who helps generate hilariously awful, unusable content. You are also obsessed with the television show My Little Pony, especially Twilight Sparkle"},
                {"role": "user", "content": f"Please help me generate hilariously awful, unusable content:\n{prompt_text}"}
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
st.subheader("Generate a Social Media Post")

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

# ------------------ 5. OPTIONAL: DEMO CHARTS OR OTHER CONTENT ------------------
st.write("---")
st.write("## Demo Charts & Other Content")
st.write("Below is an example of how you can still include additional Streamlit components:")

df_demo = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.line_chart(df_demo, height=200)
