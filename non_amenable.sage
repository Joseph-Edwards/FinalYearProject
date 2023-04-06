def is_discrete(g, part):
    return all(len(p) == 1 for p in g.coarsest_equitable_refinement(part))


def find_graphs(low, high):
    found = []
    for i in range(low, high+1):
        part = [list(range(i))]
        for j, g in enumerate(graphs.nauty_geng(f"-c {i}")):
            if j%5000 == 0:
                print(f"{i} nodes: {j} tested")
                if found:
                    print([g.graph6_string() for g in found])
            if (not g.is_regular()) and (g.automorphism_group(return_group=False, order=True) == 1) and (not is_discrete(g, part)):
                found.append(g)
                print(g.graph6_string())
        if found:
            return [g.graph6_string() for g in found]

def find_planar_graphs(low, high):
    found = []
    for i in range(low, high+1):
        part = [list(range(1, i+1))]
        for j, g in enumerate(graphs.planar_graphs(i)):
            if j%5000 == 0:
                print(f"{i} nodes: {j} tested")
                if found:
                    print([g.graph6_string() for g in found])
            if (not g.is_regular()) and (g.automorphism_group(return_group=False, order=True) == 1) and (not is_discrete(g, part)):
                found.append(g)
                print(g.graph6_string())
        if found:
            return [g.graph6_string() for g in found]

print(find_graphs(1, 10))
print(find_planar_graphs(1, 12))

# ['I?qa`q[Ww', 'I?qa`wuq_', 'I?qabK{e_', 'I?qachqm?', 'ICOedOuRO']
# Max deg 3: 'K?HGiOPGc@OB'
# 10 Nodes: 'I?qa`q[Ww'