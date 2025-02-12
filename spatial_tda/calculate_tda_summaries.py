# import libraries
import gudhi
import numpy as np


def compute_persistence(simplices, filtered_df, variable_name):
    """
    Compute persistence diagrams for the simplicial complex.
    """

    st = gudhi.SimplexTree()
    st.set_dimension(2)

    for simplex in simplices:
        if len(simplex) == 1:
            st.insert([simplex[0]], filtration=0.0)
    
    for simplex in simplices:
        if len(simplex) == 2:
            last_simplex = simplex[-1]
            filtration_value = filtered_df.loc[filtered_df['sortedID'] == last_simplex, variable_name].values[0]
            st.insert(simplex, filtration=filtration_value)

    for simplex in simplices:
        if len(simplex) == 3:
            last_simplex = simplex[-1]
            filtration_value = filtered_df.loc[filtered_df['sortedID'] == last_simplex, variable_name].values[0]
            st.insert(simplex, filtration=filtration_value)

    st.compute_persistence()
    persistence = st.persistence()

    # intervals_dim1 = st.persistence_intervals_in_dimension(1)
    intervals_dim0 = st.persistence_intervals_in_dimension(0)

    # get the max value of the filtered_df to replace inf
    max_value = filtered_df[variable_name].max()
    # print(f'max value: {max_value}')

    # replace inf with a large number   #this needs to be fixed : previously used 16
    intervals_dim0[:, 1][np.isinf(intervals_dim0[:, 1])] = max_value

    # remove if inf is there
    # intervals_dim0 = intervals_dim0[np.isfinite(intervals_dim0).all(1)]

    # calculate topological summaries for dimension 1
    H0_data_points = len(intervals_dim0)

    TL = 0
    for interval in intervals_dim0:
            TL += interval[1] - interval[0]

    TML = 0
    for interval in intervals_dim0:
        TML += (interval[1] + interval[0])/2
        # print(f'interval: {interval[1]} - {interval[0]} get added to TML: {TML}')

    if len(intervals_dim0) == 0:
        AL = 0
        AML = 0
    else: 
        AL = TL/len(intervals_dim0)
        AML = TML/len(intervals_dim0)

    return H0_data_points, TL, AL, TML, AML, intervals_dim0

