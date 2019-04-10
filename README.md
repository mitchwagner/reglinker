# RegLinker
Connect the dots in protein interaction networks ... using regular expressions!

## About
The inputs to RegLinker are a set of sources, a set of targets, an
edge-labeled protein interaction network, and the DFA coresponding to
a regular language. RegLinker computes, for each edge in the
interaction network, a shortest path from the set of sources to the
set of targets through that edge, such that each path is *regular
language constrained*: that is, the concatentation of the labels of
the edges along the path forms a word in the specified regular
language. This is achieved through finding paths in an
appropriately-defined product of the interaction network and the DFA.  

This implementation of RegLinker is written in Python 3, and is
designed to be used in conjunction with the NetworkX library.

## Dependencies

This implementation of RegLinker requires NetworkX 2.1.

## How to Run

Definitions:
- *G*: NetworkX DiGraph representing an interaction network
- *S<sub>G</sub>*: Iterable of sources for *G*
- *T<sub>G</sub>*: Iterable of targets for *G*

- *H*: DFA, represented as a NetworkX DiGraph
- *S<sub>H</sub>*: Iterable of start states for *H* 
- *T<sub>H</sub>*: Iterable of final states *H*

Each edge in *G* and each edge in *H* must be labeled using a common
dictionary attribute. Each edge in *G* must also have a common
attribute to denote an edge weight.

With these inputs in hand, RegLinker can be imported and run as
follows:

```python
import RegLinker as rl

results = rl.RegLinker(G, H, S_G, T_G, S_H, T_H, label="l", weight="w")

```

This will create a generator that yields tuples of the form:

```python
(edge, path, G_path, H_path, labeled_path, cost, rank)
```

Here:
- *edge* is the edge considered
- *path* is the path found in the product graph
- *G\_path\_* and *H\_path\_* are the paths formed by
  projecting the product *path* onto *G* and *H*
- *labeled\_path* is *path*, annotated with edge labels
- *cost* is the sum of the weights of the path
- *rank* is an ordering of the paths, from lowest to highest cost. A
  rank of zero indicates the lowest-cost path.

These tuples are produced in ascending order of rank.

## IO

The file RegLinkerIO.py contains some convenient utility functions for
reading and writing results to disk.

```python
import RegLinker as rl
import RegLinkerIO as rlio


# Open file handles
net_file = open('examples/network.tsv', 'r') 
net_nodes_file = open('examples/net-nodes.tsv', 'r')

dfa_file = open('examples/dfa.tsv', 'r') 
dfa_nodes_file = open('examples/dfa-nodes.tsv', 'r')


# Read networks in. Here, label_col and weight_col refer to the
# 0-indexed column of the corresponding TSV file.

G = rlio.read_graph(net_file, label_col=2, weight_col=3)
S_G, T_G = rlio.read_node_types(net_nodes_file) 

H = rlio.read_graph(dfa_file, label_col=2)
S_H, T_H = rlio.read_node_types(dfa_nodes_file)


# Obtain RegLinker results
results = rl.RegLinker(G, H, S_G, T_G, S_H, T_H, label="l", weight="w")
```
