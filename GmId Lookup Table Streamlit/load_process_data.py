import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import streamlit as st

def process_data_page():
    st.title("Upload and Process Data")
    st.markdown("###### Implemented by Eva Deltor")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(df.head())

        # Define parameter ranges
        st.markdown("#### Define Parameter Ranges")
        vsb_values = np.round(np.arange(st.number_input("vsb min:", 0.0), st.number_input("vsb max:", 1.8), st.number_input("vsb step:", 0.1)), 2)
        L_values = np.round(np.arange(st.number_input("L min:", 0.22), st.number_input("L max:", 3.0), st.number_input("L step:", 0.25), dtype=float), 2) * 1e-6
        vds_values = np.round(np.arange(st.number_input("vds min:", 0.0), st.number_input("vds max:", 1.8), st.number_input("vds step:", 0.1)), 2)
        vgs_values = np.round(np.arange(st.number_input("vgs min:", 0.0), st.number_input("vgs max:", 1.8), st.number_input("vgs step:", 0.1)), 2)

        if st.button("Process Data"):
            # Replace NaN values with 0
            df = df.fillna(0)

            # Outputs and results dictionary
            outputs = ['cgs', 'cgg', 'ft', 'gds', 'gm', 'gmoverid', 'region', 'vds', 'vth', 'i']
            results = {output: np.zeros((len(vsb_values), len(L_values), len(vds_values), len(vgs_values))) for output in outputs}

            # Strip parentheses and trailing spaces from column names
            df.columns = df.columns.str.replace(r'\s*\(.*\)\s*', '', regex=True).str.strip()

            total_iterations = len(vsb_values) * len(L_values) * len(vds_values) * len(vgs_values) * len(outputs) 

            # Process data with progress bar
            with tqdm(total=total_iterations, desc='Procesando', unit='iter') as pbar:
                for i, vsb in enumerate(vsb_values):
                    for j, L in enumerate(np.round(L_values, 8)):
                        for k, vds in enumerate(np.round(vds_values, 2)):
                            for l, vgs in enumerate(np.round(vgs_values, 2)):
                                for output in outputs:
                                    col_name = f'M0.m1:{output} L {L} vds {vds} vgs {vgs}'
                                    col_name_2 = f'/M0:1:{output} L {L} vds {vds} vgs {vgs}'
                                    if col_name in df.columns:
                                        filtered_df = df[np.isclose(df['vsb'], vsb)]
                                        if not filtered_df.empty:
                                            value = filtered_df[col_name].values[0]
                                            results[output][i, j, k, l] = float(value) if not isinstance(value, (int, float)) else value
                                    elif col_name_2 in df.columns:
                                        filtered_df = df[np.isclose(df['vsb'], vsb)]
                                        if not filtered_df.empty:
                                            value = filtered_df[col_name_2].values[0]
                                            results[output][i, j, k, l] = float(value) if not isinstance(value, (int, float)) else value
                                    pbar.update(1)
            
            # Save results
            np.savez('results.npz', **results)
            st.success("Results saved in 'results.npz'")

