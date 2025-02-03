import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import streamlit as st
import os

def process_data_page():
    # Section 1: Manage Saved Data
    st.title("Manage Saved Data")
    st.markdown("###### Implemented by Eva Deltor")

    # List all saved data files
    data_files = [f for f in os.listdir() if f.endswith('.csv')]
    selected_file = st.selectbox("Select Data File to Delete", data_files)

    if selected_file:
        if st.button("Delete Selected File"):
            os.remove(selected_file)
            st.success(f"File {selected_file} has been deleted. Refresh the website.")

    # Add a separator between sections
    st.markdown("---")

    # Section 2: Upload and Process Data
    st.title("Upload and Process Data")
    st.markdown("This page is used when we want to import data directly from Cadence, so it is not ready to be plotted, it needs to be processed first.")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(df.head())

        # Define parameter ranges
        st.markdown("#### Define Parameter Ranges")
        col1, col2, col3 = st.columns(3)
        with col1:
            vsb_min = st.number_input("vsb min:", 0.0)
            L_min = st.number_input("L min:", 0.22)
            vds_min = st.number_input("vds min:", 0.0)
            vgs_min = st.number_input("vgs min:", 0.0)
        with col2:
            vsb_max = st.number_input("vsb max:", 1.8)
            L_max = st.number_input("L max:", 3.0)
            vds_max = st.number_input("vds max:", 1.8)
            vgs_max = st.number_input("vgs max:", 1.8)
        with col3:
            vsb_step = st.number_input("vsb step:", 0.1)
            L_step = st.number_input("L step:", 0.25)
            vds_step = st.number_input("vds step:", 0.1)
            vgs_step = st.number_input("vgs step:", 0.1)

        vsb_values = np.round(np.arange(vsb_min, vsb_max, vsb_step), 2)
        L_values = np.round(np.arange(L_min, L_max, L_step), 2) * 1e-6
        vds_values = np.round(np.arange(vds_min, vds_max, vds_step), 2)
        vgs_values = np.round(np.arange(vgs_min, vgs_max, vgs_step), 2)

        # Add a text input field to set the name for saving the results
        st.markdown("#### Save Results")
        save_filename = st.text_input("Enter the filename to save the results", "results")

        if st.button("Process Data"):
            # Replace NaN values with 0
            df = df.fillna(0)

            # Outputs and results dictionary
            outputs = ['cgs', 'cgg', 'ft', 'gds', 'gm', 'gmoverid', 'region', 'vds', 'vth', 'i']
            results = {output: np.zeros((len(vsb_values), len(L_values), len(vds_values), len(vgs_values))) for output in outputs}

            # Strip parentheses and trailing spaces from column names
            df.columns = df.columns.str.replace(r'\s*\(.*\)\s*', '', regex=True).str.strip()

            total_iterations = len(vsb_values) * len(L_values) * len(vds_values) * len(vgs_values) * len(outputs) 

            # Create a Streamlit progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Process data with progress bar
            with tqdm(total=total_iterations, desc='Procesando', unit='iter') as pbar:
                for i, vsb in enumerate(vsb_values):
                    if vsb == 0.0:
                      vsb = 0
                    if vsb == 1.0:
                      vsb = 1
                    for j, L in enumerate(np.round(L_values, 8)):
                        for k, vds in enumerate(np.round(vds_values,2)):
                            if vds == 0.0:
                              vds = 0
                            if vds == 1.0:
                              vds = 1
                            for l, vgs in enumerate(np.round(vgs_values,2)):
                                if vgs == 0.0:
                                  vgs = 0
                                if vgs == 1.0:
                                  vgs = 1
                                for output in outputs:
                                    #print("OUTPUT",output)
                                    col_name = f'M0.m1:{output} L {L} vds {vds} vgs {vgs}'
                                    col_name_2 = f'/M0:1:{output} L {L} vds {vds} vgs {vgs}'
                                    #print("NAME: ",col_name)
            
                                    if col_name in df.columns:
                                        filtered_df = df[np.isclose(df['vsb'], vsb)]
                                        if not filtered_df.empty:
                                            try:
                                                value = filtered_df[col_name].values[0]
                                                if value == 0.0 and output!="ft" and output!="region" and not(vds == 0 or vgs == 0 ):
                                                  print("RESULT: ",value,col_name,"OUTPUT: ",output,"________________________________")
                                                results[output][i, j, k, l] = float(value) if not isinstance(value, (int, float)) else value
                                            except (ValueError, TypeError):
                                                results[output][i, j, k, l] = np.nan
                                        else:
                                            results[output][i, j, k, l] = np.nan
                                    elif col_name_2 in df.columns:
                                        filtered_df = df[np.isclose(df['vsb'], vsb)]
                                        if not filtered_df.empty:
                                            try:
                                                value = filtered_df[col_name_2].values[0]
                                                if value == 0.0 and output!="ft" and output!="region" and not(vds == 0 or vgs == 0 ):
                                                  print("RESULT: ",value, col_name_2,"OUTPUT: ",output,"________________________________")
                                                results[output][i, j, k, l] = float(value) if not isinstance(value, (int, float)) else value
                                            except (ValueError, TypeError):
                                                results[output][i, j, k, l] = np.nan
                                        else:
                                            results[output][i, j, k, l] = np.nan
            
                                    pbar.update(1)
                                                
                                    # Update the Streamlit progress bar and status text
                                    progress_bar.progress((pbar.n / total_iterations))
                                    status_text.text(f'Processing: {pbar.n / total_iterations:.2%} complete')
            
            # Save results with the specified filename
            np.savez(f'{save_filename}.npz', **results)
            st.success(f"Results saved in '{save_filename}.npz'")
