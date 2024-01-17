import streamlit as st
from hashlib import sha256
import uuid

# Function to generate a random session token
def generate_session_token():
    return str(uuid.uuid4())

# Function to check if the user is logged in based on session token
def is_user_logged_in():
    """ Check if the user is logged in based on session token. """
    return "session_token" in st.session_state

def show_login():
    st.subheader("Login")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Login"):
        stored_password = st.secrets["password"]  # Make sure the key matches exactly

        if password == stored_password:
            st.success("Login successful!")
            # Create a session token or another method to keep the user logged in
            st.session_state['logged_in'] = True  # Just a simple flag here
            # Now redirect or show the main content
        else:
            st.error("Invalid password")


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

