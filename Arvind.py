# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 19:23:23 2022

@author: josep
"""

import networkx as nx
from itertools import groupby, product
from collections import deque

X1 = nx.Graph()
X1.add_nodes_from(range(1, 21))
X1.add_edges_from([(6, 7),
    (7, 8),
    (8, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (12, 13),
    (13, 14),
    (14, 15),
    (15, 9),
    (15, 13),
    (16, 13),
    (17, 18),
    (18, 19),
    (19, 20)
    ])

X2 = nx.Graph()
X2.add_nodes_from(range(1, 7))
X2.add_edges_from([
    (1, 2),
    (1, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 7)
    ])

def colour_refinement(G):
    V = list(G.nodes)
    N = {v: G[v] for v in V}
    C = {v:1 for v in V}    # Initial colouring
    P = {1: V}              # P associates with each colour the vertices of this colour
    c_min, c_max = 1, 1     # Colour names are always between c_min and c_max
    Q = deque([1])          # Contains colours used for refinement
    while Q:
        q = Q.popleft()

        # Number of neighbours of v of colour q
        verts_with_col_q = set(P[q])
        D = {v: len(verts_with_col_q & set(N[v])) for v in V}

        # Ordered partition of vertices v sorted lexographically by (C[v], D[v])
        list.sort(V, key = lambda v: (C[v], D[v]))
        cols_and_parts = [(k[0], list(g))  for k, g in groupby(V, lambda v: (C[v], D[v]))]
        cols_of_parts, B = list(zip(*cols_and_parts))

        for i in range(c_min, c_max + 1):
            # Colour classes of B i will be split into classes B_k1, ..., B_k2
            k1, k2 = first_last(cols_of_parts, i)

            # Add all colours, except the one with the largest class, to Q
            i_star = max(range(k1, k2 + 1), key = lambda i: len(B[i]))
            for i in range(k1, k2 + 1):
                if i != i_star:
                    Q.append(c_max + i + 1)

        c_min, c_max = c_max + 1, c_max + len(B)    # New colour range
        for b in range(c_min, c_max + 1):
            B_current =  B[b - c_min]
            P[b] = B_current                        # New colouring
            for v in B_current:
                C[v] = b
    return C, P

def first_last(array,key):
    return (array.index(key), len(array) - array[::-1].index(key) - 1)

#%%

def augmented_cell_graph(G):
    # Get stable colouring
    C, P = colour_refinement(G)
    stable_colouring = {v: P[v] for v in set(C.values())}

    # Vertices of C* are colour classes of (G, C)
    V = stable_colouring.keys()

    # Find the adjacency list and d_ijs
    adj_list = {}   # vertex: [neighbours]
    d_ij = {}       # (i, j): d_ij
    for u in V:
        edges, ds = find_edges(stable_colouring[u], G, C)
        adj_list[u] = edges
        for colour, d in ds.items():
            d_ij[(u, colour)] = d

    # Convert vertex list and adjacency list to nx Graph
    aug_G = nx.Graph()
    aug_G.add_nodes_from(V)
    for u, nbs in adj_list.items():
        aug_G.add_edges_from(product([u], nbs))
    return aug_G, d_ij, stable_colouring


def find_edges(X, G, C):
    # Get representative
    u = X[0]

    # Get the colour class of each neighbour
    adjacent_colours = [C[v] for v in G[u]]

    # Count the number of occurences of each neighbour
    d_ij = {C[u]:0}
    d_ij |= {i:adjacent_colours.count(i) for i in adjacent_colours}

    adj_list = d_ij.keys() - {C[u]}
    return adj_list, d_ij

def is_amenable(G):
    aug_G, d_ij, C = augmented_cell_graph(G)
    V = list(aug_G.nodes)
    cell_size = {v: len(C[v]) for v in V}

    for uv in d_ij.keys():
        u, v = uv
        d = d_ij[(u, v)]
        if u == v:
            u_size = cell_size[u]
            # Empty, Kn, mK2, complement of mK2, C5
            if not (d in (0, u_size - 1, 1, u_size - 2) or (d == 2 and u_size == 5)):
                return False
        else:
            u_size = cell_size[u]
            v_size = cell_size[v]
            # Empty, Kmn, sK1t, sKt1, complement of sK1t, complement of sKt1
            if not (d in (0, v_size, 1, v_size/u_size, v_size - 1, v_size - v_size/u_size)):
                return False
    return True


is_amenable(X1)
#c, p = colour_refinement(X1)
#nx.draw_circular(X1, node_color = list(c.values()), labels = c)
aug_G, ds, C = augmented_cell_graph(X1)
nx.draw(aug_G, with_labels = True)

