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
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet2'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        records = worksheet.get_all_records()
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
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet2'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        worksheet.delete_rows(index + 2)  # Adjust for header row and 1-indexing
        del records[index]
        st.sidebar.success("Selected rows deleted successfully!")
    except Exception as e:
        st.sidebar.error(f"Failed to delete row from sheet: {str(e)}")






def add_item_to_sheet2(item, location):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet2'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        worksheet.append_row([item, location])
        st.sidebar.success("Item added successfully!")
    except Exception as e:
        st.sidebar.error(f"Failed to add item to sheet: {str(e)}")






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

    if choose_main == "option3":
        st.title("Data from Sheet2")

        # Input fields for adding new entries to Sheet2
        item_input = st.text_input("Item:")
        location_input = st.text_input("Location:")
        if st.button("Add Entry"):
            add_item_to_sheet2(item_input, location_input)

        # Fetching and displaying data from Sheet2
        records = fetch_data_from_sheets()
        if records:
            df = pd.DataFrame(records)
            st.write(df)

            # Deletion of selected rows
            selected_indices = st.multiselect('Select rows to delete:', df.index)
            if st.button('Delete selected rows'):
                for i in sorted(selected_indices, reverse=True):
                    delete_row_from_sheet(i, records)  # Deleting the row from the sheet
                st.experimental_rerun()  # Rerun to refresh the data display
        else:
            st.write("No records found.")






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



if __name__ == "__main__":
    main()
