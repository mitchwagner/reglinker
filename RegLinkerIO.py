import networkx as nx

def filter_comments(handle):
    return (line for line in handle if not line.startswith("#"))


def tokenize(line):
    return [x.strip() for x in line.split("\t")]


def add_edge(G, toks, label_col=None, weight_col=None, label="l", weight="w"):
    '''
    Accessory method for adding an edge to G. 

    Note: if the edge has already been added with a different label, both
        labels will be tracked, but the weight of the edge will be overwritten
        by the edge that is added last.
    '''
    tail = toks[0]
    head = toks[1]

    kwargs = {}

    if label_col != None:
        # If we've already seen this edge with a different label,
        # make sure to keep track of both
        if G.has_edge(tail, head):
            G[tail][head][label].append(toks[label_col])

        else:
            kwargs[label] = [toks[label_col]]
        
    if weight_col != None:
        kwargs[weight] = float(toks[weight_col])

    G.add_edge(tail, head, **kwargs)


def read_graph(handle, label_col=None, weight_col=None, label="l", weight="w"):
    '''
    Graphs should be in tab-separated edge-list format, where the first two
    columns of a row correspond to the tail and head nodes of an edge.

    :param handle: graph file handle

    :param label_col: column to be read as labels for the edges (if any)
        Note: 0-indexed

    :param weight_col: column to be read as weight for the edges (if any)
        Note: 0-indexed

    :param label: name to be used for the edge label field

    :param weight: name to be used fot the weight label field

    :returns: NetworkX DiGraph

    '''

    G = nx.DiGraph()

    lines = filter_comments(handle)

    for line in lines:
        add_edge(G, tokenize(line), label_col, weight_col, label, weight)

    return G


def read_node_types(handle, type_col=1, 
        source_kws=["source"], target_kws=["target"]):

    '''
    Read sources and targets from a tab-separated file, one node per line. 

    If a node is listed as both a source and a target, it will be returned
    as such.

    :param handle: node type file handle
    :param type_col: 0-indexed column to be interpreted as the node type
    :param source_kws: list of type keywords indicating sources
    :param source_kws: list of type keywords indicating targets 

    :returns: generators for sources and targets

    '''
    
    lines = filter_comments(handle)

    sources = []
    targets = []

    for line in lines:
        toks = tokenize(line)
        node = toks[0]
        node_type = toks[type_col]
    
        if node_type in source_kws:
            sources.append(node)

        elif node_type in target_kws:
            targets.append(node)

    return sources, targets


def write_edge_file(handle, results):
    for i, (edge, _, _, _, _, weight, rank) in enumerate(results):

        if i != 0:
            handle.write("\n")

        handle.write(str(edge[0]) + "\t")
        handle.write(str(edge[1]) + "\t")
        handle.write(str(rank) + "\t")
        handle.write(str(weight))


def write_projected_edge_file(handle, results):
    for i, (edge, _, _, _, _, weight, rank) in enumerate(results):

        if i != 0:
            handle.write("\n")

        handle.write(str(edge[0][0]) + "\t")
        handle.write(str(edge[1][0]) + "\t")
        handle.write(str(rank) + "\t")
        handle.write(str(weight))


def write_paths_file(handle, results):
    for i, (_, path, g_path, h_path, labeled_path, weight, rank) \
            in enumerate(results):

        if i != 0:
            handle.write("\n")

        path_string = "|".join([str(compound_node) for compound_node in path])
        g_path_string = "|".join([str(node) for node in g_path])
        h_path_string = "|".join([str(node) for node in h_path])
        labeled_string = ", ".join([str(edge) for edge in labeled_path])

        handle.write(str(rank) + "\t")
        handle.write(str(weight) + "\t")
        handle.write(path_string + "\t")
        handle.write(g_path_string + "\t")
        handle.write(h_path_string + "\t")
        handle.write(labeled_string)
