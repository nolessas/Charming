# authentication.py

import streamlit as st
from hashlib import sha256
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Example usage
hashed_password = hash_password("your_password")
print(hashed_password)



def is_user_logged_in():
    return st.session_state.get('logged_in', False)


def show_login():
    st.subheader("Login")

    # Add login form elements here
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Change these values to your desired credentials
        # These lines are no longer needed as you're now using Streamlit secrets
        # desired_username = "a"
        # desired_password = "a"

        if check_password(username, password):
            st.success("Login successful!")
            set_user_logged_in(True)
            # The balloons should be released after the successful message.
            st.balloons()
            st.experimental_rerun()

        else:
            st.error("Invalid username or password")


def check_password(username, password):
    # Retrieve user's plaintext password from Streamlit secrets
    user_password_plain = st.secrets["users"].get(username)

    return password == user_password_plain

    
def is_user_persistently_logged_in():
    return st.server.server.Server.get_current()._session_data.get('logged_in', False)


def set_user_logged_in(logged_in):
    st.session_state['logged_in'] = logged_in

