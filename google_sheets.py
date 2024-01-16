#google_sheets.py
import gspread
from google.oauth2 import service_account
import streamlit as st

SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_service():
    service_account_info = st.secrets["google_oauth"]
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES_SHEETS)
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

