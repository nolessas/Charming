import streamlit as st
import streamlit_calendar as st_calendar
import pandas as pd
from google.oauth2 import service_account
import gspread


# Function to get Google Sheets service
def get_sheets_service():
    service_account_info = st.secrets["google_oauth"]
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    return gspread.authorize(credentials)

# Function to fetch client data from Google Sheets and format it for the calendar
def fetch_client_data_for_calendar():
    service = get_sheets_service()
    worksheet = service.open_by_key('1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ').worksheet('Sheet1')
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)
    df['Date'] = pd.to_datetime(df['Date'])

    # Format data for calendar
    events = []
    for _, row in df.iterrows():
        event = {
            'title': row['Date'].strftime('%H:%M'),  # Display only hours and minutes
            'start': row['Date'].isoformat(),
            'end': (row['Date'] + pd.DateOffset(hours=1)).isoformat(),  # Assuming 1 hour duration per client
            'color': 'blue'  # Customize color if needed
        }
        events.append(event)
    return events

# Modified display_calendar function to include client data
def display_calendar():
    event_list = fetch_client_data_for_calendar()
    st_calendar.calendar(events=event_list)
