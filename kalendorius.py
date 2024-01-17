# kalendorius.py
import streamlit as st
import streamlit_calendar as st_calendar
import pandas as pd
from google.oauth2 import service_account
import gspread
from datetime import datetime


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
            'start': row['Date'].isoformat(),
            'end': (row['Date'] + pd.DateOffset(hours=1)).isoformat(),
            'color': 'blue'  # or any other color
        }
        events.append(event)
    return events


def display_calendar():
    event_list = fetch_client_data_for_calendar()
    current_month = pd.Timestamp(datetime.today()).replace(day=1)

    # Assuming we only want to show events for the current month
    month_start = current_month
    month_end = month_start + pd.DateOffset(months=1)
    filtered_events = [event for event in event_list if month_start <= pd.to_datetime(event['start']) < month_end]

    # Display the calendar with the filtered events list for the current month
    st.markdown('<div class="streamlit-calendar">', unsafe_allow_html=True)
    st_calendar.calendar(events=filtered_events, default_view="month")  # Your calendar component call with month view
    st.markdown('</div>', unsafe_allow_html=True)