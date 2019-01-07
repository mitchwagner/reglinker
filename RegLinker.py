'''
Implements the RegLinker algorithm for finding the shortest
regular-language-constrained path through every edge in a directed, weighted,
edge-labeled graph.
'''

import networkx as nx

SUPER_SOURCE = "SUPER_SOURCE" 
SUPER_TARGET = "SUPER_TARGET"

def __remove_product_edges_with_nonmatching_labels(P, label="l"):
    '''
    Given a product graph T, remove those product edges created from
    edges that had different values for the indicated labeling attribute.
    '''

    edges = list(P.edges(data=True))

    # Do the edges that combined to form the product edge share the
    # same label?
    for edge in edges:
        labels = edge[2][label]
        
        if labels[0] != labels[1]:
            P.remove_edge(edge[0], edge[1])


def __product(X, Y):
    '''
    Given two iterables X and Y, return a generator of that yields the
    Cartesian product
    '''
    return ((x, y) for x in X for y in Y)


def label_constrained_tensor_product(G, H, label="l"):
    '''
    Given: two directed, edge-labeled graphs:
        - G = (V_G, E_G, l_G) 
        - H = (V_H, E_H, l_H)
         
    Define the label-constrained tensor product T of G and H as follows: 

    V_T: V_G X V_H

    E_T: ((u, x), (v, y)) exists iff: 
        - (u, v) is an edge in E_G
        - (x, y) is an edge in E_H
        - l_G(u, v) == l_H(v, y)
    '''

    P = nx.tensor_product(G, H)
    __remove_product_edges_with_nonmatching_labels(P, label=label)

    return P


def __weight_product_graph(G, P, weight="w"):
    for edge in P.edges():
        G_tail = edge[0][0]
        G_head = edge[1][0]
        P[edge[0]][edge[1]][weight] = G[G_tail][G_head][weight]


def __add_super_source(G, sources, ss=SUPER_SOURCE):
    G.add_node(ss)

    for source in sources:
        G.add_edge(ss, source)
    

def __add_super_target(G, targets, st="SUPER_TARGET"):
    G.add_node(st)

    for target in targets:
        G.add_edge(target, st)


def __path_to_edges(path):
    return [(path[x], path[x + 1]) for x in range(0, len(path) - 1)]


def __get_path_weight(G, path, weight="w"):

    if weight == None:
        return len(path)

    else:
        edges = __path_to_edges(path)
        return sum([G[tail][head][weight] for tail, head in edges])


def __path_to_labeled_edges(G, path, label="l"):
    edges = __path_to_edges(path)
    return [(tail, head, G[tail][head][label]) for tail, head in edges]
        

def QuickLinker(G, ss=SUPER_SOURCE, st=SUPER_TARGET, weight="w"):
    '''
    Find the shortest path through every edge.
    1) Find shortest path from super source to every node 
    2) Find shortest path from every node to super target 
    3) For the edge (u, v), return SS-u + (u, v) + v-ST 
    '''

    forward = nx.shortest_path(G, source=ss, weight=weight)
    backward = nx.shortest_path(G, target=st, weight=weight)

    paths = [] 

    for edge in filter(lambda x: x[0] != ss and x[1] != st, G.edges()):
        if edge[0] in forward and edge[1] in backward:
            path = forward[edge[0]] + backward[edge[1]]

            # Clip super source/sink
            path = path[1:-1]

            path_weight = __get_path_weight(G, path, weight)

            paths.append((edge, path, path_weight))

    # Sort by path cost, then by tail/head node names
    return sorted(paths, key=lambda x: (x[2], x[0][0], x[0][1]))


def __project_path(path):
    '''
    Given paths on the product graph, provide a generator of projections back
    onto the original two graphs.
    '''

    G_path = [node[0] for node in path]
    H_path = [node[1] for node in path]

    return (G_path, H_path)


def __construct_product_graph(G, H, S_G, T_G, S_H, T_H, label="l", weight="w"):
    P = label_constrained_tensor_product(G, H, label=label)

    __weight_product_graph(G, P, weight=weight)

    product_sources = __product(S_G, S_H)
    product_targets = __product(T_G, T_H)

    __add_super_source(P, product_sources) 
    __add_super_target(P, product_targets)

    return P


def __rank_results(results):
    '''
    Augment results with a rank that corresponds to the weight of the
    path found for each edge
    '''

    weights = (w for _, _, w in results)
    weights = list(set(weights))
    weights = sorted(weights)

    rank = {}
    for i, weight in enumerate(weights):
        rank[weight] = i

    return sorted(((a, b, c, rank[c]) for a, b, c in results), 
        key=lambda x: (x[2], x[0], x[1]))


def RegLinker(G, H, S_G, T_G, S_H, T_H, label="l", weight="w"):
    '''
    :param G: Directed, weighted, edge-labeled graph
    :param H: DFA interpreted as a directed, edge-labeled graph

    :param S_G: G's sources
    :param T_G: G's targets

    :param S_H: H's sources
    :param T_H: H's targets

    :param label: Edge attribute (in both G and H) to use as a label
    :param weight: Edge attribute in G to use as a weight 
    '''
    
    P = __construct_product_graph(G, H, S_G, T_G, S_H, T_H, label, weight)

    results = QuickLinker(P, SUPER_SOURCE, SUPER_TARGET, weight)

    for edge, path, weight, rank in __rank_results(results):

        G_path, H_path = __project_path(path)
        labeled_path = __path_to_labeled_edges(G, G_path, label)

        yield (edge, path, G_path, H_path, labeled_path, weight, rank)
