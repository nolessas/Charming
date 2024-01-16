#client_managament.py
import streamlit as st
from datetime import datetime, time, timedelta, date
import pandas as pd
from google_sheets import write_to_sheets, get_sheets_service, delete_client


#class SessionState:
    #def __init__(self, **kwargs):
        #for key, val in kwargs.items():
            #setattr(self, key, val)

#if "registered_clients" not in st.session_state:
    #st.session_state.registered_clients = []

#registered_clients = []


def show_registered_clients():
    st.title("Registered Clients")

    service = get_sheets_service()

    try:
        worksheet = service.open_by_key('1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ').worksheet('Sheet1')
        records = worksheet.get_all_records()

        if records:
            df = pd.DataFrame(records)
            df['Date'] = pd.to_datetime(df['Date'])
            df['Weekday'] = df['Date'].dt.day_name()  # Add day of the week

            # Add radio buttons for filtering by time range (Day, Week, Month, Year)
            time_range = st.radio("", ["Day", "Week", "Month", "Year"])

            # Calculate the start date based on the selected time range
            if time_range == "Day":
                start_date = pd.Timestamp.now()- pd.DateOffset(days=1)
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
                sheet_data = [
                    datetime.combine(date_input, datetime.min.time()),  # Python datetime object for the date
                    datetime.combine(datetime.today(), time_in),       # Python datetime object for 'Time In'
                    datetime.combine(datetime.today(), time_out),      # Python datetime object for 'Time Out'
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