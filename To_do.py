#To_do.py
import streamlit as st
from datetime import time, datetime
import pandas as pd
from google_sheets import get_sheets_service


def manage_todo_list():
    st.title("To-Do List")

    # Fetch data from Google Sheets
    records = fetch_data_from_sheets2()

    if not records:
        st.write("No to-do items found.")
        return
    
    # Initialize a session state for selected items if it doesn't exist
    if 'selected_items' not in st.session_state:
        st.session_state.selected_items = []

    # Get the list of column names from the first record, assuming all records follow the same format
    column_names = records[0].keys() if records else []

    # Display each item with a checkbox
    for index, record in enumerate(records):
        # Use the first column name as the key for the item text
        item_text = record[column_names[0]] if column_names else "Undefined"
        # Create a unique key for the checkbox using the index
        checkbox_key = f"delete_{index}"

        # Use columns for layout
        col1, col2 = st.columns([1, 4])
        with col1:
            # Create a checkbox and save its state
            checked = st.checkbox("", key=checkbox_key)
        with col2:
            # Display the item text
            st.write(item_text)
        
        # If the checkbox is checked, add the index to the list of selected items
        if checked:
            st.session_state.selected_items.append(index)

    # Button to delete selected items
    if st.button("Delete selected items"):
        # Reverse sort the selected items to avoid index errors during deletion
        for index in sorted(st.session_state.selected_items, reverse=True):
            delete_row_from_sheet2(index + 2, records)  # Adjust for Google Sheets indexing
        # Clear the selected items after deletion
        st.session_state.selected_items = []
        st.rerun()  # Rerun the app to refresh the data display after deletion


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













