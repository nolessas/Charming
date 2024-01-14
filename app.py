import streamlit as st
import pandas as pd




st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

# Three radio bars with their respective options
option1 = st.radio("Radio 1", ("Option A", "Option B", "Option C"), index=0)
option2 = st.radio("Radio 2", ("Option X", "Option Y", "Option Z"), index=1)
option3 = st.radio("Radio 3", ("Choice 1", "Choice 2", "Choice 3"), index=2)

st.write(f"Selected Option 1: {option1}")
st.write(f"Selected Option 2: {option2}")
st.write(f"Selected Option 3: {option3}")
# Streamlit app
def main():
    st.title("Client Management App")

    menu_option = st.sidebar.selectbox("Select an option", ["Register Client", "View Registered Clients", "To-Do List"])

    if menu_option == "Register Client":
        st.header("Register New Client")
        date = st.date_input("Date")
        time = st.time_input("Time")
        full_name = st.text_input("Full Name")
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email")
        notes = st.text_area("Notes")
        if st.button("Register Client"):
            register_client(date, time, full_name, phone_number, email, notes)

    elif menu_option == "View Registered Clients":
        st.header("Registered Clients")
        view_registered_clients()

    elif menu_option == "To-Do List":
        st.header("To-Do List")
        manage_todo_list()

def register_client(date, time, full_name, phone_number, email, notes):
    try:
        # Create or load a DataFrame to store client data
        if 'client_data' not in st.session_state:
            st.session_state.client_data = pd.DataFrame(columns=["Date", "Time", "Full Name", "Phone Number", "Email", "Notes"])

        # Convert date and time to datetime object
        appointment_time = pd.to_datetime(f"{date} {time}")

        # Create a new client record
        new_client = pd.Series({
            "Date": appointment_time.strftime("%Y-%m-%d"),
            "Time": appointment_time.strftime("%H:%M:%S"),
            "Full Name": full_name,
            "Phone Number": phone_number,
            "Email": email,
            "Notes": notes
        })

        # Append the new client to the DataFrame
        st.session_state.client_data = st.session_state.client_data.append(new_client, ignore_index=True)

        st.success("Client registered successfully!")
    except Exception as e:
        st.error(f"Error registering client: {str(e)}")

def view_registered_clients():
    if 'client_data' not in st.session_state:
        st.write("No registered clients found.")
    else:
        st.write(st.session_state.client_data)

def manage_todo_list():
    # Placeholder function for the to-do list
    st.write("To-Do List functionality will be added here.")

if __name__ == "__main__":
    main()
