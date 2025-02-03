import streamlit as st
import os

'''
Page to manage the databases of saved graphs. It allows to delete them.
'''
def manage_data_page():
    st.title("Manage Saved Data")
    st.markdown("###### Implemented by Eva Deltor")

    # List all saved data files
    data_files = [f for f in os.listdir() if f.endswith('.csv')]
    selected_file = st.selectbox("Select Data File to Delete", data_files)

    if selected_file:
        if st.button("Delete Selected File"):
            os.remove(selected_file)
            st.success(f"File {selected_file} has been deleted. Refresh the website.")
            