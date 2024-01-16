# kalendorius.py
import streamlit as st
import pandas as pd
from datetime import datetime
from google_sheets import get_sheets_service  # Ensure this function is correctly defined in google_sheets.py

#@st.cache
def fetch_client_data_for_calendar():
    service = get_sheets_service()
    worksheet = service.open_by_key('1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ').worksheet('Sheet1')
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Debugging: Check the DataFrame content
    st.write("DataFrame content:")  # This will print the dataframe content in the app
    st.write(df)

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

    # Debugging: Check the events list
    st.write("Events list:")  # This will print the events list in the app
    st.write(events)

    return events

def display_calendar():
    event_list = fetch_client_data_for_calendar()
    view = st.selectbox("Select View", ["Month", "Week", "Day"])
    selected_date = st.date_input("Select Date", datetime.today())
    selected_date_ts = pd.Timestamp(selected_date)

    # Initialize filtered_events outside of the if-elif blocks to ensure it's always defined
    filtered_events = []

    if view == "Day":
        filtered_events = [event for event in event_list if pd.to_datetime(event['start']).date() == selected_date_ts.date()]
    elif view == "Week":
        week_start = selected_date_ts - pd.DateOffset(days=selected_date_ts.weekday())
        week_end = week_start + pd.DateOffset(days=7)
        filtered_events = [event for event in event_list if week_start <= pd.to_datetime(event['start']) < week_end]
    elif view == "Month":
        month_start = selected_date_ts.replace(day=1)
        month_end = month_start + pd.DateOffset(months=1)
        filtered_events = [event for event in event_list if month_start <= pd.to_datetime(event['start']) < month_end]

    # Debugging: Check if events are being filtered correctly
    st.write("Filtered events:")  # This will print the filtered events in the app
    st.write(filtered_events)

    st.markdown('<div class="streamlit-calendar">', unsafe_allow_html=True)
    for event in filtered_events:
        if st.button(event['title'], key=event['start']):
            st.write(event)  # Debug: Print the event data
            display_detailed_info(event)