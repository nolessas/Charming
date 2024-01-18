#data_base.py
import streamlit as st
from datetime import time, datetime
import pandas as pd
from client_managament import get_sheets_service



def show_clients_with_deletion_option(selected_date):
    st.title("")

    # Fetch data from Google Sheets
    records = fetch_data_from_sheets()

    if not records:
        st.write("No clients found.")
        return

    # Convert records to DataFrame
    df = pd.DataFrame(records)

    # Filter clients for the selected date
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    df = df[df['Date'].dt.date == selected_date]

    # Initialize an empty list to store indices of selected rows
    selected_indices = []

    # Display each client with a checkbox
    for index, row in df.iterrows():
        if st.checkbox(f"{row['Date'].strftime('%d/%m/%Y')}, {row['Full Name']}, {row['Phone Number']}, {row['Email']}, {row['Note']}", key=index):
            selected_indices.append(index)

    # Confirm deletion button
    if st.button('Confirm deletion of selected clients'):
        for i in selected_indices:
            delete_row_from_sheet(i, records)  # Delete selected clients
        st.success("Selected clients deleted successfully!")
        st.experimental_rerun()  # Rerun the app to ref


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



















