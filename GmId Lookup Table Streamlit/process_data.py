import numpy as np

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
# Function to get parameter values, ensuring flexibility
def get_parameter_values(name, params):
    return params.get(name, np.array([]))

# Function to find the index of a value in an array
def find_index(value, array):
    index = np.where(np.isclose(array, value))[0]
    if index.size == 0:
        raise ValueError(f"Value {value} not found in array", array)
    return index[0]

# Function to get data from the 4D matrix given a set of values
def get_value(output, vsb, L, vds, vgs,data):
    vsb_index = find_index(vsb, vsb_values)
    L_index = find_index(L, L_values)
    vds_index = find_index(vds, vds_values)
    vgs_index = find_index(vgs, vgs_values)
    return data[output][vsb_index, L_index, vds_index, vgs_index]


# Dynamic get_value call
def dynamic_get_value(output, vsb, L, vds, vgs, x_axis_name, sweep_name, x, sweep_value,data):
    if x_axis_name == 'vsb':
        if sweep_name == 'L':
            return get_value(output, x, sweep_value, vds, vgs,data)
        elif sweep_name == 'vds':
            return get_value(output, x, L, sweep_value, vgs,data)
        elif sweep_name == 'vgs':
            return get_value(output, x, L, vds, sweep_value,data)
    elif x_axis_name == 'L':
        if sweep_name == 'vsb':
            return get_value(output, sweep_value, x, vds, vgs,data)
        elif sweep_name == 'vds':
            return get_value(output, vsb, x, sweep_value, vgs,data)
        elif sweep_name == 'vgs':
            return get_value(output, vsb, x, vds, sweep_value,data)
    elif x_axis_name == 'vds':
        if sweep_name == 'vsb':
            return get_value(output, sweep_value, L, x, vgs,data)
        elif sweep_name == 'L':
            return get_value(output, vsb, sweep_value, x, vgs,data)
        elif sweep_name == 'vgs':
            return get_value(output, vsb, L, x, sweep_value,data)
    elif x_axis_name == 'vgs':
        if sweep_name == 'vsb':
            return get_value(output, sweep_value, L, vds, x,data)
        elif sweep_name == 'L':
            return get_value(output, vsb, sweep_value, vds, x,data)
        elif sweep_name == 'vds':
            return get_value(output, vsb, L, sweep_value, x,data)
        
        
