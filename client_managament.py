#client_managament.py
import streamlit as st
from datetime import datetime, time, timedelta, date
import pandas as pd
import gspread
from google.oauth2 import service_account



#class SessionState:
    #def __init__(self, **kwargs):
        #for key, val in kwargs.items():
            #setattr(self, key, val)

#if "registered_clients" not in st.session_state:
    #st.session_state.registered_clients = []
 #   1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ
#registered_clients = []

SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']

# Function to get Google Sheets service
def get_sheets_service():
    service_account_info = st.secrets["google_oauth"]
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    return gspread.authorize(credentials)



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
        
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        records = worksheet.get_all_records()

        if records:
            df = pd.DataFrame(records)
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            
            # Add a date picker to select a day for filtering
            selected_date = st.date_input("Pasirinkite data")
            
            if selected_date:
                df = df[df['Date'].dt.date == selected_date]
                # Convert 'Time' column to datetime, then format to 'HH:MM'
                df['Time in'] = pd.to_datetime(df['Time in'], format='%H:%M').dt.time
                df['Time in'] = df['Time in'].apply(lambda x: x.strftime('%H:%M'))  # Format to 'HH:MM'
                df = df.sort_values(by='Time in')
            
            df['Weekday'] = df['Date'].dt.day_name().map(day_name_map)
            
            if 'Phone Number' in df.columns:
                df['Phone Number'] = df['Phone Number'].astype(str)

            # Format the 'Date' column to display without the time part
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

            df.set_index('Weekday', inplace=True)
            
            st.write("Pasirinktos dienos klientai:")
            st.dataframe(df)
        else:
            st.write("Šiuo metu registruotu klientu nėra.")
    except Exception as e:
        st.error(f"Failed to fetch data from Google Sheets: {str(e)}")



def register_client1():
    st.title("Registruoti naują klientą")

    # Input fields for registration
    date_input = st.date_input("Data:")

    # Implementing custom time picker in 10-minute increments
    business_hours_start = time(9, 0)  # Business hours start at 8:00 AM
    business_hours_end = time(21, 0)  # Business hours end at 6:00 PM
    time_options = [(datetime.combine(date.today(), business_hours_start) + timedelta(minutes=10 * i)).time() 
                    for i in range(int((datetime.combine(date.today(), business_hours_end) - 
                                        datetime.combine(date.today(), business_hours_start)).seconds / 600))]
    time_in = st.selectbox("Nuo:", time_options, format_func=lambda x: x.strftime("%H:%M"))


    full_name_input = st.text_input("Vardas Pavardė:")
    phone_input = st.text_input("Telefono numeris: Pavyzdys 61271128:")
    # Removed email input
    note_input = st.text_area("Pastabos:")

    if st.button("Registruoti klientą"):
        if full_name_input and phone_input:  # Ensure required fields are filled
            try:
                # Format the data for Google Sheets as strings
                formatted_date = date_input.strftime("%d/%m/%Y")  # 'DD/MM/YYYY' format for the date
                # The time picker value will be used here (next step)

                formatted_time_in = time_in.strftime("%H:%M")

                sheet_data = [
                    formatted_date,
                    formatted_time_in,
                    full_name_input, 
                    phone_input, 
                    # Removed email
                    note_input
                ]

                # Then you write sheet_data to the Google Sheet as before
                write_to_sheets(sheet_data)  # Your function to write data to Google Sheets

                st.success("Client registered successfully!")
                st.rerun()  # Refresh the page to show updated data
            except Exception as e:
                st.error(f"Failed to register client: {e}")
        else:
            st.error("Please fill in all required fields.")





def write_to_sheets(data, value_input_option='USER_ENTERED'):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet_name = 'Sheet1'
    try:
        worksheet = service.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        # Append the new data row
        worksheet.append_row(data, value_input_option=value_input_option)
    except Exception as e:
        st.error(f"Error writing to Google Sheets: {str(e)}")



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


        





def edit_appointment_details(client_name):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet = service.open_by_key(spreadsheet_id).worksheet('Sheet1')

    # Search for the client by name
    client_name = st.text_input("Enter client's name:")
    client_row = None
    for row in worksheet.get_all_values():
        if client_name in row:
            client_row = row
            break

    if client_row is not None:
        client_date = client_row[0]
        client_time = client_row[1]
        client_full_name = client_row[2]
        client_phone = client_row[3]
        client_note = client_row[4]

        # Update the client details
        updated_date = st.date_input("New Date:", value=pd.to_datetime(client_date))
        updated_time = st.time_input("New Time In:", value=pd.to_datetime(client_time).time())
        updated_full_name = st.text_input("New Full Name:", value=client_full_name)
        updated_phone = st.text_input("New Phone Number:", value=client_phone)
        updated_note = st.text_area("New Note:", value=client_note)

        if st.button("Update Client Details"):
            # Format the updated details for Google Sheets
            formatted_updated_date = updated_date.strftime("%d/%m/%Y")
            formatted_updated_time = updated_time.strftime("%H:%M")

            # Write the updated details to the worksheet
            worksheet.update_cell(client_row[0], 0, formatted_updated_date)
            worksheet.update_cell(client_row[1], 1, formatted_updated_time)
            worksheet.update_cell(client_row[2], 2, updated_full_name)
            worksheet.update_cell(client_row[3], 3, updated_phone)
            worksheet.update_cell(client_row[4], 4, updated_note)

            st.success("Client details updated successfully!")
            st.rerun()
    else:
        st.error(f"Client not found: {client_name}")


