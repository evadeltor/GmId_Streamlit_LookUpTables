import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from process_data import get_parameter_values, dynamic_get_value

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

# Function to save data to a DataFrame
def save_data_to_df(data, title, x_axis_name, y_axis_name):
    df = pd.DataFrame(data)
    df.columns = [x_axis_name, y_axis_name]
    df.to_csv(f"{title}.csv", index=False)
    return 

def ratio_page(data_name, data):
    st.title("GmId Methodology")
    st.markdown("###### Implemented by Eva Deltor")

    # Create two columns with wider column width for the graph
    col1, col2 = st.columns([1, 1])

    with col1:
        # Variables to Select
        st.markdown("<u><strong>Variables to Select</strong></u>", unsafe_allow_html=True)
        vsb = st.selectbox("Select vsb", vsb_values)
        L = st.selectbox("Select L", L_values)
        vds = st.selectbox("Select vds", vds_values)
        vgs = st.selectbox("Select vgs", vgs_values)

        # Graph Properties
        st.markdown("<u><strong>Graph Properties</strong></u>", unsafe_allow_html=True)
        x_axis_option = st.selectbox("Select x_axis:", ["Existing Variable", "Scaled Variable"])
        if x_axis_option == "Existing Variable":
            x_axis_name = st.selectbox("Select x_axis parameter", ['vsb', 'L', 'vds', 'vgs', 'cgs', 'cgg', 'ft', 'gds', 'gm', 'gmoverid', 'region', 'vds', 'vgs', 'vth', 'i'])
            x_axis_values = get_parameter_values(x_axis_name, params)
        else:
            x_axis_name = st.selectbox("Select variable to scale for x-axis", ['vsb', 'L', 'vds', 'vgs', 'cgs', 'cgg', 'ft', 'gds', 'gm', 'gmoverid', 'region', 'vds', 'vgs', 'vth', 'i'])
            scale_factor = st.number_input("Enter scale factor for x-axis variable:", min_value=1e-9, value=1.0, step=1e-9, format="%.1e")
            x_axis_values = [value * scale_factor for value in get_parameter_values(x_axis_name, params)]

        sweep_name = st.selectbox("Select sweep", ['vsb', 'L', 'vds', 'vgs'])
        output1 = st.selectbox("Select output1", ['cgs', 'cgg', 'ft', 'gds', 'gm', 'gmoverid', 'region', 'vds', 'vgs', 'vth', 'i'])
        ratio_option = st.selectbox("Divide output1 by:", ["Another Output", "Scaled Variable", "Value"])
        if ratio_option == "Another Output":
            output2 = st.selectbox("Select output2", ['cgs', 'cgg', 'ft', 'gds', 'gm', 'gmoverid', 'region', 'vds', 'vgs', 'vth', 'i'])
        elif ratio_option == "Scaled Variable":
            scale_variable = st.selectbox("Select variable to scale", ['cgs', 'cgg', 'ft', 'gds', 'gm', 'gmoverid', 'region', 'vds', 'vgs', 'vth', 'i'])
            scale_factor_output = st.number_input("Enter scale factor for variable:", min_value=1e-9, value=1.0, step=1e-9, format="%.1e")
        else:
            custom_value = st.number_input("Enter custom value for output2:", min_value=1e-9, value=1.0, step=1e-9, format="%.1e")

        selected_sweep_values = st.multiselect(f"Select {sweep_name} values", get_parameter_values(sweep_name, params), default=get_parameter_values(sweep_name, params))

        # Adding sliders for x-axis range, only if using an existing parameter
        if x_axis_option == "Existing Variable":
            x_min = st.slider("X-axis Min", float(x_axis_values.min()), float(x_axis_values.max()), float(x_axis_values.min()))
            x_max = st.slider("X-axis Max", float(x_axis_values.min()), float(x_axis_values.max()), float(x_axis_values.max()))
            filtered_x_axis_values = [x for x in x_axis_values if x_min <= x <= x_max]
        else:
            filtered_x_axis_values = x_axis_values

    with col2:
        # Plotting
        fig, ax = plt.subplots()
        data_to_save = []
        for sweep_value in selected_sweep_values:
            if ratio_option == "Another Output":
                ratio_values = []
                for x in filtered_x_axis_values:
                    value1 = dynamic_get_value(output1, vsb, L, vds, vgs, x_axis_name, sweep_name, x, sweep_value, data)
                    value2 = dynamic_get_value(output2, vsb, L, vds, vgs, x_axis_name, sweep_name, x, sweep_value, data)
                    if value1 is not None and value2 is not None:
                        ratio_values.append(value1 / value2)
                    else:
                        ratio_values.append(None)
            elif ratio_option == "Scaled Variable":
                ratio_values = []
                for x in filtered_x_axis_values:
                    value1 = dynamic_get_value(output1, vsb, L, vds, vgs, x_axis_name, sweep_name, x, sweep_value, data)
                    value2 = dynamic_get_value(scale_variable, vsb, L, vds, vgs, x_axis_name, sweep_name, x, sweep_value, data)
                    if value1 is not None and value2 is not None:
                        ratio_values.append(value1 / (value2 * scale_factor_output))
                    else:
                        ratio_values.append(None)
            else:
                ratio_values = []
                for x in filtered_x_axis_values:
                    value1 = dynamic_get_value(output1, vsb, L, vds, vgs, x_axis_name, sweep_name, x, sweep_value, data)
                    if value1 is not None:
                        ratio_values.append(value1 / custom_value)
                    else:
                        ratio_values.append(None)

            if all(value is not None for value in ratio_values):
                ax.plot(filtered_x_axis_values, ratio_values, label=f'{sweep_name}={sweep_value}')
                data_to_save.extend(zip(filtered_x_axis_values, ratio_values))

        ax.set_xlabel(x_axis_name)
        ax.set_ylabel(f'{output1}/{output2}' if ratio_option == "Another Output" else f'{output1}/({scale_variable}*{scale_factor_output})' if ratio_option == "Scaled Variable" else f'{output1}/{custom_value}')
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ax.grid(True)

        # Save the data if the button is clicked
        if st.session_state.save_data:
            save_data_to_df(data_to_save, data_name, x_axis_name, f'{output1}/{output2}' if ratio_option == "Another Output" else f'{output1}/({scale_variable}*{scale_factor_output})' if ratio_option == "Scaled Variable" else f'{output1}/{custom_value}')
            st.sidebar.success(f"Data saved as {data_name}.csv")

        st.pyplot(fig)
