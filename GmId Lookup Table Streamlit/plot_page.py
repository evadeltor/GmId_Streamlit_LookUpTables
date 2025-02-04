import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd  # Import pandas for data handling

from process_data import dynamic_get_value, get_parameter_values

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

# Define a function for the plotting page
def plot_page(data):
    st.markdown("# GmId Methodology", unsafe_allow_html=True)
    st.markdown("##### Implemented by Eva Deltor", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)

    # Create two columns with wider column width for the graph
    col1, col2 = st.columns([3, 4])

    with col1:
        # Variables to Select
        st.markdown("<u><strong>Variables to Select</strong></u>", unsafe_allow_html=True)
        vsb = st.selectbox("Select vsb", vsb_values)
        L = st.selectbox("Select L", L_values)
        vds = st.selectbox("Select vds", vds_values)
        vgs = st.selectbox("Select vgs", vgs_values)

        # Graph Properties
        st.markdown("<u><strong>Graph Properties</strong></u>", unsafe_allow_html=True)
        x_axis_name = st.selectbox("Select x_axis", ['vsb', 'L', 'vds', 'vgs'])
        sweep_name = st.selectbox("Select sweep", ['vsb', 'L', 'vds', 'vgs'])
        output = st.selectbox("Select output", ['cgs', 'cgg', 'ft', 'gds', 'gm', 'gmoverid', 'region', 'vds', 'vgs', 'vth', 'i'])

        selected_sweep_values = st.multiselect(
            f"Select {sweep_name} values",
            get_parameter_values(sweep_name, params),
            default=get_parameter_values(sweep_name, params)
        )

        x_axis_values = get_parameter_values(x_axis_name, params)

        # Adding sliders for x-axis range
        x_min, x_max = st.slider(
            "X-axis range",
            float(x_axis_values.min()),
            float(x_axis_values.max()),
            (float(x_axis_values.min()), float(x_axis_values.max()))
        )

        # Options for log scale at the bottom
        x_log_scale = st.checkbox("Log scale X axis")
        y_log_scale = st.checkbox("Log scale Y axis")

    with col2:
        # Filtering x_axis_values based on x_min and x_max
        filtered_x_axis_values = [x for x in x_axis_values if x_min <= x <= x_max]

        # Prepare data for plotting and saving
        graph_data = []
        fig, ax = plt.subplots()

        for sweep_value in selected_sweep_values:
            x_plot = []
            y_plot = []

            for x in filtered_x_axis_values:
                # Update parameters based on x_axis_name
                current_params = {
                    'vsb': vsb,
                    'L': L,
                    'vds': vds,
                    'vgs': vgs
                }
                current_params[x_axis_name] = x
                current_params[sweep_name] = sweep_value

                # Get the output value
                y = dynamic_get_value(
                    output,
                    current_params['vsb'],
                    current_params['L'],
                    current_params['vds'],
                    current_params['vgs'],
                    x_axis_name,
                    sweep_name,
                    x,
                    sweep_value,
                    data
                )
                if y is not None:
                    x_plot.append(x)
                    y_plot.append(y)

            if x_plot and y_plot:
                # Plot the data
                ax.plot(x_plot, y_plot, label=f'{sweep_name}={sweep_value}')

                # Store data for saving
                for xi, yi in zip(x_plot, y_plot):
                    graph_data.append({
                        x_axis_name: xi,
                        output: yi,
                        sweep_name: sweep_value
                    })

        ax.set_xlabel(x_axis_name)
        ax.set_ylabel(output)
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ax.grid(True)

        if x_log_scale:
            ax.set_xscale('log')
        if y_log_scale:
            ax.set_yscale('log')

        st.pyplot(fig)

    # Outside the columns
    # Add a 'Save Graph Data' button and file name input
    st.markdown("---")
    st.markdown("### Save Graph Data")

    # Input for file name
    file_name = st.text_input('Enter file name for graph data', value='graph_data.csv')

    # When 'Save Graph Data' button is clicked
    if st.button('Save Graph Data'):
        if graph_data:
            # Convert graph data to a DataFrame
            graph_df = pd.DataFrame(graph_data)
            # Save the DataFrame to CSV
            graph_df.to_csv(file_name, index=False)
            st.success(f"Graph data saved to {file_name}")
        else:
            st.warning("No graph data to save.")
