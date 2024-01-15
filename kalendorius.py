#kalendorius.py
import streamlit as st
import streamlit_calendar as st_calendar
import pandas as pd
from google.oauth2 import service_account
import gspread
from datetime import datetime, timedelta

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

# Modified display_calendar function to include client data
def display_calendar():
    view_options = ["Day", "Week", "Month"]
    selected_view = st.radio("Choose Calendar View", view_options)
    
    event_list = fetch_client_data_for_calendar()
    today = datetime.today()

    if selected_view == "Day":
        start_date = today
        end_date = today + timedelta(days=1)
    elif selected_view == "Week":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=7)
    else:  # Month
        start_date = today.replace(day=1)
        end_date = (start_date + pd.DateOffset(months=1)) - timedelta(days=1)

    st_calendar.calendar(
        events=event_list,
        start_date=start_date,
        end_date=end_date
    )







                                              
