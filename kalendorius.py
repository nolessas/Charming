#kalendorius.py
import streamlit as st
import streamlit_calendar as st_calendar
import pandas as pd
from google.oauth2 import service_account
import gspread
from streamlit_fullcalendar import FullCalendar


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

    events = []
    for _, row in df.iterrows():
        event = {
            'title': f"{row['Full Name']}, {row['Phone Number']}",
            'start': row['Date'].strftime("%Y-%m-%dT%H:%M:%S"),
            'end': (row['Date'] + pd.DateOffset(hours=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            'color': 'blue',
            'extendedProps': {
                'Phone': row['Phone Number'],
                'Email': row['Email'],
                'Note': row['Note']
            }
        }
        events.append(event)
    return events


# Modified display_calendar function to include client data
def display_calendar():
    event_list = fetch_client_data_for_calendar()
    calendar_config = {
        'initialView': 'dayGridMonth',  # Default view
        'headerToolbar': {
            'left': 'prev,next today',
            'center': 'title',
            'right': 'dayGridMonth,timeGridWeek,timeGridDay'  # Buttons for different views
        },
        'events': event_list
    }
    st_fullcalendar(calendar_config=calendar_config)#kalendorius.py
import streamlit as st
import streamlit_calendar as st_calendar
import pandas as pd
from google.oauth2 import service_account
import gspread
from streamlit_fullcalendar import FullCalendar


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

    events = []
    for _, row in df.iterrows():
        event = {
            'title': f"{row['Full Name']}, {row['Phone Number']}",
            'start': row['Date'].strftime("%Y-%m-%dT%H:%M:%S"),
            'end': (row['Date'] + pd.DateOffset(hours=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            'color': 'blue',
            'extendedProps': {
                'Phone': row['Phone Number'],
                'Email': row['Email'],
                'Note': row['Note']
            }
        }
        events.append(event)
    return events


# Modified display_calendar function to include client data
def display_calendar():
    event_list = fetch_client_data_for_calendar()
    calendar_config = {
        'initialView': 'dayGridMonth',  # Default view
        'headerToolbar': {
            'left': 'prev,next today',
            'center': 'title',
            'right': 'dayGridMonth,timeGridWeek,timeGridDay'  # Buttons for different views
        },
        'events': event_list
    }
    st_fullcalendar(calendar_config=calendar_config)
