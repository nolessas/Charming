#data_base.py
import streamlit as st
from datetime import time, datetime
import pandas as pd
from google.oauth2 import service_account
from client_managament import get_sheets_service



SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']

def show_clients_with_date_filter(selected_date):
    st.title("Client Information")

    # Fetch data from Google Sheets
    records = fetch_data_from_sheets()

    if not records:
        st.write("No clients found.")
        return

    st.write("Client Information for Selected Date:")

    # Initialize an empty list to store indices of selected rows
    selected_indices = []

    # Display each client with a checkbox for the selected date
    for index, record in enumerate(records):
        date_string = record['Date']
        try:
            date_obj = datetime.strptime(date_string, "%d/%m/%Y").date()
            if date_obj == selected_date:
                if st.checkbox(f"{date_string}, {record['Full Name']}, {record['Phone Number']}, {record['Email']}, {record['Note']}", key=index):
                    selected_indices.append(index)
        except ValueError:
            pass

    if st.button('Confirm deletion of selected clients'):
        for i in selected_indices:
            delete_row_from_sheet(i, records)  # Delete selected clients
        st.success("Selected clients deleted successfully!")
        st.experimental_rerun()  # Rerun the app to refresh the data display



def delete_row_from_sheet(index, records):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet1'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        worksheet.delete_rows(index + 2)  # Adjust for header row and 1-indexing
        del records[index]
        st.success("Selected rows deleted successfully!")
    except Exception as e:
        st.error(f"Failed to delete row from sheet: {str(e)}")


#######?
def fetch_data_from_sheets():
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet1'  # Change this to 'Sheet1'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        records = worksheet.get_all_records()
        return records
    except Exception as e:
        st.error(f"Failed to fetch data from Google Sheets: {str(e)}")
        return []



















