
import os
import io
import base64
import pandas as pd
import zipfile
import streamlit as st

def main():
    st.title("Excel File Processor")

    uploaded_file = st.file_uploader("Upload an XLSX file that is less than 200MB in size", type=["xlsx"])
    
    if uploaded_file is not None:
        # Reading the uploaded Excel file
        data = pd.read_excel(uploaded_file)

        # Calculating unique counts and digit lengths
        unique_school_count = data['School_ID'].nunique()
        school_digit_count = len(str(unique_school_count))
        unique_district_count = data['District'].nunique()
        district_digit_count = len(str(unique_district_count))
        unique_block_count = data['Block'].nunique()
        block_digit_count = len(str(unique_block_count))
        student_digit_count = len(str(max(data['Total_Students'])))

        # Centered and colored message for file upload success
        st.markdown("<p style='text-align: center; color: green;'>File uploaded successfully!</p>", unsafe_allow_html=True)

        # Display options
        col099, col098 = st.columns([1, 1])
        with col099: 
            run_default = st.checkbox("IDs with Default Settings")
        with col098:
            customize_id = st.checkbox("IDs with Customized Settings")

        # Ensure only one checkbox is selected
        if run_default and customize_id:
            st.warning("Please select only one option.")
            return

        # Set checkboxes_checked to True if either checkbox is selected
        st.session_state['checkboxes_checked'] = run_default or customize_id

        # Default or customized settings
        if run_default:
            # Default parameters
            partner_id = 11
            col1, col2 = st.columns([1, 1])
            with col1:
                grade = st.number_input("➡️ Please provide Grade Value", min_value=1, value=1)
            with col2:
                st.write(" ")
            buffer_percent = 0.0
            district_digits = district_digit_count
            block_digits = block_digit_count
            school_digits = school_digit_count
            # Add further processing based on default settings

        elif customize_id:
            # Customized parameters
            # Add input fields for customized settings
            pass

        # Generate PDFs and ZIP files based on inputs
        st.write("Processing your input...")

        # Example: Generating a PDF link (dummy file for now)
        preview_pdf_path = "sample.pdf"  # This should be the actual generated PDF path
        st.markdown(f"<p style='text-align: center; color: green;'>Preview generated successfully!</p>", unsafe_allow_html=True)
        
        if preview_pdf_path:
            # Read and display PDF download link
            with open(preview_pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
                base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
                pdf_link = f'<a href="data:application/pdf;base64,{base64_pdf}" download="{os.path.basename(preview_pdf_path)}">Click here to download and view PDF</a>'
                st.markdown(pdf_link, unsafe_allow_html=True)

        # Create and download ZIP file
        zip_buffer = io.BytesIO()
        district_folders = {}  # Placeholder for actual folder structure
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for district_name, folder_path in district_folders.items():
                for foldername, _, filenames in os.walk(folder_path):
                    for filename in filenames:
                        filepath = os.path.join(foldername, filename)
                        arcname = os.path.relpath(filepath, folder_path)
                        zip_file.write(filepath, arcname)

        zip_buffer.seek(0)  # Reset buffer position

        # Provide download link for the ZIP file
        st.download_button(
            label="Click to Download Zip File",
            data=zip_buffer.getvalue(),
            file_name="attendance_Sheets.zip",
            mime="application/zip"
        )
        
        st.session_state['thank_you_displayed'] = True  # Set thank you message state

if __name__ == "__main__":
    main()
