import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
import datetime

# ----------- Authentication Setup -----------
# Define user details
names = ["Tina", "Rex", "Harshit", "Julian", "Ibraheem"]
usernames = ["tina", "rex", "harshit", "julian", "ibraheem"]
# Plain-text passwords for demonstration only (not secure for production)
passwords = ["password1", "password2", "password3", "password4", "password5"]

# Hash the passwords
hashed_passwords = stauth.Hasher(passwords).generate()

# Build the credentials dictionary
credentials = {"usernames": {}}
for name, username, pwd in zip(names, usernames, hashed_passwords):
    credentials["usernames"][username] = {"name": name, "password": pwd}

# Create the authenticator instance using the credentials dictionary
authenticator = stauth.Authenticate(credentials, "some_cookie_name", "some_signature_key", cookie_expiry_days=30)

# Render the login widget on the main page using the new 'fields' parameter only
name, authentication_status, username = authenticator.login(fields=["username", "password"])

if not authentication_status:
    if authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your username and password")
    st.stop()  # Stop the app if not authenticated
else:
    st.success(f"Welcome {name}!")
    # Optionally, add a logout button in the sidebar
    authenticator.logout("Logout", "sidebar")
# ----------- End of Authentication Setup -----------

# ----------------- Your App Code -----------------
st.title('Hello, Lonely Octopus!')

st.header('This is a header')
st.subheader('This is a subheader')
st.text('This is some black text.')

# Simple chart example
df = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
st.line_chart(df)

# Generate a date range for a month
dates = pd.date_range(start="2024-01-01", end="2024-01-31")

# Weather data example
weather_data = {
    "Avg Temperature (°C)": np.round(np.random.normal(loc=18, scale=5, size=len(dates)), 1),
    "Humidity (%)": np.random.randint(40, 80, size=len(dates)),
    "Wind Speed (km/h)": np.round(np.random.uniform(5, 20, size=len(dates)), 1)
}
df_weather = pd.DataFrame(weather_data, index=dates)

# Generating monthly sales data for different services
services = ["Cruises", "Skydiving", "Water skiing"]
sales_data = {service: np.random.randint(200, 500, size=12) for service in services}
months = pd.date_range(start="2024-01-01", end="2024-12-01", freq='MS')
df_sales = pd.DataFrame(sales_data, index=months.strftime('%B'))

# Unique key for selectbox to avoid duplicate widget errors
chart_type = st.selectbox('Choose a chart type:', ['Line', 'Bar'], key="chart_type_unique")

if chart_type == 'Line':
    st.write("Weather Data Overview")
    st.line_chart(df_weather)
elif chart_type == 'Bar':
    st.write("Monthly Sales Data")
    st.bar_chart(df_sales)

# Dictionary of names with their respective country and favorite color
people_info = {
    "Tina": {"country": "Canada", "fav_color": "yellow"},
    "Rex": {"country": "the Philippines", "fav_color": "purple"},
    "Harshit": {"country": "India", "fav_color": "orange"},
    "Julian": {"country": "Australia", "fav_color": "black"},
    "Ibraheem": {"country": "Morocco", "fav_color": "light blue"},
}

selected_name = st.sidebar.selectbox('Which Lonely Octopus are you interested in?', list(people_info.keys()), key="sidebar_select")

selected_info = people_info[selected_name]

st.markdown(
    f"<b>{selected_name}</b> is from <b>{selected_info['country']}</b>. Favorite color: <b>{selected_info['fav_color']}</b>.",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
with col1:
    st.line_chart(df['a'])
with col2:
    st.line_chart(df['b'])

with st.expander("See explanation"):
    st.text("Here you can put in detailed explanations.")

if st.button('What is Streamlit?'):
    st.write('A faster way to build and share data apps. Streamlit turns data scripts into shareable web apps in minutes.')
else:
    st.write('Click me to define streamlit.')
