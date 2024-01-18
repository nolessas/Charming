#To_do.py
import streamlit as st
from datetime import time, datetime
import pandas as pd
from google_sheets import get_sheets_service


def register_todo():
    st.title("To-Do List")

    # Display current to-do list
    records = fetch_data_from_sheets2()

    if records:
        # Convert records to DataFrame
        df = pd.DataFrame(records)
        st.write("Current To-Do List:")
        st.dataframe(df)  # Display the current to-do list
    else:
        st.write("No to-do items found.")

    # User input fields to add a new to-do item
    kiek = st.slider("Kiek", min_value=1, max_value=100, value=50)
    ko = st.text_input("Ko")

    # Button to add the new item
    if st.button("Add To-Do Item"):
        if ko:  # Make sure 'Ko' is not empty
            try:
                add_item_to_sheet2(kiek, ko)
                st.success("To-Do item added successfully!")
                st.experimental_rerun()  # Refresh the page to show updated data
            except Exception as e:
                st.error(f"Failed to add item to sheet: {str(e)}")
        else:
            st.error("Please enter some text for 'Ko'.")


def add_item_to_sheet2(kiek, ko):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet2'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        worksheet.append_row([kiek, ko])
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
    worksheet_name = 'Sheet2'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        data = worksheet.get_all_values()
        headers = data[0]  # Assumes the first row is the header
        records = data[1:]  # The rest is data
        return [dict(zip(headers, record)) for record in records]
    except Exception as e:
        st.error(f"Failed to fetch data from Google Sheets: {str(e)}")
        return []











