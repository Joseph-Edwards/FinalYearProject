def is_discrete(g, part):
    # Check if stable partition is discrete
    return all(len(p) == 1 for p in g.coarsest_equitable_refinement(part))


def find_graphs(low=1, high=None, gen_args="", planar=False, v=3):
    mod = [False, 50000, 5000, 1000, 100][v]
    find_smallest = False
    if not high:
        high = 0
        find_smallest = True

    i = low
    found = {}
    total_found = 0
    while find_smallest or i <= high:
        found_now = 0
        found_any = False
        found[i] = []

        # Nice output
        title = f" {i} nodes " if i > 0 else " 1 node "
        print(f"\n{title:=^100}")
        print(f"Found so far: {total_found}")

        # Create target graphs
        if not planar:
            part = [list(range(i))]
            all_graphs = graphs.nauty_geng(f"{i} -c {gen_args}")
            if mod:
                num_graphs = sum(1 for g in graphs.nauty_geng(f"{i} -c {gen_args}"))
        else:
            part = [list(range(1, i + 1))]
            all_graphs = graphs.planar_graphs(i)
            if mod:
                num_graphs = sum(1 for g in graphs.planar_graphs(i))
        
        if mod:
            print(f"{num_graphs} graphs with {i} nodes to test")

        for j, g in enumerate(all_graphs):
            # Count itteratrions, and show currently found graphs
            if mod and j % mod == 0 and j != 0:
                bar_length = int((j / num_graphs) * 60)
                bar = "=" * bar_length
                progress = f"({j}/{num_graphs})"
                if found_any:
                    progress = f"{progress} Found: {found_now}"
                else:
                    progress = f"{progress} None found"
                output = f"|{bar:<60}|{progress}"
                print(f"\r{output:<100}", end="", flush=True)

            # Test for non-regularity, asymmetry and non-discreteness
            # (which implies non-amenability)
            if (
                (not g.is_regular())
                and (g.automorphism_group(return_group=False, order=True) == 1)
                and (not is_discrete(g, part))
            ):
                found[i].append(g.graph6_string())
                found_any = True
                found_now += 1
                if not mod:
                    print(f"\rFound: {found_now}", end="", flush=True)

        total_found += found_now

        if mod:
            full_bar = "=" * 60
            progress = f"({num_graphs}/{num_graphs})"
            if found_any:
                progress = f"{progress} Found: {found_now}"
            else:
                progress = f"{progress} None found"
            print(f"\r|{full_bar}|{progress}\n", end="")
        else:
            print(f"Found: {found_now}")

        if not found_any:
            del found[i]
        if found_any and find_smallest:
            print("=" * 100 + "\n")
            return found

        i += 1

    print("=" * 100 + "\n")
    return found

# Find the smallest asymmetric, non-regular, non-amenable graphs with degree
# at most 3
find_graphs(gen_args="-D3")

# Returns:
# {12: ['K?AA@agLECJ?']}

# Find the smallest asymmetric, non-regular, non-amenable graphs
find_graphs(10, v=0)
# # Returns:
# {
#     10: [
#         "I?qa`q[Ww",
#         "I?qachqm?",
#         "I?qaeWyN_",
#         "I?qa`wuq_",
#         "I?qabK{e_",
#         "I?q`qx]ho",
#         "I?qbtrqn?",
#         "I?otQi]ZW",
#         "I?otQm]ZW",
#         "I?ot]ro|?",
#         "I?rfdpyn?",
#         "I?qvEfk\\O",
#         "I?qvEd]|?",
#         "I?qrdZq}?",
#         "I?qvfPyn?",
#         "I?qjbrQ|?",
#         "I?zTfZq\\_",
#         "ICOedOuRO",
#         "ICOedPNLo",
#         "ICQfCxwM_",
#         "ICQebXwf?",
#         "ICQbere}?",
#         "ICQbec{^?",
#         "ICQbdLw}?",
#         "ICQeQxw|?",
#         "ICQeMptz?",
#         "ICQeLpw[_",
#         "ICQfeo{^?",
#         "ICQUbRd}?",
#         "ICQTbTkx?",
#         "ICQRVbe}?",
#         "ICRbbzU^G",
#         "ICRcrrw\\_",
#         "ICRctVkN_",
#         "ICR`uiwy_",
#         "ICQvCxw]_",
#         "ICQuQpu}?",
#         "ICQuRp{{_",
#         "ICQuRpu}?",
#         "ICpddpU^?",
#         "ICpdbi{V_",
#         "ICpdbi]^?",
#         "ICpbdh]n?",
#         "ICpdRYxFw",
#         "ICpdlpyz?",
#         "ICrbbpufO",
#         "ICpvdt{~?",
#         "ICprn`|vO",
#         "ICrJbzw]g",
#         "ICZbvjsVo",
#         "ICZejrsNo",
#         "ICZfvp{v_",
#         "ICZVExym_",
#         "ICZTfQ{Xw",
#         "ICZTfRXhw",
#         "ICZTeqlww",
#         "ICZTepfy_",
#         "ICZVRrqfo",
#         "ICZLbb[Mw",
#         "ICZLb`yfW",
#         "ICZLbaxVg",
#         "ICZLfp{l_",
#         "ICZJfb[Mw",
#         "ICZJf`yfO",
#         "ICZJdpytO",
#         "ICZJd^s{_",
#         "ICXmdb[io",
#         "ICXmdbifW",
#         "ICXmfb[iw",
#         "ICXmfVs|_",
#         "ICXmdvwx_",
#         "ICdev`lz?",
#         "ICxvbvkvO",
#         "IEhfczsJo",
#         "IEjfbzm^_",
#         "IEhvFp]n_",
#         "IEhvExmn_",
#         "IEhuVpun_",
#         "IEhvTn{}O",
#         "IQjRfM}fo",
#     ]
# }


###############################################################################
# Other uses:
###############################################################################

# Find the smallest asymmetric, non-regular, non-amenable planar graphs
# find_graphs(planar=True)

# Find the smallest asymmetric, non-regular, non-amenable with at most 17 edges
# find_graphs(gen_args="0:17")
