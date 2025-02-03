import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.interpolate import interpn, interp1d
from process_data import get_value, get_parameter_values


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

def find_closest_values(list1, list3):
    closest_values = []
    list1 = np.array(list1)  # Convert list1 to a numpy array for efficient computation
    
    for value in list3:
        # Find the index of the closest value in list1
        index = np.abs(list1 - value).argmin()
        closest_values.append(list1[index])
    
    return closest_values

# Define the cross_lookup function without interpolation
def cross_lookup(data, outvar, invar, xdesired, L=None, vgs=None, vds=None, vsb=None):
    # Evaluate the output variable (outvar)
    if '_' in outvar:
        underscore = outvar.find('_')
        numerator = outvar[:underscore]
        denominator = outvar[underscore + 1:]
        if numerator == "ID":
            numerator = "i"
        if denominator == "ID":
            denominator = "i"
        numerator_values = np.array([get_value(numerator.lower(), vsb, L, vds, x, data) for x in vgs])
        denominator_values = np.array([get_value(denominator.lower(), vsb, L, vds, x, data) for x in vgs])
        ydata = numerator_values / denominator_values
    else:
        ydata = np.array([get_value(outvar.lower(), vsb, L, vds, x, data) for x in vgs])

    # Evaluate the input variable (invar)
    if '_' in invar:
        underscore = invar.find('_')
        numerator = invar[:underscore]
        denominator = invar[underscore + 1:]
        if numerator == "ID":
            numerator = "i"
        if denominator == "ID":
            denominator = "i"
        numerator_values = np.array([get_value(numerator.lower(), vsb, L, vds, x, data) for x in vgs])
        denominator_values = np.array([get_value(denominator.lower(), vsb, L, vds, x, data) for x in vgs])
        xdata = numerator_values / denominator_values
    else:
        xdata = np.array([get_value(invar.lower(), vsb, L, vds, x, data) for x in vgs])

    # Print the actual range of xdata, rounded to two decimal places
    xdata_min = round(np.min(xdata), 2)
    xdata_max = round(np.max(xdata), 2)
    st.markdown(f"Actual range of xdata: [{xdata_min}, {xdata_max}]")

    closest_values = find_closest_values(xdata, xdesired)
    
    positions = []

    for y in closest_values:
        idx = np.where(xdata == y)[0]
        if idx.size > 0:
            positions.append(idx[0])
        else:
            positions.append(None)  # Add None if the value is not found in xdata
     
    corresponding_A_values = [ydata[pos] for pos in positions if pos is not None]
    

    # Plot corresponding_A_values vs closest_values
    fig, ax = plt.subplots()
    ax.plot(closest_values, corresponding_A_values, 'o-')
    ax.set_xlabel(invar)
    ax.set_ylabel(outvar)
    ax.set_title('Corresponding A Values vs Closest Values')
    ax.grid(True)

    st.pyplot(fig)

# Define the cross_lookup_page function
def cross_lookup_page(data):
    st.title("Cross-Lookup Page")
    st.markdown("###### Implemented by Eva Deltor")

    # Create two columns with wider column width for the graph
    col1, col2 = st.columns([1, 1])

    with col1:
        # Variables to Select
        st.markdown("<u><strong>Variables to Select</strong></u>", unsafe_allow_html=True)
        vsb = st.selectbox("Select vsb", vsb_values)
        L = st.selectbox("Select L", L_values)
        vds = st.selectbox("Select vds", vds_values)
        # We will not include vgs in the choice since we will sweep it around it.
        # vgs = st.selectbox("Select vgs", vgs_values)
    with col2:
        # Ratios and Desired Values
        st.markdown("<u><strong>Ratios and Desired Values</strong></u>", unsafe_allow_html=True)
        outvar = st.selectbox("Select output ratio", ['GM_CGG','ft'])  # Example ratios; adjust as needed
        invar = st.selectbox("Select input ratio", ['GM_ID', 'VDS_ID', 'VGS'])  # Example ratios; adjust as needed
        xdesired_min = st.number_input("Enter minimum xdesired value", value=1.0)
        xdesired_max = st.number_input("Enter maximum xdesired value", value=3.0)
        num_points = st.number_input("Enter number of points in range", value=10, min_value=1)

        xdesired = np.linspace(xdesired_min, xdesired_max, num_points)

        if st.button("Perform Cross-Lookup"):
            cross_lookup(data, outvar, invar, xdesired, L, vgs_values, vds, vsb)
