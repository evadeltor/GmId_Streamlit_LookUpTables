import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def create_own_graph_page(saved_data_option):
    st.title("Create Your Own Graph")
    st.markdown("###### Implemented by Eva Deltor")

    # Load the selected saved data
    saved_data = pd.read_csv(saved_data_option)

    # Convert saved_data to a suitable format for plotting
    saved_data_values = saved_data.values.flatten()

    # Create two columns with wider column width for the graph
    col1, col2 = st.columns([1, 2])

    with col1:
        # Select x value range
        st.markdown("<u><strong>Select X Value Range</strong></u>", unsafe_allow_html=True)
        x_min = st.number_input("X-axis Min", value=0.0)
        x_max = st.number_input("X-axis Max", value=10.0)
        num_points = st.number_input("Number of points", value=100, step=1)

        # Generate x values
        x_values = np.linspace(x_min, x_max, num_points)

        # Input equation
        st.markdown("<u><strong>Input Equation</strong></u>", unsafe_allow_html=True)
        equation = st.text_input("Enter equation in terms of x (e.g., 'np.sin(x)', 'x**2 + 2*x + 1')", value="np.sin(x)")

        # Evaluate the equation for each x value
        try:
            y_values = [eval(equation, {"np": np, "x": x}) for x in x_values]
        except Exception as e:
            st.error(f"Error in equation: {e}")
            return
        
        # Options for log scale at the bottom
        x_log_scale = st.checkbox("Log scale X axis")
        y_log_scale = st.checkbox("Log scale Y axis")

    with col2:
        # Plot the graph
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values, label=f"y = {equation}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ax.grid(True)
    
        if x_log_scale:
            ax.set_xscale('log')
        if y_log_scale:
            ax.set_yscale('log')

        st.pyplot(fig)

    # Plot the saved data
    if saved_data is not None:
        st.markdown("<u><strong>Saved Data Plot</strong></u>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.plot(saved_data_values, label=f"Saved Data: {saved_data_option}")
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ax.grid(True)
        st.pyplot(fig)
