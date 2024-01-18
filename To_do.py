#To_do.py
import streamlit as st
from datetime import time, datetime
import pandas as pd
from google_sheets import get_sheets_service


def register_todo():
    st.title("")

    # Fetch data from Google Sheets
    records = fetch_data_from_sheets2()

    if not records:
        st.write("No clients found.")
        return

    # Convert records to DataFrame
    df = pd.DataFrame(records)

    # Initialize an empty list to store indices of selected rows
    selected_indices = []

    # Display each client with a checkbox
    for index, row in df.iterrows():
        if st.checkbox(f"{row['Keik']}{row['Ko']}", key=index):
            selected_indices.append(index)

    # Confirm deletion button
    if st.button('Confirm deletion of selected clients'):
        for i in selected_indices:
            delete_row_from_sheet2(i, records)  # Delete selected clients
        st.success("Selected clients deleted successfully!")
        st.rerun()  # Rerun the app to refresh the data display
    


def add_item_to_sheet2(item, location):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet2'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        worksheet.append_row([item, location])
        st.success("Item added successfully!")
    except Exception as e:
        st.error(f"Failed to add item to sheet: {str(e)}")

def delete_row_from_sheet2(index, records):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet2'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        worksheet.delete_rows(index + 2)  # Adjust for header row and 1-indexing
        del records[index]
        st.success("Selected rows deleted successfully!")
    except Exception as e:
        st.error(f"Failed to delete row from sheet: {str(e)}")

def fetch_data_from_sheets2():
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet2'  # Change this to 'Sheet1'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        records = worksheet.get_all_records()
        return records
    except Exception as e:
        st.error(f"Failed to fetch data from Google Sheets: {str(e)}")
        return []













