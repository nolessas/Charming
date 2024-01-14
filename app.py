import streamlit as st
import pandas as pd
from authentication import is_user_logged_in, show_login, set_user_logged_in




# Streamlit app
def main():
    st.title("Client Management App")

    # Check if the user is logged in
    if not is_user_logged_in():
        show_login()  # Show the login screen if not logged in
    else:
        # User is logged in, show the main menu
        show_main_menu()
    
    # Create st.radio buttons for main menu options
    menu_option = st.radio("Select an option", ("Register Client", "View Registered Clients", "To-Do List"))

    if menu_option == "Register Client":
        st.header("Register New Client")
        date = st.date_input("Date")
        time = st.time_input("Time")
        full_name = st.text_input("Full Name")
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email")
        notes = st.text_area("Notes")
        if st.button("Register Client"):
            register_client(date, time, full_name, phone_number, email, notes)

    elif menu_option == "View Registered Clients":
        st.header("Registered Clients")
        view_registered_clients()

    elif menu_option == "To-Do List":
        st.header("To-Do List")
        manage_todo_list()

def register_client(date, time, full_name, phone_number, email, notes):
    try:
        # Create or load a DataFrame to store client data
        if 'client_data' not in st.session_state:
            st.session_state.client_data = pd.DataFrame(columns=["Date", "Time", "Full Name", "Phone Number", "Email", "Notes"])

        # Convert date and time to datetime object
        appointment_time = pd.to_datetime(f"{date} {time}")

        # Create a new client record
        new_client = pd.Series({
            "Date": appointment_time.strftime("%Y-%m-%d"),
            "Time": appointment_time.strftime("%H:%M:%S"),
            "Full Name": full_name,
            "Phone Number": phone_number,
            "Email": email,
            "Notes": notes
        })

        # Append the new client to the DataFrame
        st.session_state.client_data = st.session_state.client_data.append(new_client, ignore_index=True)

        st.success("Client registered successfully!")
    except Exception as e:
        st.error(f"Error registering client: {str(e)}")

def view_registered_clients():
    if 'client_data' not in st.session_state:
        st.write("No registered clients found.")
    else:
        st.write(st.session_state.client_data)

def manage_todo_list():
    # Placeholder function for the to-do list
    st.write("To-Do List functionality will be added here.")

if __name__ == "__main__":
    main()
