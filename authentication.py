# authentication.py

import streamlit as st
from hashlib import sha256

def is_user_logged_in():
    return st.session_state.get('logged_in', False)


def show_login():
    st.subheader("Login")

    # Add login form elements here
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Change these values to your desired credentials
        desired_username = "a"
        desired_password = "a"  # Replace with your actual desired password

        if check_password(username, password, desired_username, desired_password):
            st.success("Login successful!")
            set_user_logged_in(True)
            # The balloons should be released after the successful message.
            st.balloons()
            st.experimental_rerun()

        else:
            st.error("Invalid username or password")

def check_password(username, password):
    # Retrieve user's hashed password from Streamlit secrets
    user_password_hash = st.secrets["users"].get(username)

    if user_password_hash:
        # Check if the provided password matches the stored hash
        hashed_input_password = sha256(password.encode()).hexdigest()
        return hashed_input_password == user_password_hash
    else:
        # Username not found in secrets
        return False
    
def is_user_persistently_logged_in():
    return st.server.server.Server.get_current()._session_data.get('logged_in', False)


def set_user_logged_in(logged_in):
    st.session_state['logged_in'] = logged_in

