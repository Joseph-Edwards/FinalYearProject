# Note that this needs the colour refinement code

def triv_aut_refineable(G):
    return is_single(colour_refinement(G)[0])

def bad_graphs(low, high):
    for i in range(low, high+1):
        print(i)
        G = (g for g in graphs.nauty_geng(f"{i} {i}:0 -c") if (not g.is_regular() and g.automorphism_group().cardinality() == 1 and not triv_aut_refineable(g.networkx_graph())))
        g = next(G, False)
        if (g):
            return g
    return []

# Max deg 3: 'K?HGiOPGc@OB'
# 10 Nodes: 'I?qa`q[Ww'