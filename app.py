def get_credentials():
    try:
        service_account_info = st.secrets["google_oauth"]
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES_SHEETS
        )
        return credentials
    except Exception as e:
        st.error(f"Error getting credentials: {e}")
        raise e

def show_dashboard():
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose_main = st.radio("", ("option1", "option2", "option3", "option4"))

    if choose_main == "option2":
        st.title("Today's Events")

        # Google Calendar API

        # Fetch today's events
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=(datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        )

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
    st.sidebar.success("Client registered successfully!")

    try:
        service.events().insert(calendarId='primary', body=event).execute()
        st.sidebar.success("Client registered successfully and event created in Google Calendar!")
    except HttpError as e:
        st.sidebar.error(f"Error creating event: {str(e)}")

# The rest of your code here...

if __name__ == "__main__":
    main()
