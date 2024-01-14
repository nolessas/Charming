import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread
from datetime import datetime, timedelta

# Google Sheets and Google Calendar API scopes
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']
SCOPES_CALENDAR = ['https://www.googleapis.com/auth/calendar']

# Load Google Sheets service account credentials from Streamlit secrets
service_account_info_sheets = st.secrets["google_sheets_credentials"]
credentials_sheets = service_account.Credentials.from_service_account_info(
    service_account_info_sheets, scopes=SCOPES_SHEETS)
gc_sheets = gspread.authorize(credentials_sheets)

# Load Google Calendar service account credentials from Streamlit secrets
service_account_info_calendar = st.secrets["google_calendar_credentials"]
credentials_calendar = service_account.Credentials.from_service_account_info(
    service_account_info_calendar, scopes=SCOPES_CALENDAR)

# Function to create a Google Calendar event
def create_calendar_event(client_name, appointment_time):
    service_calendar = build('calendar', 'v3', credentials=credentials_calendar)

    event = {
        'summary': f'Appointment with {client_name}',
        'description': 'Client appointment',
        'start': {
            'dateTime': appointment_time.isoformat(),
            'timeZone': 'UTC',  # Replace with your desired time zone
        },
        'end': {
            'dateTime': (appointment_time + timedelta(minutes=30)).isoformat(),
            'timeZone': 'UTC',
        },
    }

    event = service_calendar.events().insert(calendarId='primary', body=event).execute()

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
        worksheet = gc_sheets.open_by_key('YOUR_SPREADSHEET_ID').worksheet('Sheet1')

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
        worksheet = gc_sheets.open_by_key('YOUR_SPREADSHEET_ID').worksheet('Sheet1')
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
        worksheet = gc_sheets.open_by_key('YOUR_SPREADSHEET_ID').worksheet('Sheet2')
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
