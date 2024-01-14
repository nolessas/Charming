#app.py
import os
import streamlit as st
from authentication import is_user_logged_in, show_login, set_user_logged_in
from datetime import datetime
import gspread
from google.oauth2 import service_account
import pandas as pd





SCOPES = ['https://www.googleapis.com/auth/calendar']
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']

service_account_info = st.secrets["google_oauth"]
credentials = service_account.Credentials.from_service_account_info(service_account_info)
gc = gspread.authorize(credentials)



def get_sheets_service():
    # Accessing service account credentials from Streamlit secrets
    service_account_info = st.secrets["google_oauth"]

    # Creating credentials from the service account info
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES_SHEETS)

    # Authorizing the gspread client with the credentials
    service = gspread.authorize(credentials)
    return service




class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

if "registered_clients" not in st.session_state:
    st.session_state.registered_clients = []

registered_clients = []



def main():
    st.title("Hello world")

    # Check if the user is logged in
    if not is_user_logged_in():
        show_login()
    else:
        show_dashboard()

        # You can add your logout logic here if needed
        logout_button = st.sidebar.button("Logout", on_click=set_user_logged_in, args=(False,))











def write_to_sheets(data):
    service = get_sheets_service()

    # Replace 'YOUR_SPREADSHEET_ID' with the actual ID of your Google Sheets document
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet1'

    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        
        # Check if we need to write the header row (only if the worksheet is empty)
        if worksheet.row_count == 0:
            header_row = ["Date", "Full Name", "Last Name", "Phone Number", "Note", "Email Sent"]
            worksheet.append_row(header_row)
        
        # Append the new data row, including a 'No' for 'Email Sent' status
        new_row = data + ['No']  # Add 'No' to indicate the email has not been sent
        worksheet.append_row(new_row)

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
        worksheet.delete_rows(index + 2)  # +2 to account for the header row and 1-indexing

        # Update the records list to reflect the deletion
        del records[index]

        st.sidebar.success("Selected rows deleted successfully!")

    except Exception as e:
        st.sidebar.error(f"Failed to delete row from sheet: {str(e)}")






def add_item_to_sheet2(item, location):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'  # Replace with your actual spreadsheet ID
    worksheet_name = 'Sheet2'  # The name of the worksheet where you want to add items
    
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        worksheet.append_row([item, location])
        st.sidebar.success("Item added successfully!")
    except Exception as e:
        st.sidebar.error(f"Failed to add item to sheet: {str(e)}")






####
def show_dashboard():
    choose_main = st.radio("", ("option1", "option2", "option3"))

    if choose_main == "option1":
        # Registration Section
        # ... (Your existing code for registration)

        # Simplified Client Display
        st.write("Displaying Registered Clients:")
        try:
            service = get_sheets_service()
            worksheet = service.open_by_key('1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ').worksheet('Sheet1')
            records = worksheet.get_all_records()
            if records:
                df = pd.DataFrame(records)
                st.dataframe(df)
            else:
                st.write("No registered clients found.")
        except Exception as e:
            st.error(f"Failed to fetch data from Google Sheets: {str(e)}")

    # ... (Rest of option2 and option3 code)






def delete_client(index):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet1'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        # Delete the row; add 2 to index to account for header row and 0-based indexing
        worksheet.delete_rows(index + 2)
        st.success(f"Client at row {index + 1} deleted successfully.")
        st.experimental_rerun()  # Rerun the app to refresh the data display
    except Exception as e:
        st.error(f"Failed to delete client: {str(e)}")

####










def show_dashboard():
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose_main = st.radio("", ("option1", "option2", "option3"))

    if choose_main == "option1":
        # Option 1: Show Registered Clients and Register New Client
        st.title("Registered Clients")
        show_registered_clients()

        st.title("Register New Client")
        # Input fields for registration
        date_input = st.date_input("Date:")
        hours_input = st.time_input("Time:")
        full_name_input = st.text_input("Full Name:")
        phone_input = st.text_input("Phone Number:")
        email_input = st.text_input("Email:")
        note_input = st.text_area("Note:")

        # Button for registering the client
        if st.button("Register"):
            register_client(date_input, hours_input, full_name_input, phone_input, email_input, note_input)
            st.success("Client registered successfully!")

    elif choose_main == "option2":
        # Option 2: Placeholder functionality
        st.title("Placeholder Functionality")
        # Add functionality for option 2 here

    elif choose_main == "option3":
        # Option 3: Add Item to Sheet2 and Display Data
        st.title("Data from Sheet3")
        st.write("Reikalingos priemones ir kur jas rasti.")

        item_input = st.text_input("Reikalingos priemones:", key="item")
        location_input = st.text_input("Kur:", key="location")
        if st.button("Add Entry", key="add"):
            add_item_to_sheet2(item_input, location_input)

        # Fetch and display data from Google Sheets
        records = fetch_data_from_sheets()
        if records:
            df = pd.DataFrame(records)
            # Add a selectbox for sorting options
            sort_option = st




def register_client(date, hours, full_name, phone, email, note):
    # Add the data to the list
    registered_clients.append({
        "Date": str(datetime.combine(date, hours)),
        "Full Name": full_name,
        "Phone Number": phone,
        "Email": email,
        "Note": note
    })

    # Format the data for Google Sheets
    sheet_data = [str(datetime.combine(date, hours)), full_name, phone, email, note]

    # Write data to Google Sheets
    write_to_sheets(sheet_data)

    st.success("Client registered successfully!")

# ... (rest of your existing functions)

if __name__ == "__main__":
    print("Before main()")
    main()
    print("After main()")







