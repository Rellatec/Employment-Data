import pandas as pd
import streamlit as st

def summarize_data(data):
    # Convert employment figures to numeric, handling non-numeric values gracefully
    data['2022 Employment'] = pd.to_numeric(data['2022 Employment'], errors='coerce')
    data['Projected 2032 Employment'] = pd.to_numeric(data['Projected 2032 Employment'], errors='coerce')
    
    # Calculate employment change and percent change for 2022-2032, ensuring no division by zero
    data['Employment Change, 2022-2032'] = data['Projected 2032 Employment'] - data['2022 Employment']
    data['Percent Change, 2022-2032'] = data.apply(
        lambda row: (row['Employment Change, 2022-2032'] / row['2022 Employment'] * 100) if row['2022 Employment'] > 0 else 0, axis=1)
    
    # Summarize and return key figures
    summary = {
        '2022 Employment': data['2022 Employment'].sum(),
        'Projected 2032 Employment': data['Projected 2032 Employment'].sum(),
        'Employment Change, 2022-2032': data['Employment Change, 2022-2032'].sum(),
        'Percent Change, 2022-2032': data['Percent Change, 2022-2032'].mean()
    }
    return summary

def main():
    st.title('Summary of Employment Data')
    
    uploaded_files = st.file_uploader("Upload CSV files", type='csv', accept_multiple_files=True)
    
    if uploaded_files is not None:
        summary_data = {
            'File Name': [],
            '2022 Employment': [],
            'Projected 2032 Employment': [],
            'Employment Change 2022-2032': [],
            'Percent Change 2022-2032': []
        }

        for uploaded_file in uploaded_files:
            data = pd.read_csv(uploaded_file)
            summary = summarize_data(data)
            
            summary_data['File Name'].append(uploaded_file.name)
            summary_data['2022 Employment'].append(summary['2022 Employment'])
            summary_data['Projected 2032 Employment'].append(summary['Projected 2032 Employment'])
            summary_data['Employment Change 2022-2032'].append(summary['Employment Change, 2022-2032'])
            summary_data['Percent Change 2022-2032'].append(f"{summary['Percent Change, 2022-2032']:.2f}%")
        
        st.table(pd.DataFrame(summary_data))

if __name__ == "__main__":
    main()
