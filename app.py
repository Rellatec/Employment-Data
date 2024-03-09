import pandas as pd
import streamlit as st
from tabulate import tabulate

# Function to summarize data from a given DataFrame
def summarize_data(data):
    # Convert employment figures to numeric, handling any non-numeric gracefully
    data['2022 Employment'] = pd.to_numeric(data['2022 Employment'], errors='coerce')
    data['Projected 2032 Employment'] = pd.to_numeric(data['Projected 2032 Employment'], errors='coerce')
    # Calculate employment change and percent change for the period 2022-2032
    data['Employment Change, 2022-2032'] = data['Projected 2032 Employment'] - data['2022 Employment']
    data['Percent Change, 2022-2032'] = (data['Employment Change, 2022-2032'] / data['2022 Employment']) * 100 if data['2022 Employment'].sum() > 0 else 0
    # Summarize and return key figures
    summary = {
        '2022 Employment': data['2022 Employment'].sum(),
        'Projected 2032 Employment': data['Projected 2032 Employment'].sum(),
        'Employment Change, 2022-2032': data['Employment Change, 2022-2032'].sum(),
        'Percent Change, 2022-2032': data['Percent Change, 2022-2032'].mean()
    }
    return summary

# Streamlit app
def main():
    st.title('Summary of Employment Data')
    
    # Allow user to upload CSV files
    uploaded_files = st.file_uploader("Upload CSV files", type='csv', accept_multiple_files=True)
    
    # Initialize list for summary data including headers
    summary_rows = [['File Name', '2022 Employment', 'Projected 2032 Employment', 'Employment Change 2022-2032', 'Percent Change 2022-2032']]
    
    # Display summary table for each uploaded file
    for uploaded_file in uploaded_files:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(uploaded_file)
        
        # Summarize the data
        summary = summarize_data(data)
        
        # Add summary data to list
        summary_rows.append([
            uploaded_file.name,
            str(summary['2022 Employment']),  # Convert numeric values to strings
            str(summary['Projected 2032 Employment']),
            str(summary['Employment Change, 2022-2032']),
            f"{summary['Percent Change, 2022-2032']:.2f}%"
        ])
    
    # Display the summary table
    st.table(summary_rows)

if __name__ == "__main__":
    main()
