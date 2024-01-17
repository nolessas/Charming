#To_do.py
import streamlit as st
from datetime import time, datetime
import pandas as pd
from google_sheets import get_sheets_service



def register_todo():
    st.write("")
    
    location_input = st.slider("1-100:", min_value=1, max_value=100, value=50)
    item_input = st.text_input("A thing:")
    if st.button("Add Entry"):
        add_item_to_sheet2(item_input, location_input)
    
    records = fetch_data_from_sheets2()
    if not records:
        st.write("No data available.")
    else:
        # Convert records to DataFrame
        df = pd.DataFrame(records)


    # Display each client with a checkbox
    for index, row in df.iterrows():
        if st.checkbox(f"{row['1-100']}{row['A thing']}, key=index):
            selected_indices.append(index)

    # Confirm deletion button
    if st.button('Confirm deletion of selected clients'):
        for i in selected_indices:
            delete_row_from_sheet2(i, records)  # Delete selected clients
        st.success("Selected clients deleted successfully!")
        st.experimental_rerun()  # Rerun the app to refresh the data display

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













