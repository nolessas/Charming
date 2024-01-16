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

    # UI elements for selecting the view
    view = st.selectbox("Select View", ["Month", "Week", "Day"])
    selected_date = st.date_input("Select Date", datetime.today())

    # Convert selected_date to a pandas Timestamp for consistent comparison
    selected_date_ts = pd.Timestamp(selected_date)

    # Filter events based on the selected view
    if view == "Day":
        filtered_events = [event for event in event_list if pd.to_datetime(event['start']).date() == selected_date_ts.date()]
    elif view == "Week":
        week_start = selected_date_ts - pd.DateOffset(days=selected_date_ts.weekday())
        week_end = week_start + pd.DateOffset(days=7)
        filtered_events = [event for event in event_list if week_start <= pd.to_datetime(event['start']) < week_end]
    else:  # Month view
        month_start = selected_date_ts.replace(day=1)
        month_end = month_start + pd.DateOffset(months=1)
        filtered_events = [event for event in event_list if month_start <= pd.to_datetime(event['start']) < month_end]

    # Display the calendar with the filtered events list
    st.markdown('<div class="streamlit-calendar">', unsafe_allow_html=True)
    st_calendar.calendar(events=filtered_events)  # Your calendar component call
    st.markdown('</div>', unsafe_allow_html=True)