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
        df = pd.DataFrame(records)

        # Checkbox for sorting order
        sort_ascending = st.checkbox("Rušiavimas", value=False)  # Set to True for ascending order

        # Sort the DataFrame based on the second column (numbers)
        df = df.sort_values(by=[df.columns[1]], ascending=[sort_ascending])

        # Display the data frame as a list with a delete button for each row
        for index, row in df.iterrows():
            # Create columns for layout
            col1, col2, col3, col4, col5 = st.columns(5)  # Create columns for layout
            with col1:
                if len(row) > 0:
                    st.write(row[0])  # Display the first column of the row
            with col2:
                if len(row) > 1:
                    st.write(row[1])  # Display the second column of the row
            with col3:
                if len(row) > 2:
                    st.write(row[2])  # Display the third column of the row
            with col4:
                if len(row) > 3:
                    st.write(row[3])  # Display the fourth column of the row
            with col5:
                # Add a delete button for each row in the fifth column
                if st.button(f"Delete Row {index + 1}"):
                    delete_row_from_sheet2(index, records)  # Call function to delete the row
                    st.rerun()  # Rerun

def manage_todo_list():
    st.title("To-Do List")

    # Fetch data from Google Sheets
    records = fetch_data_from_sheets2()

    if not records:
        return

    df = pd.DataFrame(records)
    st.write(df)

    # Deletion of selected rows
    selected_indices = st.multiselect('Select rows to delete:', df.index)
    if st.button('Delete selected rows'):
        # Reverse sort indices so we delete from the bottom of the list first
        for i in sorted(selected_indices, reverse=True):
            delete_row_from_sheet(i, records)  # Call function to delete the row
        st.rerun()
    
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












