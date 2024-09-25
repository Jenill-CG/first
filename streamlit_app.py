import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define a function to connect to Google Sheets
def connect_to_gsheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    
    sheet = client.open(sheet_name).sheet1  # Opens the first sheet
    return sheet

# Define a function to update the Google Sheet
def update_gsheet(data, sheet):
    sheet.clear()  # Optional: Clears the sheet before writing
    sheet.update([data.columns.values.tolist()] + data.values.tolist())

# Streamlit app
st.title('Google Sheets Data Uploader')

# Sample DataFrame input by the user
st.write("Enter the data you want to upload to Google Sheets")

# Example: A small table created by the user
data = {
    'Name': ['John', 'Jane', 'Doe'],
    'Age': [28, 24, 32],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

df = pd.DataFrame(data)
st.write(df)

sheet_name = st.text_input("Enter Google Sheet name", "My Google Sheet")

# Button to update data to Google Sheets
if st.button('Upload to Google Sheet'):
    try:
        sheet = connect_to_gsheet(sheet_name)
        update_gsheet(df, sheet)
        st.success("Data successfully uploaded to Google Sheets!")
    except Exception as e:
        st.error(f"Error: {e}")

