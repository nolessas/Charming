#To_do.py
import streamlit as st
from datetime import time, datetime
import pandas as pd
from google_sheets import get_sheets_service


import streamlit as st
from google_sheets import get_sheets_service

def manage_todo_list():
    st.title("To-Do List")

    # Fetch data from Google Sheets
    records = fetch_data_from_sheets()

    if not records:
        st.write("No to-do items found.")
        return

    # Initialize a session state to store indices of items to delete
    if 'delete_todo' not in st.session_state:
        st.session_state.delete_todo = []

    # Iterate over the records and display them with checkboxes
    for index, record in enumerate(records):
        # Assuming 'Item' is a key in the record
        item_text = record.get('Item', 'Unnamed Item')
        # Create a checkbox for the current record
        if st.checkbox(item_text, key=f"todo-{index}"):
            # If checked, add the index to the list of items to delete
            st.session_state.delete_todo.append(index)

    # Button to delete selected items
    if st.button("Delete Selected Items"):
        # Get a reference to the Google Sheet
        service = get_sheets_service()
        sheet = service.open_by_key('your-spreadsheet-key').sheet1

        # Reverse the indices to delete items from the end of the list
        for index in sorted(st.session_state.delete_todo, reverse=True):
            # Delete the row from the sheet using the index
            sheet.delete_row(index + 2)  # +2 to account for header and 1-based indexing

        # Clear the selected items and rerun to refresh the display
        st.session_state.delete_todo = []
        st.experimental_rerun()

# Utility functions
def fetch_data_from_sheets():
    # Fetch data from Google Sheets and return as a list of dictionaries
    # This is a placeholder - replace with your actual data fetching logic
    return []

def ge


def manage_todo_list():
    st.title("To-Do List")

    # Fetch data from Google Sheets
    records = fetch_data_from_sheets2()

    if not records:
        st.write("No to-do items found.")
        return

    # Create a dictionary to hold the checkbox state for each item
    checkbox_states = {}

    # Display each to-do item with a checkbox
    for index, record in enumerate(records):
        # Use the index and item text to create a unique key for each checkbox
        key = f"checkbox-{index}-{record['Item']}"
        checkbox_states[key] = st.checkbox(record['Item'], key=key)

    # If the delete button is pressed, delete all selected items
    if st.button('Delete selected items'):
        # Iterate over the checkbox_states to see which items were selected for deletion
        for key, checked in checkbox_states.items():
            if checked:
                index_to_delete = int(key.split('-')[1]) + 2  # Extract the index and adjust for Google Sheets
                delete_row_from_sheet2(index_to_delete, records)
        st.experimental_rerun()  # Rerun the app to refresh the data display after deletion


    
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













