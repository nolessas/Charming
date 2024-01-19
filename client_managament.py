#client_managament.py
import streamlit as st
from datetime import datetime, time, timedelta, date
import pandas as pd
import gspread
from google.oauth2 import service_account
from gspread.exceptions import CellNotFound


#class SessionState:
    #def __init__(self, **kwargs):
        #for key, val in kwargs.items():
            #setattr(self, key, val)

#if "registered_clients" not in st.session_state:
    #st.session_state.registered_clients = []
 #   1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ
#registered_clients = []

SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_service():
    service_account_info = st.secrets["google_oauth"]
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES_SHEETS)
    service = gspread.authorize(credentials)
    return service



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

            df['Weekday'] = df['Date'].dt.day_name().map(day_name_map)
            
            if 'Phone Number' in df.columns:
                df['Phone Number'] = df['Phone Number'].astype(str)

            # Format the 'Date' column to display without the time part
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

            df.set_index('Weekday', inplace=True)

            st.write("Pasirinktos dienos klientai:")
            st.dataframe(df)
        else:
            st.write("Šiuo metu registruotu kleintu nėra.")
    except Exception as e:
        st.error(f"Failed to fetch data from Google Sheets: {str(e)}")




def register_client1():
    st.title("Registruoti naują klientą")

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
                write_to_sheets(sheet_data)  # Your function to write data to Google Sheets

                st.success("Client registered successfully!")
                st.experimental_rerun()  # Refresh the page to show updated data
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
        st.experimental_rerun()  # Rerun the app to refresh the data display
    except Exception as e:
        st.error(f"Failed to delete client: {str(e)}")


# ... existing imports and functions ...
        
def add_client_note(client_id, note):
    """
    Adds or updates a note for a given client.
    :param client_id: The unique identifier for the client.
    :param note: The note to be added.
    """
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    notes_worksheet_name = 'Client Notes'  # Assume there is a sheet for notes
    
    try:
        # Open the notes worksheet
        notes_worksheet = service.open_by_key(spreadsheet_id).worksheet(notes_worksheet_name)
        
        # Fetch all the notes records
        notes_records = notes_worksheet.get_all_records()
        
        # Convert the records to a DataFrame for easier searching
        notes_df = pd.DataFrame(notes_records)
        
        # Check if the client already has a note
        if client_id in notes_df['Client ID'].values:
            # Update the existing note
            row_index = notes_df.index[notes_df['Client ID'] == client_id].tolist()[0] + 2  # Offset for header and 1-indexing
            notes_worksheet.update_cell(row_index, notes_df.columns.get_loc('Note') + 1, note)  # Update the note
        else:
            # Add a new note entry
            new_row = [client_id, note]
            notes_worksheet.append_row(new_row)  # Append a new row with the client ID and note
        
        st.success("Note added/updated successfully for client ID: " + str(client_id))
    except Exception as e:
        st.error(f"Failed to add/update note for client: {str(e)}")



def display_client_note(client_name):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet = service.open_by_key(spreadsheet_id).worksheet('Sheet1')

    try:
        cell = worksheet.find(client_name)
        current_note = worksheet.cell(cell.row, 7).value  # Assuming note is in the 7th column
        st.text_area("Current Note for " + client_name, value=current_note, height=150, key='current_note')
        return cell.row  # Return the row number for the update function
    except gspread.exceptions.CellNotFound:
        st.error("Client not found.")
        return None

def update_client_note(row_number, client_name, new_note):
    if row_number is None:
        return  # Do nothing if row number is not provided

    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet = service.open_by_key(spreadsheet_id).worksheet('Sheet1')

    worksheet.update_cell(row_number, 7, new_note)  # Update the note in the 7th column
    st.success("Note updated successfully for " + client_name)

def get_and_update_client_notes(client_name):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet = service.open_by_key(spreadsheet_id).worksheet('Sheet1')

    try:
        cell = worksheet.find(client_name)
    except gspread.exceptions.CellNotFound:
        st.error("Client not found.")
        return

    if not cell:
        st.error("Error finding the client.")
        return

    # Fetch the current note from the 7th column in the client's row
    current_note = worksheet.cell(cell.row, 7).value
    new_note = st.text_area("Note for " + client_name, value=current_note, height=150)

    if st.button('Update Note'):
        worksheet.update_cell(cell.row, 7, new_note)
        st.success("Note updated successfully for " + client_name)




def edit_appointment_details(client_name):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet = service.open_by_key(spreadsheet_id).worksheet('Sheet1')

    try:
        # Find the client in the worksheet
        cell = worksheet.find(client_name)
        # Get the current details from the worksheet
        current_date = worksheet.cell(cell.row, 1).value
        current_time_in = worksheet.cell(cell.row, 2).value
        current_time_out = worksheet.cell(cell.row, 3).value
        
        # Display the current details
        st.write("Current appointment details for " + client_name + ":")
        st.write("Date: " + current_date)
        st.write("Time In: " + current_time_in)
        st.write("Time Out: " + current_time_out)
        
        # Provide inputs for new details
        new_date = st.date_input("New Date:", value=pd.to_datetime(current_date, dayfirst=True))
        new_time_in = st.time_input("New Time In:", value=pd.to_datetime(current_time_in).time())
        new_duration = st.slider("New Duration (hours):", min_value=0, max_value=12, value=(pd.to_datetime(current_time_out).time() - pd.to_datetime(current_time_in).time()).seconds // 3600, step=1)
        
        # Calculate the new Time Out based on the new Time In and Duration
        new_time_out = (datetime.combine(new_date, new_time_in) + timedelta(hours=new_duration)).time()
        
        if st.button("Update Appointment Details"):
            # Format the new details for Google Sheets
            formatted_new_date = new_date.strftime("%d/%m/%Y")  # 'DD/MM/YYYY' format for the date
            formatted_new_time_in = new_time_in.strftime("%H:%M")  # 'HH:MM' format for time
            formatted_new_time_out = new_time_out.strftime("%H:%M")  # 'HH:MM' format for time
            
            # Update the details in the worksheet
            worksheet.update_cell(cell.row, 1, formatted_new_date)
            worksheet.update_cell(cell.row, 2, formatted_new_time_in)
            worksheet.update_cell(cell.row, 3, formatted_new_time_out)
            
            st.success("Appointment details updated successfully for " + client_name)
    except gspread.exceptions.APIError as e:  # Use a more generic exception
        if "Cell not found" in str(e):
            st.error("Client not found.")
            return
        else:
            raise
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
