import numpy as np


def lower_neighbors(adjacencies, vertex):
    return [v for v in adjacencies[vertex] if v < vertex]


def incremental_vr(V, adjacencies, maxDimension,county_list):
    Vnew = list(V)
    # print("county list len",len(county_list))
    # print("adjacencies len",len(adjacencies))
    # for vertex in np.arange(len(adjacencies)):
    for vertex in county_list:
        # print("vertex",vertex)
        # print("adjacencies",adjacencies[vertex])
        N = sorted(lower_neighbors(adjacencies, vertex))
        add_cofaces(adjacencies, maxDimension, [vertex], N, Vnew)
    return Vnew


def add_cofaces(adjacencies, maxDimension, face, N, V):
    if sorted(face) not in V:
        V.append(sorted(face))
    if len(face) >= maxDimension:
        return
    else:
        for vertex in N:
            coface = list(face)
            coface.append(vertex)
            M = list(set(N) & set(lower_neighbors(adjacencies, vertex)))
            add_cofaces(adjacencies, maxDimension, coface, M, V)