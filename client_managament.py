#client_managament.py
import streamlit as st
from datetime import datetime, time, timedelta, date
import pandas as pd
import gspread
from google_sheets import write_to_sheets, get_sheets_service, delete_client


#class SessionState:
    #def __init__(self, **kwargs):
        #for key, val in kwargs.items():
            #setattr(self, key, val)

#if "registered_clients" not in st.session_state:
    #st.session_state.registered_clients = []
 #   1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ
#registered_clients = []


def get_unique_headers(worksheet):
    headers = worksheet.row_values(1)
    return len(headers) == len(set(headers)), headers

day_name_map = {
    'Monday': 'Pirmadienis',
    'Tuesday': 'Antradienis',
    'Wednesday': 'Trečiadienis',
    'Thursday': 'Ketvirtadienis',
    'Friday': 'Penktadienis',
    'Saturday': 'Šeštadienis',
    'Sunday': 'Sekmadienis'
}


def show_registered_clients():
    service = get_sheets_service()
    try:
        spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
        worksheet_name = 'Sheet1'
        
        # Open the worksheet
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        
        # Read all records
        records = worksheet.get_all_records()
        
        if records:
            df = pd.DataFrame(records)

            # Convert 'Date' to datetime
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

            # Filter options
            time_filter = st.radio(
                "Filter by:",
                ('Day', 'Week', 'Month'),
                index=0  # Default is 'Day'
            )

            # Filter based on the selected time period
            today = datetime.today()
            if time_filter == 'Day':
                df = df[df['Date'] == today.date()]
            elif time_filter == 'Week':
                week_start = today - timedelta(days=today.weekday())  # Calculate the start of the week
                week_end = week_start + timedelta(days=6)
                df = df[(df['Date'] >= week_start.date()) & (df['Date'] <= week_end.date())]
            elif time_filter == 'Month':
                df = df[df['Date'].dt.month == today.month]

            # Add day name in Lithuanian
            df['Weekday'] = df['Date'].dt.day_name().map(day_name_map)
            
            # Convert 'Phone Number' to string
            if 'Phone Number' in df.columns:
                df['Phone Number'] = df['Phone Number'].astype(str)

            # Set the 'Weekday' column as the index of the DataFrame
            df.set_index('Weekday', inplace=True)

            # Display the filtered DataFrame
            st.write("Client Information:")
            st.dataframe(df)
        else:
            st.write("No registered clients found.")
    except Exception as e:
        st.error(f"Failed to fetch data from Google Sheets: {str(e)}")



# The rest of your Streamlit app code, including register_client1 and other components
# Don't forget to call show_registered_clients() in your main app flow to display the data

# Example call within your Streamlit layout:
if st.sidebar.button('Show Registered Clients'):
    show_registered_clients()


def register_client1():
    st.title("Register New Client")

    # Input fields for registration
    date_input = st.date_input("Date:")
    time_in = st.slider("Time In:", value=time(8, 0), format="HH:mm", key='time_in')
    duration = st.slider("Duration (hours):", min_value=0, max_value=12, value=1, step=1, key='duration')

    # Calculate Time Out
    time_out = (datetime.combine(date_input, time_in) + timedelta(hours=duration)).time()
    st.write(f"Time Out: {time_out.strftime('%H:%M')}")

    full_name_input = st.text_input("Full Name:")
    phone_input = st.text_input("Phone Number:")
    email_input = st.text_input("Email:")
    note_input = st.text_area("Note:")

    if st.button("Register Client"):
        if full_name_input and phone_input and email_input:  # Ensure all required fields are filled
            try:
                # Format the data for Google Sheets as strings
                formatted_date = date_input.strftime("%d/%m/%Y")  # 'DD/MM/YYYY' format for the date
                formatted_time_in = time_in.strftime("%H:%M")     # 'HH:MM' format for time
                formatted_time_out = time_out.strftime("%H:%M")   # 'HH:MM' format for time

                sheet_data = [
                    formatted_date,
                    formatted_time_in,
                    formatted_time_out,
                    full_name_input, 
                    phone_input, 
                    email_input, 
                    note_input
                ]

                # Then you write sheet_data to the Google Sheet as before
                write_to_sheets(sheet_data)

                # User feedback
                st.success("Client registered successfully!")
            except Exception as e:
                st.error(f"Failed to register client: {e}")
        else:
            st.error("Please fill in all required fields.")