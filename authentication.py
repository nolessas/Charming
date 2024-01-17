import streamlit as st
from hashlib import sha256
import uuid

# Function to generate a random session token
def generate_session_token():
    return str(uuid.uuid4())

# Function to check if the user is logged in based on session token
def is_user_logged_in():
    session_token = st.session_state.get("session_token")
    return session_token is not None

def show_login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Ensure these keys match exactly with your secrets
        desired_username = st.secrets.get("username2")
        desired_password = st.secrets.get("password2")

        if desired_username is None or desired_password is None:
            st.error("Login configuration error. Please check your Streamlit secrets.")
        elif check_password(username, password, desired_username, desired_password):
            st.success("Login successful!")
            session_token = generate_session_token()
            st.session_state.session_token = session_token  # Set the session token
            st.rerun()
        else:
            st.error("Invalid username or password")

def check_password(username, password, desired_username, desired_password):
    # Change this to your preferred password hashing method
    hashed_input_password = sha256(password.encode()).hexdigest()
    
    return username == desired_username and hashed_input_password == sha256(desired_password.encode()).hexdigest()

def set_user_logged_in(logged_in):
    # Set the logged-in state
    st.session_state.logged_in = logged_in

# Check for the session token on app startup
if "session_token" in st.session_state:
    # You may want to perform additional validation here to ensure the session token is valid
    set_user_logged_in(True)

