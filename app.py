import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread
from datetime import datetime, timedelta

# Define the necessary scope(s) for the Google Calendar API
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']

service_account_info = st.secrets["google_oauth"]
credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES_SHEETS)
gc = gspread.authorize(credentials)




# Streamlit app
def main():
    st.title("Client Management App")

    menu_option = st.sidebar.selectbox("Select an option", ["Register Client", "View Registered Clients", "To-Do List"])

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
        worksheet = gc_sheets.open_by_key('1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ').worksheet('Sheet1')

        if worksheet.row_count == 0:
            header_row = ["Date", "Time", "Full Name", "Phone Number", "Email", "Notes"]
            worksheet.append_row(header_row)

        appointment_time = datetime.combine(date, time)
        data = [appointment_time.strftime("%Y-%m-%d"), appointment_time.strftime("%H:%M:%S"), full_name, phone_number, email, notes]
        worksheet.append_row(data)

        create_calendar_event(full_name, appointment_time)

        st.success("Client registered successfully!")
    except Exception as e:
        st.error(f"Error registering client: {str(e)}")

def view_registered_clients():
    try:
        worksheet = gc_sheets.open_by_key('1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ').worksheet('Sheet1')
        data = worksheet.get_all_records()

        if not data:
            st.write("No registered clients found.")
        else:
            df = pd.DataFrame(data)
            st.write(df)
    except Exception as e:
        st.error(f"Error fetching registered clients: {str(e)}")

def manage_todo_list():
    try:
        worksheet = gc_sheets.open_by_key('1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ').worksheet('Sheet2')
        data = worksheet.get_all_records()

        if not data:
            st.write("No to-do items found.")
        else:
            df = pd.DataFrame(data)
            st.write(df)
    except Exception as e:
        st.error(f"Error fetching to-do list: {str(e)}")

if __name__ == "__main__":
    main()
