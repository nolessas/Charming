# kalendorius.py
import streamlit as st
import streamlit_calendar as st_calendar
import pandas as pd
from google.oauth2 import service_account
import gspread
from datetime import datetime
from google_sheets import get_sheets_service  # Make sure to have this function in google_sheets.py

# Function to fetch client data from Google Sheets and format it for the calendar
#@st.cache
def fetch_client_data_for_calendar():
    service = get_sheets_service()
    worksheet = service.open_by_key('1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ').worksheet('Sheet1')
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)
    df['Date'] = pd.to_datetime(df['Date'])

    events = []
    for _, row in df.iterrows():
        event = {
            'start': row['Date'].isoformat(),
            'end': (row['Date'] + pd.DateOffset(hours=1)).isoformat(),
            'title': row['Full Name'],  # Display client's name
            'details': row['Note'],  # Additional details
            'color': 'blue'
        }
        events.append(event)
    return events

def display_detailed_info(event):
    st.subheader(f"Details for {event['title']}:")
    st.write(f"Date: {event['start']}")
    st.write(f"Note: {event['details']}")
    # Add more details you want to show
    # ...

def display_calendar():
    event_list = fetch_client_data_for_calendar()
    view = st.selectbox("Select View", ["Month", "Week", "Day"])
    selected_date = st.date_input("Select Date", datetime.today())
    selected_date_ts = pd.Timestamp(selected_date)

    filtered_events = [event for event in event_list if pd.to_datetime(event['start']).date() == selected_date_ts.date()]

    if view == "Week":
        week_start = selected_date_ts - pd.DateOffset(days=selected_date_ts.weekday())
        week_end = week_start + pd.DateOffset(days=7)
        filtered_events = [event for event in event_list if week_start <= pd.to_datetime(event['start']) < week_end]
    elif view == "Month":
        month_start = selected_date_ts.replace(day=1)
        month_end = month_start + pd.DateOffset(months=1)
        filtered_events = [event for event in event_list if month_start <= pd.to_datetime(event['start']) < month_end]

    st.markdown('<div class="streamlit-calendar">', unsafe_allow_html=True)
    for event in filtered_events:
        if st.button(event['title'], key=event['start']):
            display_detailed_info(event)
    st.markdown('</div>', unsafe_allow_html=True)

