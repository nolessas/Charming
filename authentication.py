import streamlit as st
import streamlit.components.v1 as components
from hashlib import sha256
import uuid

# Function to generate a random session token
def generate_session_token():
    return str(uuid.uuid4())

# Function to check if the user is logged in based on session token
def is_user_logged_in():
    session_token = st.session_state.get("session_token")
    return session_token is not None

# Function to check the entered password against the desired credentials
def check_password(username, password, desired_username, desired_password):
    hashed_input_password = sha256(password.encode()).hexdigest()
    return username == desired_username and hashed_input_password == sha256(desired_password.encode()).hexdigest()

def show_login():
    st.subheader("Login")

    # Add login form elements here
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Login"):
        # Change these values to your actual secrets keys
        desired_username = st.secrets["global"]["username"]
        desired_password = st.secrets["global"]["password"]

        if check_password(username, password, desired_username, desired_password):
            st.success("Login successful!")
            # Generate a session token and store it in session state
            session_token = generate_session_token()
            st.session_state.session_token = session_token
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")


# Check for the session token on app startup
if "session_token" not in st.session_state:
    show_login()
else:
    if is_user_logged_in():
        # User is logged in, proceed to main app functionality
        pass  # Replace with the code to display your main app
    else:
        # Session token is missing or invalid, show the login form again
        show_login()


def set_user_logged_in(logged_in):
    # Set the logged-in state
    st.session_state.logged_in = logged_in

# Check for the session token on app startup
if "session_token" in st.session_state:
    # You may want to perform additional validation here to ensure the session token is valid
    set_user_logged_in(True)

