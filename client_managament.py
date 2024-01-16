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

def show_registered_clients():
    service = get_sheets_service()
    try:
        worksheet = service.open_by_key('1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ').worksheet('Sheet1')
        unique, headers = get_unique_headers(worksheet)
        if not unique:
            st.error(f"The header row in the worksheet is not unique: {', '.join(headers)}")
            return  # Stop execution if headers are not unique

        records = worksheet.get_all_records()
        if records:
            df = pd.DataFrame(records)
            df['Date'] = pd.to_datetime(df['Date'])
            df['Weekday'] = df['Date'].dt.day_name()  # Add day of the week

            # Add radio buttons for filtering by time range (Day, Week, Month, Year)
            time_range = st.radio("Filter by time range:", ["Day", "Week", "Month", "Year"])

            # Calculate the start date based on the selected time range
            start_date = {
                "Day": pd.Timestamp.now() - pd.DateOffset(days=1),
                "Week": pd.Timestamp.now() - pd.DateOffset(weeks=1),
                "Month": pd.Timestamp.now() - pd.DateOffset(months=1),
                "Year": pd.Timestamp.now() - pd.DateOffset(years=1)
            }.get(time_range, pd.Timestamp(1970, 1, 1))  # Default to a very old date

            # Filter the dataframe based on the selected time range
            filtered_df = df[df['Date'] >= start_date]

            # Sort the dataframe by Date column
            filtered_df = filtered_df.sort_values(by=["Date"])

            st.write("Client Information:")
            st.dataframe(filtered_df)  # Displaying the filtered dataframe directly

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