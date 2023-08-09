import pandas as pd
import streamlit as st

def detect_delimiter(file, num_lines=5):
    """
    Detect the delimiter of a CSV file based on the frequency of potential delimiters in the first few lines.

    Args:
    - file: File-like object (e.g., result of open() or an uploaded file in Streamlit).
    - num_lines: Number of lines to consider for delimiter detection.

    Returns:
    - Detected delimiter as a string (e.g., ",", ";", "\t").
    """
    
    # Potential delimiters to consider
    delimiters = [',', '\t', ';', '|', ' ']
    
    # Read the first few lines of the file
    lines = [file.readline().decode('utf-8') for _ in range(num_lines)]
    file.seek(0)  # Reset file pointer to the beginning
    
    # Count occurrences of each potential delimiter
    delimiter_counts = {delimiter: sum(line.count(delimiter) for line in lines) for delimiter in delimiters}
    
    # Return the delimiter with the maximum count
    return max(delimiter_counts, key=delimiter_counts.get)



st.title("Combine CSV files into one Excel file")
st.write("#### Created by: [Nicolas Cantarovici](https://github.com/nicocanta20), [Florian Reyes](https://github.com/florianreyes), [Julian Fischman](https://github.com/JulianFischman)")
csv_files = st.file_uploader("Upload csv files", type=["csv"], accept_multiple_files=True)
button = st.button("Combine")
if button:
    if csv_files:
        excel_path = 'combined_data.xlsx'
        with pd.ExcelWriter(excel_path) as excel_writer:
            for i, file in enumerate(csv_files):
                # Detect the delimiter for the current file
                delimiter = detect_delimiter(file)
                
                # Use the detected delimiter to read the CSV file
                data_df = pd.read_csv(file, delimiter=delimiter,low_memory=False,error_bad_lines=False)
                
                data_df.to_excel(excel_writer, sheet_name=f'sheet_{i+1}', index=False)

        st.success("Successfully combined csv files into one Excel file!")
        # Reading the saved Excel file as bytes
        with open(excel_path, 'rb') as f:
            bytes_data = f.read()

        st.download_button(label="Download", data=bytes_data, file_name='combined_data.xlsx')
        
    else:
        st.error("Please upload csv files and click on the button to combine them into one Excel file!")
