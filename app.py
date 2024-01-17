#app.py
import os
import streamlit as st
from authentication import is_user_logged_in, show_login, set_user_logged_in, is_user_persistently_logged_in
from datetime import time, datetime
import gspread
from google.oauth2 import service_account
import pandas as pd
from streamlit_calendar import calendar
from kalendorius import display_calendar
import streamlit as st
from pathlib import Path
from client_managament import show_registered_clients, register_client1  
from google_sheets import get_sheets_service, write_to_sheets, delete_client
from data_base import show_clients_with_deletion_option, delete_row_from_sheet, fetch_data_from_sheets
from To_do import register_todo, manage_todo_list, add_item_to_sheet2, delete_row_from_sheet2, fetch_data_from_sheets2



SCOPES = ['https://www.googleapis.com/auth/calendar']
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']
service_account_info = st.secrets["google_oauth"]
credentials = service_account.Credentials.from_service_account_info(service_account_info)
gc = gspread.authorize(credentials)


def main():
    st.title("Charming")

    # Check if the user is logged in
    if not is_user_logged_in():
        show_login()
    else:
        show_dashboard()
        # Logout logic
        if st.sidebar.button("Logout", on_click=set_user_logged_in, args=(False,)):
            st.experimental_rerun()



def show_dashboard():
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose_main = st.radio("", ("1", "2", "3", "4","5"))

    if choose_main == "1":
        st.title("")

        show_registered_clients()
        register_client1()

    elif choose_main == "2":
        st.title("Calendar")
        display_calendar()

    elif choose_main == "3":
        st.title("List of clients")
        show_clients_with_deletion_option()

    elif choose_main == "4":
        st.title("ToDo")
        register_todo()
        #manage_todo_list()

    elif choose_main == "5":
        st.write("This tab is on development")


if __name__ == "__main__":
    main()