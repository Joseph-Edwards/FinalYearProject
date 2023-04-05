import colour_refinement as CR
import networkx as nx

# =============================================================================
# Dissertation Examples
# =============================================================================
# Show the graph in example 2.1.6 is amenable
g_2_1_6 = nx.Graph()
g_2_1_6.add_nodes_from(range(10))
g_2_1_6.add_edges_from(
    [[0, 2], [2, 8], [4, 9], [5, 6], [5, 7], [5, 8], [6, 7], [8, 9]]
)
CR.is_amenable(g_2_1_6)  # True

# Calculate the stable partition of the graph in Example 3.2.2
g_3_2_2 = nx.Graph()
g_3_2_2.add_nodes_from(range(1, 15))
g_3_2_2.add_edges_from(
    [
        [3, 4],
        [3, 5],
        [3, 6],
        [4, 7],
        [4, 8],
        [4, 9],
        [5, 10],
        [5, 11],
        [5, 12],
        [6, 13],
        [6, 14],
        [7, 8],
        [7, 9],
        [8, 9],
        [10, 11],
        [10, 12],
        [11, 12],
        [13, 14],
    ]
)

C_3_2_2, P_3_2_2 = CR.colour_refinement(g_3_2_2)
P_3_2_2  # {32: [4, 5], 27: [1, 2], 28: [13, 14], 29: [7, 8, 9, 10, 11, 12], 30: [3], 31: [6]}

# Calculate the stable partition of J_10 in Section 3.3
J_10 = nx.Graph()
J_10.add_nodes_from(range(1, 11))
J_10.add_edges_from(
    [
        [1, 2],
        [1, 5],
        [1, 8],
        [1, 9],
        [1, 10],
        [2, 3],
        [2, 4],
        [2, 6],
        [2, 7],
        [3, 4],
        [3, 10],
        [4, 5],
        [5, 6],
        [6, 7],
        [6, 10],
        [7, 8],
        [8, 9],
        [9, 10],
    ]
)

C_J_10, P_J_10 = CR.colour_refinement(J_10)
P_J_10  # {16: [1, 2], 13: [4, 8], 14: [3, 5, 7, 9], 15: [6, 10]}
CR.is_amenable(J_10)  # Fails H; False

# Calculate the stable partition of J_12 in Section 3.3
J_12 = nx.Graph()
J_12.add_nodes_from(range(1, 13))
J_12.add_edges_from(
    [
        [1, 2],
        [1, 8],
        [2, 3],
        [2, 8],
        [3, 4],
        [3, 9],
        [4, 5],
        [4, 12],
        [5, 6],
        [5, 11],
        [6, 7],
        [7, 8],
        [7, 10],
        [9, 10],
        [10, 11],
        [11, 12],
    ]
)

C_J_12, P_J_12 = CR.colour_refinement(J_12)
P_J_12  # {4: [1, 6, 9, 12], 5: [2, 3, 4, 5, 7, 8, 10, 11]}
CR.is_amenable(J_12)  # Fails A; False
