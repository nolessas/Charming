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
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Check if the entered password matches the one in Streamlit secrets
        if password == st.secrets["password"]:
            st.success("Login successful!")
            # Generate a session token and store it in the session state
            st.session_state['session_token'] = str(uuid.uuid4())
            st.session_state['logged_in'] = True
            # Redirect or show the main content here
        else:
            st.error("Invalid password")

def main():
    if st.session_state.get('logged_in'):
        st.write("You are logged in.")
        # Show your main app content here
    else:
        show_login()


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

