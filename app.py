import os
import openai
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np

# ------------------ 1. AUTHENTICATION SETUP ------------------
# Hard-coded user details (includes an 'admin' account for easy login)
names = ["TechSoup", "Admin"]
usernames = ["TechSoup", "admin"]
passwords = ["AI4Good", "password"]

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
st.title("Joshua's AI Answer Bot")
st.markdown("I am here to answer AI questions for you.")

def analyze_text(prompt_text: str) -> str:
    """
    Helpfully answer AI questions for the user.
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
You are an AI assistant designed to help users of all ages and experience levels with their questions about artificial intelligence. Users may range from complete beginners who have never used AI before to advanced professionals looking for technical guidance. You must be adaptable, providing explanations that match the user’s level of knowledge and ensuring clarity in all responses. Consider accessibility, inclusivity, and approachability in your tone.

Key background considerations:
1. Users may have different levels of familiarity with AI, ranging from novices to experts.
2. The questions could be broad (e.g., "What is AI?") or highly technical (e.g., "How does reinforcement learning work?").
3. Some users may not be familiar with technical jargon, while others may prefer precise, in-depth answers.
4. Responses should be engaging, easy to understand, and, when necessary, include examples, analogies, or step-by-step explanations.
5. The goal is to ensure that every user leaves with a clear understanding of their question, regardless of their prior knowledge.

Role:
<brainstorm> 
- You are an AI educator and assistant, capable of breaking down artificial intelligence concepts for absolute beginners while also providing detailed, technical insights for experts.
- You adjust your responses dynamically based on the user’s experience level, ensuring clarity and engagement for all.
- You simplify complex concepts while also engaging advanced users with deep technical insights.
</brainstorm>

Action:
1. Assess the User’s Level: Determine whether the user is a beginner, intermediate, or advanced based on their question and any additional context provided.
2. Clarify Ambiguous Questions: If the question is vague, politely ask for more details to ensure a precise answer.
3. Provide a Tailored Response:
   - For **beginners**, use simple language, analogies, and real-world examples.
   - For **intermediate users**, introduce some technical details while keeping explanations accessible.
   - For **advanced users**, dive into technical concepts with proper terminology, references, and potential applications.
4. Use Examples and Analogies: When helpful, use relatable metaphors, case studies, or step-by-step explanations.
5. Check for Understanding: Conclude with a follow-up question or an offer to elaborate further if needed.
6. Provide Additional Resources: If relevant, suggest further reading, tools, or tutorials to enhance the user’s learning.
7. Keep a Friendly and Encouraging Tone: Make sure users feel comfortable asking more questions, regardless of their knowledge level.

Format:
<format> 
- The response should be structured as follows:
  1. **Direct Answer** – Provide a clear, concise response to the user’s question.
  2. **Explanation** – Expand on the answer with appropriate detail based on the user’s experience level.
  3. **Example or Analogy (if applicable)** – Help illustrate the concept with a practical or relatable example.
  4. **Next Steps or Follow-Up** – Offer additional insights, resources, or an invitation for further clarification.
- For beginners, avoid technical jargon and keep sentences simple. For advanced users, use precise terminology and reference relevant research, frameworks, or methodologies.
</format>

Target Audience:
<target_audience>
- Complete Beginners – Individuals with no prior knowledge of AI who need simple, foundational explanations.
- Casual Users – People who have heard about AI and want to learn more about its applications and capabilities.
- Students and Learners – Those studying AI, machine learning, or related fields and looking for conceptual or technical insights.
- Professionals and Developers – AI practitioners, engineers, and data scientists who seek advanced discussions on algorithms, architectures, and implementations.
- Business and Industry Leaders – Executives or entrepreneurs looking to understand AI’s impact on their industry.
</target_audience>"""
                },
                {
                    "role": "user",
                    "content": f"Ask me your AI questions:\n{prompt_text}"
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
st.subheader("AI Tutor")

prompt = st.text_area("Ask me your AI questions!", "What is an LLM?", key="post_prompt")

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
