import os
import streamlit as st
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta

# Define the necessary scope(s) for the Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']

# Load Google Sheets service account credentials from Streamlit secrets
service_account_info_sheets = st.secrets["google_sheets_credentials"]
credentials_sheets = service_account.Credentials.from_service_account_info(
    service_account_info_sheets, scopes=SCOPES_SHEETS)
gc_sheets = gspread.authorize(credentials_sheets)

# Load Google Calendar service account credentials from Streamlit secrets
service_account_info_calendar = st.secrets["google_calendar_credentials"]
credentials_calendar = service_account.Credentials.from_service_account_info(
    service_account_info_calendar, scopes=SCOPES)

# Streamlit app title
st.title("Client Management App")

class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

if "registered_clients" not in st.session_state:
    st.session_state.registered_clients = []

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

# ... (other code)

def manage_todo_list():
    try:
        worksheet = gc_sheets.open_by_key('YOUR_SPREADSHEET_ID').worksheet('Sheet2')
        data = worksheet.get_all_records()

        if not data:
            st.write("No to-do items found.")
        else:
            df = pd.DataFrame(data)
            st.write(df)

            selected_indices = st.multiselect('Select rows to delete:', df.index)
            if st.button('Delete selected rows'):
                for i in sorted(selected_indices, reverse=True):
                    delete_row_from_sheet(i, data)
                st.rerun()

    except Exception as e:
        st.error(f"Error fetching to-do list: {str(e)}")

def delete_row_from_sheet(index, data):
    try:
        worksheet = gc_sheets.open_by_key('YOUR_SPREADSHEET_ID').worksheet('Sheet2')
        worksheet.delete_rows(index + 2)
        del data[index]
        st.success("Selected rows deleted successfully!")

    except Exception as e:
        st.error(f"Failed to delete row from sheet: {str(e)}")

# ... (other code)

if __name__ == "__main__":
    main()
