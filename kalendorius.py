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
def display_calendar():
    event_list = fetch_client_data_for_calendar()

    # UI elements for selecting the view
    view = st.selectbox("Select View", ["Month", "Week", "Day"])
    selected_date = st.date_input("Select Date", datetime.today())

    # Filter events based on the selected view
    if view == "Day":
        filtered_events = [event for event in event_list if pd.to_datetime(event['start']).date() == selected_date]
    elif view == "Week":
        week_start = selected_date - timedelta(days=selected_date.weekday())
        week_end = week_start + timedelta(days=7)
        filtered_events = [event for event in event_list if week_start <= pd.to_datetime(event['start']).date() < week_end]
    else:  # Month view
        month_start = selected_date.replace(day=1)
        month_end = month_start + pd.DateOffset(months=1)
        filtered_events = [event for event in event_list if month_start <= pd.to_datetime(event['start']).date() < month_end]

    # Display the calendar with the filtered events list
    st_calendar.calendar(events=filtered_events)



                                              
