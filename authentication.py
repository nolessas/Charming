import streamlit as st
from hashlib import sha256
from datetime import datetime

# Define the session timeout as None (unlimited session duration)
SESSION_TIMEOUT = None

def is_user_logged_in():
    return st.session_state.get("logged_in", False)

def show_login():
    st.subheader("Login")

    # Add login form elements here
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Change these values to your desired credentials
        desired_username = st.secrets["username2"]
        desired_password = st.secrets["password2"]

        if check_password(username, password, desired_username, desired_password):
            st.success("Login successful!")
            set_user_logged_in(True)
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def check_password(username, password, desired_username, desired_password):
    # Change this to your preferred password hashing method
    hashed_input_password = sha256(password.encode()).hexdigest()
    
    return username == desired_username and hashed_input_password == sha256(desired_password.encode()).hexdigest()

def set_user_logged_in(logged_in):
    # Set the logged-in state
    st.session_state.logged_in = logged_in
