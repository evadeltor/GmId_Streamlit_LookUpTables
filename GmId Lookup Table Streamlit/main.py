import os
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from plot_page import plot_page
from value_page import value_page
from manage_data_page import manage_data_page
from process_data_page import process_data_page
from create_own_graph_page import create_own_graph_page
from lookup_ratios import cross_lookup_page
from ratio_page import ratio_page
from plot_saved_graphs_page import plot_saved_graphs_page

st.set_page_config(layout="wide")

# Sidebar for navigation and data file selection
st.sidebar.title("Mode of analysis 📊")

# List all available .npz files in the current folder
npz_files = [f for f in os.listdir() if f.endswith('.npz')]

# Selection to choose the data file
data_file_option = st.sidebar.selectbox("Select Data File", npz_files)

# Load arrays from the selected .npz file
data = np.load(data_file_option)

# Add the new page to the sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Plot", "Get Value","Overlap graphs", "Ratio", "Create Your Own Graph", "Cross-Lookup",  "Load RAW Data"])

# Add a text input for the data name
data_name = st.sidebar.text_input("Enter Data Name", value="File1")

# Initialize session state for saved data names
if 'saved_data_names' not in st.session_state:
    st.session_state.saved_data_names = []
    st.session_state.saved_graphs = []

# Add a button to save the data
if st.sidebar.button("Save Data"):
    st.session_state.saved_data_names.append(f"{data_name}.csv")
    # Save the data to .csv file with the name
    pd.DataFrame(data).to_csv(f"{data_name}.csv", index=False)
    
    # Save graph data
    graph_data = st.session_state.get('graph_data', {})
    if graph_data:
        st.session_state.saved_graphs.append(graph_data)
        pd.DataFrame(graph_data).to_csv(f"{data_name}_graph.csv", index=False)

# Dropdown to show the names of the saved data
saved_data_option = st.sidebar.selectbox("Saved Data Names", st.session_state.saved_data_names)

# Show the selected page
if page == "Plot":
    plot_page(data)
elif page == "Get Value":
    value_page(data)
elif page == "Manage Data":
    manage_data_page()
elif page == "Load RAW Data":
    process_data_page()
elif page == "Create Your Own Graph":
    create_own_graph_page(saved_data_option)  # pass saved_data_option
elif page == "Cross-Lookup":
    cross_lookup_page(data)
elif page == "Ratio":
    ratio_page(data_name, data)
elif page == "Overlap graphs":
    plot_saved_graphs_page()
