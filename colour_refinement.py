# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 19:23:23 2022

@author: Joseph Edwards
"""

from collections import deque
from itertools import groupby, product
import networkx as nx

# =============================================================================
# Colour Refinement
# =============================================================================


def first_last(array, key):
    # Find first and last occurrence of an element in a sorted list
    return (array.index(key), len(array) - array[::-1].index(key) - 1)


def colour_refinement(G):
    V = list(G.nodes)
    N = {v: G[v] for v in V}  # Neighbours of each vertex
    C = {v: 1 for v in V}     # Initial colouring
    P = {1: V}                # P associates each colour with its colour class
    c_min, c_max = 1, 1       # Colour names are always between c_min and c_max
    Q = deque([1])            # Contains colours used for refinement
    while Q:
        q = Q.popleft()

        # Number of neighbours of v of colour q
        verts_with_col_q = set(P[q])
        D = {v: len(verts_with_col_q & set(N[v])) for v in V}

        # Ordered partition of vertices sorted by (C[v], D[v])
        list.sort(V, key=lambda v: (C[v], D[v]))
        cols_and_parts = [
            (k[0], list(g)) for k, g in groupby(V, lambda v: (C[v], D[v]))
        ]
        cols_of_parts, B = list(zip(*cols_and_parts))

        for i in range(c_min, c_max + 1):
            # Colour classes of B i will be split into classes B_k1, ..., B_k2
            k1, k2 = first_last(cols_of_parts, i)

            # Add all colours, except the one with the largest class, to Q
            i_star = max(range(k1, k2 + 1), key=lambda i: len(B[i]))
            for i in range(k1, k2 + 1):
                if i != i_star:
                    Q.append(c_max + i + 1)

        c_min, c_max = c_max + 1, c_max + len(B)    # New colour range
        for b in range(c_min, c_max + 1):
            B_current = B[b - c_min]
            P[b] = B_current                        # New colouring
            for v in B_current:
                C[v] = b
    return C, {v: P[v] for v in set(C.values())}

# =============================================================================
# Create Augmented Cell Graph
# =============================================================================


def find_edges(col_class, G, C):
    # Get representative
    u = col_class[0]

    # Get the colour of each neighbour
    adjacent_colours = [C[v] for v in G[u]]

    unique_colours = set(adjacent_colours)

    # Count the number of occurrences of each neighbour
    d_ij = {C[u]: 0}
    d_ij |= {i: adjacent_colours.count(i) for i in unique_colours}

    adj_list = unique_colours - {C[u]}  # Can there be loops?
    return adj_list, d_ij


def augmented_cell_graph(G):
    # Get stable colouring
    C, P = colour_refinement(G)

    # Vertices of C* are colours used in (G, C)
    aug_V = P.keys()

    # Make the adjacency list of  aug_G and find d_ijs
    adj_list = {}   # vertex: [neighbours]
    d_ij = {}       # (i, j): d_ij
    for aug_u in aug_V:
        edges, ds = find_edges(P[aug_u], G, C)
        adj_list[aug_u] = edges
        for aug_v, d in ds.items():
            d_ij[(aug_u, aug_v)] = d

    # Convert vertex list and adjacency list to nx Graph
    aug_G = nx.Graph()
    aug_G.add_nodes_from(aug_V)
    for aug_u, nbs in adj_list.items():
        aug_G.add_edges_from(product([aug_u], nbs))
    return aug_G, d_ij, P

# =============================================================================
# Find Valid Anisotropic Components
# =============================================================================


def is_anisotropic(u, v, d, cell_size):
    return d[(u, v)] not in (0, cell_size[v])


def is_heterogeneous(u, d, cell_size):
    return d[(u, u)] not in (0, cell_size[u] - 1)


def anisotropic_components(aug_G, d, cell_size):
    aug_V = set(aug_G.nodes)
    components = []

    # Iterate until we have visited all nodes in aug_G
    while aug_V:
        # Use breadth first search to build components
        root = aug_V.pop()
        visit = deque([root])
        seen = {root}
        component = nx.Graph()

        min_card = cell_size[root]
        min_card_vertex = root

        found_het = False

        while visit:
            aug_u = visit.popleft()
            card = cell_size[aug_u]
            # Check H
            if is_heterogeneous(aug_u, d, cell_size):
                if (not found_het) and card <= min_card:
                    found_het = True
                    het_card = card
                else:
                    raise AssertionError
            elif found_het and card < het_card:
                raise AssertionError

            # Maintain record of minimum cardinality vertex
            if card < min_card:
                min_card = card
                min_card_vertex = aug_u

            component.add_node(aug_u)

            # Search Neighbours and add edge to component if anisotropic
            for aug_v in aug_G[aug_u]:
                if is_anisotropic(aug_u, aug_v, d, cell_size):
                    component.add_edge(aug_u, aug_v)
                    if aug_v not in seen:
                        visit.append(aug_v)
                        seen |= {aug_v}
                        aug_V.remove(aug_v)

        # Check component is Tree (Part of G)
        assert nx.is_tree(component)
        components.append((component, min_card_vertex))
    return components


# =============================================================================
# Check Monotonicity
# =============================================================================


def satisfies_monotonicity(component, root, cell_size):
    for aug_u, aug_v in bfs(component, root):
        if cell_size[aug_u] > cell_size[aug_v]:
            return False
    return True


# =============================================================================
# Amenability Testing
# =============================================================================


def bfs(G, root):
    # Breadth First Search over a tree
    visit = deque([root])
    visited = set()
    while visit:
        u = visit.popleft()
        visited.add(u)
        for v in G[u]:
            if v not in visited:
                visit.append(v)
                yield (u, v)


def is_amenable(G):
    aug_G, d_ij, col_classes = augmented_cell_graph(G)
    aug_V = list(aug_G.nodes)
    cell_size = {aug_v: len(col_classes[aug_v]) for aug_v in aug_V}

    for aug_u, aug_v in d_ij.keys():
        d = d_ij[(aug_u, aug_v)]
        if aug_u == aug_v:
            # Check A
            aug_u_size = cell_size[aug_u]
            if not (
                d in (
                    0,                           # Empty
                    aug_u_size - 1,              # Kn
                    1,                           # mK2
                    aug_u_size - 2               # Complement of mK2
                )
                or (d == 2 and aug_u_size == 5)  # C5
            ):
                print("Fails A")
                return False
        else:
            # Check B
            aug_u_size = cell_size[aug_u]
            aug_v_size = cell_size[aug_v]
            if not (d in (
                0,                                  # Empty
                aug_v_size,                         # Kmn
                1,                                  # sK1t
                aug_v_size/aug_u_size,              # sKt1
                aug_v_size - 1,                     # Complement of sK1t
                aug_v_size - aug_v_size/aug_u_size  # Complement of sKt1
            )):
                print("Fails B")
                return False

    # Get anisotropic components and Check H
    try:
        comps = anisotropic_components(aug_G, d_ij, cell_size)
    except AssertionError:
        print("Fails H")
        return False

    # Test monotonicity (Part of G)
    for comp, root in comps:
        if not satisfies_monotonicity(comp, root, cell_size):
            print("Fails G")
            return False
    return True

# =============================================================================
# Jellyfishification
# =============================================================================


def jellyfishify(G, k):
    J_k_G = nx.Graph()
    J_k_G.add_edges_from(G.edges)
    n = G.order()
    for v in G:
        for i in range(1, k + 1):
            J_k_G.add_edge(v + (i - 1) * n, v + i * n)
    return J_k_G
