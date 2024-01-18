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

    # Convert records to DataFrame
    df = pd.DataFrame(records)

    # Filter clients based on selected date
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce').dt.date
    filtered_df = df[df['Date'] == selected_date]

    if not filtered_df.empty:
        st.write("Client Information for Selected Date:")
        st.dataframe(filtered_df)
    else:
        st.write("No clients found for the selected date.")




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



















