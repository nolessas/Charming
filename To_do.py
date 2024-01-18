#To_do.py
import streamlit as st
from datetime import time, datetime
import pandas as pd
from google_sheets import get_sheets_service


def register_todo():
    st.title("To-Do List")

    # User input fields to add a new to-do item
    kiek = st.slider("Kiek", min_value=1, max_value=100, value=50)
    ko = st.text_input("Ko", placeholder="Enter task description here...")

    # Button to add the new item
    if st.button("Add To-Do Item"):
        if ko:  # Ensure 'Ko' is not empty
            add_item_to_sheet2(kiek, ko)

    # Fetch and display current to-do list
    df = fetch_data_from_sheets2()
    if not df.empty:
        st.write("Current To-Do List:")
        # Display to-do list with checkboxes
        selected_indices = []
        for index, row in df.iterrows():
            if st.checkbox(f"{row['Kiek']} - {row['Ko']}", key=index):
                selected_indices.append(index + 2)  # +2 to account for header and 1-indexing in Sheets

        # Button to delete selected items
        if st.button('Delete Selected Items'):
            for i in selected_indices:
                delete_row_from_sheet2(i)
            st.rerun()


def add_item_to_sheet2(kiek, ko):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet2'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        worksheet.append_row([kiek, ko])
        st.success("Item added successfully!")
        st.experimental_rerun()  # Refresh the list after adding an item
    except Exception as e:
        st.error(f"Failed to add item to sheet: {str(e)}")


def delete_row_from_sheet2(index):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet2'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        worksheet.delete_rows(index)
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
        df = pd.DataFrame(records, columns=headers)
        # Convert 'Kiek' to numeric type, errors='coerce' will set invalid parsing as NaN
        df['Kiek'] = pd.to_numeric(df['Kiek'], errors='coerce')
        # Drop rows with NaN values in 'Kiek' column
        df = df.dropna(subset=['Kiek'])
        # Sort the DataFrame based on 'Kiek' column in descending order
        df = df.sort_values('Kiek', ascending=False)
        return df
    except Exception as e:
        st.error(f"Failed to fetch data from Google Sheets: {str(e)}")
        return pd.DataFrame()



