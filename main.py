# Importing necessary libraries
import pandas as pd
import streamlit as st
import csv

# Function to detect the delimiter used in a CSV file
def enhanced_detect_delimiter(file, num_lines=5):
    # List of potential delimiters
    delimiters = [',', '\t', ';', '|', ' ']
    
    # Reading the first few lines of the file to assist in delimiter detection
    lines = [file.readline().decode('utf-8') for _ in range(num_lines)]
    file.seek(0)  # Resetting file pointer to the beginning
    
    # Counting the occurrences of each potential delimiter
    delimiter_counts = {}
    for delimiter in delimiters:
        count = sum(len(list(csv.reader([line], delimiter=delimiter))) for line in lines)
        delimiter_counts[delimiter] = count
    
    # If the detected delimiter doesn't appear as often as the number of lines, default to comma
    if max(delimiter_counts.values()) < num_lines:
        return ','
    
    # Return the delimiter with the maximum occurrences
    return max(delimiter_counts, key=delimiter_counts.get)

# Function to combine multiple CSV files into a single Excel file
def streamlit_csv_combiner(csv_files, excel_path):
    success_files = []  # List to keep track of successfully processed files
    failed_files = []   # List to keep track of files that failed to process

    # Creating or overwriting an Excel file to save the combined data
    with pd.ExcelWriter(excel_path) as excel_writer:
        for i, file in enumerate(csv_files):
            # Detecting the delimiter for the current file
            delimiter = enhanced_detect_delimiter(file)
            
            try:
                # Reading the CSV file into a pandas DataFrame
                data_df = pd.read_csv(file, delimiter=delimiter, low_memory=False, quotechar='"')
                
                # If the DataFrame is empty, add the file to the failed_files list and continue
                if data_df.empty:
                    failed_files.append(f"sheet_{i+1}")
                    continue

                # Saving the DataFrame as a sheet in the Excel file
                data_df.to_excel(excel_writer, sheet_name=f'sheet_{i+1}', index=False)
                success_files.append(f"sheet_{i+1}")

            # Handling potential errors due to empty data
            except pd.errors.EmptyDataError:
                failed_files.append(f"sheet_{i+1}")
                continue

    return success_files, failed_files

# Streamlit UI

# Path to save the combined Excel file
excel_path = 'combined.xlsx'

# Streamlit title and description
st.title("Combine CSV files into one Excel file")
st.write("#### Created by: [Nicolas Cantarovici](https://github.com/nicocanta20), [Florian Reyes](https://github.com/florianreyes), [Julian Fischman](https://github.com/JulianFischman)")

# Streamlit file uploader to select multiple CSV files
csv_files = st.file_uploader("Upload csv files", type=["csv"], accept_multiple_files=True)

# Streamlit button to trigger the combining process
button = st.button("Combine")
if button:
    if csv_files:
        # Combining the uploaded CSV files
        success_files, failed_files = streamlit_csv_combiner(csv_files, excel_path)

        # Displaying success message and download link if files were successfully processed
        if success_files:
            st.success(f"Successfully combined csv files into one Excel file! Processed sheets: {', '.join(success_files)}")
            with open(excel_path, 'rb') as f:
                bytes_data = f.read()
            st.download_button(label="Download", data=bytes_data, file_name='combined_data.xlsx')
        
        # Displaying an error message for files that failed to process
        if failed_files:
            st.error(f"Failed to process the following sheets: {', '.join(failed_files)}")

    # Displaying an error message if no files were uploaded
    else:
        st.error("Please upload csv files and click on the button to combine them into one Excel file!")
