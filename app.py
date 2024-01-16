#app.py
import os
import streamlit as st
from authentication import is_user_logged_in, show_login, set_user_logged_in
from datetime import time, datetime
import gspread
from google.oauth2 import service_account
import pandas as pd
from kalendorius import display_calendar
import streamlit as st
from pathlib import Path
from streamlit_calendar import calendar
from client_managament import show_registered_clients, Register_client1  
from google_sheets import get_sheets_service, write_to_sheets, delete_client



SCOPES = ['https://www.googleapis.com/auth/calendar']
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']
service_account_info = st.secrets["google_oauth"]
credentials = service_account.Credentials.from_service_account_info(service_account_info)
gc = gspread.authorize(credentials)


def main():
    st.title("Hello world")

    # Check if the user is logged in
    if not is_user_logged_in():
        show_login()
    else:
        show_dashboard()

        # You can add your logout logic here if needed
        logout_button = st.sidebar.button("Logout", on_click=set_user_logged_in, args=(False,))



def show_dashboard():
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose_main = st.radio("", ("1", "2", "3", "4"))

    if choose_main == "option1":
        show_registered_clients()

    elif choose_main == "option2":
        st.title("Calendar")
        #show_clients_with_deletion_option()
        #display_calendar()

    elif choose_main == "option3":
        st.title("ToDo")
        #register_todo()

    elif choose_main == "option4":
        st.title("DoDo")


if __name__ == "__main__":
    main()