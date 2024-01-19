#app.py
import os
import streamlit as st
from authentication import is_user_logged_in, show_login, set_user_logged_in, generate_session_token
from datetime import time, datetime
import gspread
from google.oauth2 import service_account
import pandas as pd
from streamlit_calendar import calendar
from kalendorius import display_calendar
import streamlit as st
from pathlib import Path
from client_managament import show_registered_clients, register_client1, get_sheets_service, write_to_sheets, delete_client, update_client_note, add_client_note, display_client_note, edit_appointment_details, archive_old_clients
from data_base import show_clients_with_date_filter, delete_row_from_sheet, fetch_data_from_sheets
from To_do import register_todo, add_item_to_sheet2, delete_row_from_sheet2, fetch_data_from_sheets2

st.image("logo2.png")

SCOPES = ['https://www.googleapis.com/auth/calendar']
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']
service_account_info = st.secrets["google_oauth"]
credentials = service_account.Credentials.from_service_account_info(service_account_info)
gc = gspread.authorize(credentials)


def main():
    # Check for session token and set logged in status
    if "session_token" in st.session_state and st.session_state["session_token"]:
        set_user_logged_in(True)

    # Attempt to display content after login
    if is_user_logged_in():
        show_dashboard()  # This function displays your app's content
    else:
        show_login()



def show_dashboard():
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose_main = st.radio("", ("1", "2", "3", "4","5","6"))

    if choose_main == "1":
        st.title("")
        show_registered_clients()
        register_client1()
    if st.button('Archive Old Clients'):
        archive_old_clients()


    elif choose_main == "2":
        st.title("Kalendorius")
        display_calendar()
        # URL to Google Calendar
        google_calendar_url = "https://calendar.google.com/calendar/u/0/r/month/2024/1/1"
        google_sheets_url = "https://docs.google.com/spreadsheets/d/1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ/edit#gid=0"
        # Using markdown to open link in a new tab
        if st.button('Open Sheets or Calendar'):
            st.markdown(f'<a href="{google_calendar_url}" target="_blank">Click here to open Google Calendar</a>', unsafe_allow_html=True)
            st.markdown(f'<a href="{google_sheets_url}" target="_blank">Click here to open Google Sheets</a>', unsafe_allow_html=True)

    elif choose_main == "3":
        st.title("Pašalinti klientą")
        selected_date = st.date_input("Pasirinkite dieną:")
        show_clients_with_date_filter(selected_date)  # Call the new function


    elif choose_main == "4":
        st.title("")
        register_todo()

    elif choose_main == "5":
        st.title("Pakoreguoti kliento pastabas")
        # Inside the relevant section of your Streamlit app
        client_name_search = st.text_input("Įveskite kliento Vardą Pavardę:")

        if client_name_search:
            row_number = display_client_note(client_name_search)
            
            new_note = st.text_area("Nauja pastaba " + client_name_search, height=150)

            if st.button('Update Note') and row_number is not None:
                update_client_note(row_number, client_name_search, new_note)

    elif choose_main == "6":
        st.title("Keisti kliento atvykimo dieną")
        # Provide an input to enter the client's name
        client_name_to_edit = st.text_input("Iveskite kliento Vardą Pavardę:")
        if client_name_to_edit:
            # Call the function to edit appointment details
            edit_appointment_details(client_name_to_edit)
        # app.py or within a specific part of your Streamlit application


if __name__ == "__main__":
    main()