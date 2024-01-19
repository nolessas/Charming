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
            
            # Filter the DataFrame by the selected date and sort by time
            if selected_date:
                df = df[df['Date'].dt.date == selected_date]
                # Assuming 'Time' column exists and is in format 'HH:MM'
                df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time
                df = df.sort_values(by='Time')
            
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
    date_input = st.date_input("Data:")
    time_in = st.slider("Nuo:", value=time(8, 0), format="HH:mm", key='time_in')
    duration = st.slider("Vizito trukmė:", min_value=0, max_value=12, value=1, step=1, key='duration')

    # Calculate Time Out
    time_out = (datetime.combine(date_input, time_in) + timedelta(hours=duration)).time()
    st.write(f"Vizito pabaiga: {time_out.strftime('%H:%M')}")

    full_name_input = st.text_input("Vardas Pavardė:")
    phone_input = st.text_input("Telefono numeris: Pavizdys 61271128:")
    email_input = st.text_input("Emailas:")
    note_input = st.text_area("Pastabos:")

    if st.button("Registruoti kleintą"):
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
        # Find all cells with the client name
        cells = worksheet.findall(client_name)
        if not cells:
            st.error("Klientas nerastas.")
            return None
        
        # Display current notes for all clients with the name
        for cell in cells:
            current_note = worksheet.cell(cell.row, 7).value  # Assuming note is in the 7th column
            st.text_area(f"Dabartinis aprašymas {client_name} (Eilutė {cell.row})", value=current_note, height=150, key=f'current_note_{cell.row}')

        # Return the row numbers for the update function
        return [cell.row for cell in cells]
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def update_client_note(row_number, client_name, new_note):
    if row_number is None:
        return  # Do nothing if row number is not provided

    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet = service.open_by_key(spreadsheet_id).worksheet('Sheet1')

    worksheet.update_cell(row_number, 7, new_note)  # Update the note in the 7th column
    st.success("Pastaba atnaujinta! " + client_name)

def get_and_update_client_notes(client_name):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet = service.open_by_key(spreadsheet_id).worksheet('Sheet1')

    try:
        cell = worksheet.find(client_name)
    except gspread.exceptions.CellNotFound:
        st.error("Kleintas nerastas.")
        return

    if not cell:
        st.error("Klaida ieškant kliento.")
        return

    # Fetch the current note from the 7th column in the client's row
    current_note = worksheet.cell(cell.row, 7).value
    new_note = st.text_area("Note for " + client_name, value=current_note, height=150)

    if st.button('Atnaujinti'):
        worksheet.update_cell(cell.row, 7, new_note)
        st.success("Sekmingai atnaujinta " + client_name)





def edit_appointment_details(client_name):
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    worksheet = service.open_by_key(spreadsheet_id).worksheet('Sheet1')

    try:
        # Find all cells with the client name
        cells = worksheet.findall(client_name)
        if not cells:
            st.error("Klientas nerastas.")
            return None
        
        # Display current details for all clients with the name and allow selection
        appointment_options = []
        for cell in cells:
            current_date = worksheet.cell(cell.row, 1).value
            current_time_in = worksheet.cell(cell.row, 2).value
            current_time_out = worksheet.cell(cell.row, 3).value
            appointment_details = f"Eilutė {cell.row}: {current_date} nuo {current_time_in} iki {current_time_out}"
            appointment_options.append(appointment_details)
            st.write(appointment_details)

        # Allow user to select which appointment to edit
        selected_appointment = st.selectbox("Pasirinkite vizito eilutę redagavimui:", appointment_options)
        selected_row_number = int(selected_appointment.split(":")[0].split()[1])
        
        # Provide inputs for new details
        current_date = worksheet.cell(selected_row_number, 1).value
        new_date = st.date_input("New Date:", value=pd.to_datetime(current_date, dayfirst=True))
        current_time_in = worksheet.cell(selected_row_number, 2).value
        new_time_in = st.time_input("New Time In:", value=pd.to_datetime(current_time_in, format='%H:%M').time())
        current_time_out = worksheet.cell(selected_row_number, 3).value
        current_duration_hours = int((pd.to_datetime(current_time_out, format='%H:%M') - pd.to_datetime(current_time_in, format='%H:%M')).seconds / 3600)
        new_duration = st.slider("New Duration (hours):", min_value=0, max_value=12, value=current_duration_hours, step=1)
        
        # Calculate the new Time Out based on the new Time In and Duration
        new_time_out = (datetime.combine(new_date, new_time_in) + timedelta(hours=new_duration)).time()
        
        if st.button("Update Appointment Details"):
            # Format the new details for Google Sheets
            formatted_new_date = new_date.strftime("%d/%m/%Y")  # 'DD/MM/YYYY' format for the date
            formatted_new_time_in = new_time_in.strftime("%H:%M")  # 'HH:MM' format for time
            formatted_new_time_out = new_time_out.strftime("%H:%M")  # 'HH:MM' format for time
            
            # Update the details in the worksheet
            worksheet.update_cell(selected_row_number, 1, formatted_new_date)
            worksheet.update_cell(selected_row_number, 2, formatted_new_time_in)
            worksheet.update_cell(selected_row_number, 3, formatted_new_time_out)
            
            st.success(f"Appointment details updated successfully for {client_name} (Eilutė {selected_row_number})")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


def archive_old_clients():
    service = get_sheets_service()
    spreadsheet_id = '1HR8NzxkcKKVaWCPTowXdYtDN5dVqkbBeXFsHW4nmWCQ'
    today = datetime.today().date()

    # Open the current and archive worksheets
    current_worksheet = service.open_by_key(spreadsheet_id).worksheet('Sheet1')
    archive_worksheet = service.open_by_key(spreadsheet_id).worksheet('Sheet3')

    # Get all records from the current worksheet
    records = current_worksheet.get_all_records()
    df = pd.DataFrame(records)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')

    # Filter out old clients
    old_clients_df = df[df['Date'].dt.date < today]

    # Adjust for header row and 1-based indexing
    rows_to_archive = [row_index + 2 for row_index in old_clients_df.index.tolist()]

    if rows_to_archive:
        # Reverse the rows to archive to avoid index shifting
        rows_to_archive.reverse()
        for row_number in rows_to_archive:
            # Get the client data from the row
            client_data = current_worksheet.row_values(row_number)
            # Append the client data to the archive worksheet
            archive_worksheet.append_row(client_data)
            # Delete the client row from the current worksheet
            current_worksheet.delete_rows(row_number)


