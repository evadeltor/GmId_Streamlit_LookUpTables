import streamlit as st
import numpy as np
import process_data
from process_data import get_value

# Define your possible parameters and their values
vsb_values = np.round(np.arange(0, 1.8, 0.1), 2)
L_values = np.round(np.arange(0.22, 3, 0.25), 2) * 1e-6
vds_values = np.round(np.arange(0, 1.8, 0.1), 2)
vgs_values = np.round(np.arange(0, 1.8, 0.1), 2)

params = {
    'vsb': vsb_values,
    'L': L_values,
    'vds': vds_values,
    'vgs': vgs_values
}

# Define a function for the value page
def value_page(data):
    st.title("GmId Methodology")
    st.markdown("### Implemented by Eva Deltor")

    # Create two columns with wider column width for the graph
    col1, col2 = st.columns([1, 2])

    with col1:
        # Variables to Select
        st.markdown("<u><strong>Variables to Select</strong></u>", unsafe_allow_html=True)
        vsb = st.selectbox("Select vsb", vsb_values)
        L = st.selectbox("Select L", L_values)
        vds = st.selectbox("Select vds", vds_values)
        vgs = st.selectbox("Select vgs", vgs_values)

        

    with col2:
        # Graph Properties
        st.markdown("<u><strong>Graph Properties</strong></u>", unsafe_allow_html=True)
        output = st.selectbox("Select output", ['cgs', 'cgg', 'ft', 'gds', 'gm', 'gmoverid', 'region', 'vds', 'vgs', 'vth', 'i'])
        
        # Get the value and display it with custom HTML and CSS
        value = get_value(output, vsb, L, vds, vgs, data)
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 100%; background-color: #f0f0f0; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
                <h1 style="font-size: 3rem; color: #333;">{output} = {value}</h1>
            </div>
        """, unsafe_allow_html=True)
        