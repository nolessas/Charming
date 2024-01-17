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

    # DEBUG: Print records to check structure
    st.write("Records:", records)

    # Initialize an empty list to store indices of selected rows
    selected_indices = []

    # Display each to-do item with a checkbox and a slider for importance
    for index, record in enumerate(records):
        col1, col2, col3 = st.columns(3)
        with col1:
            item_text = record.get('Item', 'No Item Label')  # Use .get to avoid KeyError
            if st.checkbox(item_text, key=index):
                selected_indices.append(index)
        with col2:
            # Assume that 'Importance' is a key in the record. If not, use a default value.
            importance = record.get('Importance', 50)  # Default importance value set to 50
            record['Importance'] = st.slider('Importance', min_value=0, max_value=100, value=importance, key=f'slider-{index}')
        with col3:
            # Display the second column as plain text; handle missing key with a default message
            second_col_text = record.get('Second Column', 'No Second Column Data')
            st.text(second_col_text)

    # If the delete button is pressed, delete all selected items
    if st.button('Delete selected items'):
        for i in selected_indices:
            delete_row_from_sheet2(i, records)  # Delete selected items
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













