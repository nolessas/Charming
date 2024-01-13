#app.py
import os
import streamlit as st
from authentication import is_user_logged_in, show_login, set_user_logged_in
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from hashlib import sha256
import gspread
from google.oauth2 import service_account
import pandas as pd



service_account_info = st.secrets["service_account"]
credentials = service_account.Credentials.from_service_account_info(service_account_info)
gc = gspread.authorize(credentials)




class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

if "registered_clients" not in st.session_state:
    st.session_state.registered_clients = []

registered_clients = []



def main():
    st.title("")

    # Check if the user is logged in
    if not is_user_logged_in():
        show_login()
    else:
        show_dashboard()

        # You can add your logout logic here if needed
        logout_button = st.sidebar.button("Logout", on_click=set_user_logged_in, args=(False,))





def get_sheets_service():
    credentials = service_account.Credentials.from_service_account_file(
        '.streamlit/key.json', scopes=SCOPES_SHEETS
    )

    service = gspread.authorize(credentials)
    return service






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





def get_calendar_service():
    credentials = None

    # Load or create credentials
    if os.path.exists('.streamlit/token.json'):
        credentials = Credentials.from_authorized_user_file('.streamlit/token.json')

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES_CLIENT)
            credentials = flow.run_local_server(port=0)

        with open('.streamlit/token.json', 'w') as token:
            token.write(credentials.to_json())

    # Build the Google Calendar service
    service = build(API_NAME, API_VERSION, credentials=credentials)
    return service


    # Sidebar logic
    choose_sidebar = st.sidebar.radio("Choose an option", ("app1", "app2"))

    # Main logic
    choose_main = st.radio("View section", ("option1", "option2", "option3", "option4"))



def show_dashboard():
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose_main = st.radio("", ("option1", "option2", "option3", "option4"))

    if choose_main == "option2":
        st.title("Today's Events")

        # Google Calendar API
        service = get_calendar_service()

        # Fetch today's events
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=(datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        
        if not events:
            st.write("No events found.")
        else:
            for event in events:
                start_time = event['start'].get('dateTime', event['start'].get('date'))
                event_summary = event.get('summary', 'No summary provided')
                st.write(f"{start_time} - {event_summary}")

    elif choose_main == "option1":
        st.write("")
        show_registered_clients()  # Function to display clients from Google Sheets


    elif choose_main == "option3":
        st.title("Data from Sheet3")
        st.write("Reikalingos priemones ir kur jas rasti.")

        # Fetch data from Google Sheets
        records = fetch_data_from_sheets()

        if not records:
            return

        df = pd.DataFrame(records)

        # Add a selectbox for sorting options
        sort_option = st.selectbox("Sort by:", df.columns, index=1)  # Set index to 1 for selecting the second column

        # Checkbox for sorting order
        sort_ascending = st.checkbox("Rušiavimas", value=True)

        # Sort the DataFrame based on the selected column
        df = df.sort_values(by=[sort_option], ascending=[sort_ascending])

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
                    delete_row_from_sheet(index, records)  # Call function to delete the row


    elif choose_main == "option4":
        st.title("Client Information")

        # Placeholder for displaying client information
        st.write("Client information will be displayed here.")

    choose_sidebar = st.sidebar.radio("", ("app1", "app2"))
    if choose_sidebar == "app1":
        st.sidebar.title("Register Client")

        # Input fields for registration
        date_input = st.sidebar.date_input("Date:")
        hours_input = st.sidebar.time_input("Time:")
        full_name_input = st.sidebar.text_input("Full Name:")
        phone_input = st.sidebar.text_input("Phone Number:")
        email_input = st.sidebar.text_input("Email:")
        note_input = st.sidebar.text_area("Note:")

        # Button for registering the client
        if st.sidebar.button("Register"):
            # Placeholder function for handling registration
            register_client(date_input, hours_input, full_name_input, phone_input, email_input, note_input)
            st.sidebar.success("Client registered successfully!")

    if choose_sidebar == "app2":
        item_input = st.sidebar.text_input("Reikalingos priemones:", key="item")
        location_input = st.sidebar.text_input("Kur:", key="location")
        if st.sidebar.button("Add Entry", key="add"):
            add_item_to_sheet2(item_input, location_input)


def register_client(date, hours, full_name, phone, email, note):
    # Placeholder function for handling client registration
    # You can add the logic to save the client information to a database or file
    # For now, it just prints the information
    print(f"Registered Client:")
    print(f"Date: {date}")
    print(f"Hours: {hours}")
    print(f"Full Name: {full_name}")
    print(f"Phone Number: {phone}")
    print(f"Email: {email}")
    print(f"Note: {note}")



def register_client(date, hours, full_name, phone, email, note):
    # ... (your existing code)

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

    # Google Calendar API
    service = get_calendar_service()

    # Format the event start time
    start_datetime = datetime.combine(date, hours)

    # Format the event end time (assuming it's 30 minutes later)
    end_datetime = start_datetime + timedelta(minutes=30)

    # Create event
    event = {
        'summary': f"Client Registration - {full_name}",
        'description': f"Client details:\nFull Name: {full_name}\nPhone: {phone}\nEmail: {email}\nNote: {note}",
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'UTC',  # Replace with your desired time zone
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'UTC',  # Replace with your desired time zone
        },
    }

    try:
        service.events().insert(calendarId='primary', body=event).execute()
        st.sidebar.success("Client registered successfully and event created in Google Calendar!")
    except HttpError as e:
        st.sidebar.error(f"Error creating event: {str(e)}")

if __name__ == "__main__":
    print("Before main()")
    main()
    print("After main()")
