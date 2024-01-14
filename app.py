import os
import streamlit as st
from authentication import is_user_logged_in, show_login, set_user_logged_in
import gspread
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime
from datetime import timedelta

# Define the necessary scope(s) for the Google Calendar API
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']

service_account_info = st.secrets["google_oauth"]
credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES_SHEETS)
gc = gspread.authorize(credentials)

class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

if "registered_clients" not in st.session_state:
    st.session_state.registered_clients = []

def main():
    st.title("")

    # Check if the user is logged in
    if not is_user_logged_in():
        show_login()
    else:
        show_dashboard()

        # You can add your logout logic here if needed
        logout_button = st.sidebar.button("Logout", on_click=set_user_logged_in, args=(False,))

def get_credentials():
    try:
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )
    except Exception as e:
        print(f"Error initializing credentials: {e}")
        raise e

# Modify the write_to_sheets function
def write_to_sheets(data):
    service = get_sheets_service()

    # Replace 'YOUR_SPREADSHEET_ID' with the actual ID of your Google Sheets document
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet1'

    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        
        # Check if we need to write the header row (only if the worksheet is empty)
        if worksheet.row_count == 0:
            header_row = ["Date", "Full Name", "Phone Number", "Note"]
            worksheet.append_row(header_row)
        
        # Append the new data row
        worksheet.append_row(data)

    except Exception as e:
        st.error(f"Error writing to Google Sheets: {str(e)}")

def fetch_data_from_sheets():
    try:
        service = get_sheets_service()
        spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
        worksheet_name = 'Sheet2'
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        records = worksheet.get_all_records()

        if not records:
            st.write("No to-do items found.")
            return []

        return records

    except Exception as e:
        st.error(f"Failed to fetch data from Google Sheets: {str(e)}")
        return []

def manage_todo_list():
    st.title("To-Do List")

    # Fetch data from Google Sheets
    records = fetch_data_from_sheets()

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

def delete_row_from_sheet(index, records):
    try:
        service = get_sheets_service()
        spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
        worksheet_name = 'Sheet2'

        # Delete the row from the Google Sheets
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        worksheet.delete_rows(index + 2)  # +2 to account for the header row and 0-based indexing

        # Update the records list to reflect the deletion
        del records[index]

        st.sidebar.success("Selected rows deleted successfully!")

    except Exception as e:
        st.sidebar.error(f"Failed to delete row from sheet: {str(e)}")

def get_sheets_service():
    credentials = get_credentials()
    return gspread.authorize(credentials)

####

def show_registered_clients():
    st.title("Registered Clients")

    service = get_sheets_service()

    try:
        worksheet = service.open_by_key('1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ').worksheet('Sheet1')
        records = worksheet.get_all_records()

        if records:
            df = pd.DataFrame(records)
            df['Date'] = pd.to_datetime(df['Date'])

            # Add radio buttons for filtering by time range (Day, Week, Month, Year)
            time_range = st.radio("Filter by Time Range", ["Day", "Week", "Month", "Year"])

            # Calculate the start date based on the selected time range
            if time_range == "Day":
                start_date = pd.Timestamp.now().normalize()
            elif time_range == "Week":
                start_date = pd.Timestamp.now() - pd.DateOffset(weeks=1)
            elif time_range == "Month":
                start_date = pd.Timestamp.now() - pd.DateOffset(months=1)
            elif time_range == "Year":
                start_date = pd.Timestamp.now() - pd.DateOffset(years=1)
            else:
                start_date = pd.Timestamp(1970, 1, 1)  # Default to a very old date

            # Filter the dataframe based on the selected time range
            if time_range == "Day":
                filtered_df = df[df['Date'].dt.date == start_date.date()]
            else:
                filtered_df = df[df['Date'] >= start_date]

            # Sort the dataframe by Date column
            filtered_df = filtered_df.sort_values(by=["Date"])

            st.write("Client Information:")
            for index, row in filtered_df.iterrows():
                # Create columns for layout
                col1, col2 = st.columns([4, 1])  # Adjust the ratio as needed

                # Display client information in the first column
                with col1:
                    st.write(f"Date: {row['Date']}")
                    st.write(f"Full Name: {row['Full Name']}")
                    st.write(f"Phone Number: {row['Phone Number']}")
                    st.write(f"Email: {row['Email']}")
                    st.write(f"Note: {row['Note']}")
                    st.write(f"Email Sent: {row['Email Sent']}")

                # Display delete button in the second column
                with col2:
                    delete_button_label = f"Delete {row['Full Name']}"
                    if st.button(delete_button_label, key=f"delete_{index}"):
                        delete_client(index)

                # Add a horizontal line as a separator after each client
                st.markdown("---")


        else:
            st.write("No registered clients found.")
    except Exception as e:
        st.error(f"Failed to fetch data from Google Sheets: {str(e)}")

def add_item_to_sheet2(item_input, location_input):
    try:
        service = get_sheets_service()
        spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
        worksheet_name = 'Sheet2'

        # Add your code to write the item and location data to Google Sheets here

        st.success("Item added successfully!")  # Display a success message

    except Exception as e:
        st.error(f"Failed to add item: {str(e)}")

def delete_client(index):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet1'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        # Delete the row; add 2 to index to account for header row and 0-based indexing
        worksheet.delete_rows(index + 2)
        st.success(f"Client at row {index + 1} deleted successfully.")
        st.rerun()  # Rerun the app to refresh the data display
    except Exception as e:
        st.error(f"Failed to delete client: {str(e)}")

if __name__ == "__main__":
    main()
