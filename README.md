# RegLinker
Connect the dots in protein interaction networks ... using regular
expressions!

## About

Cellular biology is predicated upon many complex interactions that
take place among biomolecules, including genes and proteins. These
supply the machinery by which cells live, grow, and reproduce. Taken
together, the whole of these interactions is termed the *interactome*. 

### Signaling Pathways

Subsets of the interactome allow cells to implement complex signaling
mechanisms, by which they can sense their environment and respond
appropriately to the perceived conditions. These *signaling pathways*,
networks of molecular interactions that together effect some
biological function, are widely studied. In such pathways,
membrane-bound proteins called *receptors* act as initial sensors,
binding with molecules originating outside the cell. These signals are
then propagated inside the cell via further interactions involving
intermediate proteins. Ultimately, this process will reach
*transcription factors* (TF), upon which point, DNA transcription, and
thus, cell behavior, will be affected.

Numerous databases exist to catalogue the interactions that comprise
known signaling pathways; however, manual curation of signaling
pathways is time consuming and painstaking. A natural question arises:
given the interactome and the interactions annotated to a given
curated pathway, can we computationally identify candidate proteins
from the interactome that might be considered for inclusion in the
pathway?

### Automated Signaling Pathway Curation

RegLinker offers one approach to automated pathway curation, treating
the interactome itself as a directed graph, *G*, wherein a vertex represents
a protein, and an edge is present between two vertices if their
corresponding proteins interact. For a given signaling pathway, we can
distinguish the edges of *G* with one of two labels: *known*, for
those edges whose corresponding interactions appear in the signaling
pathway, and *unknown*, for those edges whose corresponding
interactions have not been so annotated.

Underlying RegLinker are two key principles. The first of these is
that proteins that lie along the shortest paths from receptors to
transcription factors in *G* are most likely to be involved in a
signaling pathway. The second is that, considering our earlier
labeling, we can partition these paths into subpaths of the following
structure: each subpath contains only interactions with the label
*known* or the label *unknown*. The challenge is that we do not know
*a priori* how many edges each of these subpaths contains. Our key
insight is that a regular language acts as a constraint that allows us
to control the number of and structure by which new edges (and
vertices) are considered for addition to the signaling pathway.

### Regular Languages

Informally, a regular language is a set of strings with the property
thatan algorithm that uses a fixed amount of memory can examine the
lettersin the string sequentially to determine if it is a member of
the language. For example, for the alphabet {*p*,*x*}, regular languages
are expressive enough to represent strings with an even number of
occurrences of *p* or strings where *p* and *x* strictly alternate an
arbitrary number of times.

A regular language can be equivalently represented by a *regular
expression* or a deterministic finite automaton (DFA).

For a given regular language *L*, we say that a path in *G* is
*regular-language-constrained* if the concatenation of the labels of
the edges along the path forms a string that is a member of *L*.

### RegLinker

As input, RegLinker requires:

- a directed, weighted, edge-labeled graph, *G*, corresponding to the
  interactome; 

- a subnetwork *P* of *G* representing the vertices and edges of a
  curated signaling pathway;

- sets *S<sub>G</sub>* and *T<sub>G</sub>* of vertices corresponding to
  the receptor and TF proteins in *P*;

- a directed, edge-labeled graph *H* corresponding to the DFA. 

- and sets *S<sub>H</sub>* and *T<sub>H</sub>* of vertices
  corresponding to the start and final states of the DFA.

It then computes, for each edge in *G*, a shortest *S*-*T* path
in *G*, should one exist. To produce a ranked list of candidate
interactions, we order the edges in *G* in increasing order of weight.
Then, for each edge *e* with a rank *r* (edges may be tied in weight),
we assign a rank of *r* to every edge in the shortest *S*-*T* path via
*e*, provided the edge has not already received a rank.

## Dependencies

This implementation of RegLinker is written in Python 3, and is
designed to be used in conjunction with the NetworkX library, v.2.1.

## Usage

Please see [the documentation for examples of usage](./docs/usage.md).

## Reference, Citation, and Collaboration

RegLinker is the subject of a to-be-published manuscript as a part of
conference proceedings. In the interim, we ask that if you use
RegLinker in your work, that you please reach out for information on
best to cite RegLinker.

We encourage experimentation with RegLinker. Please don't hesitate to
contact us if you would like to collaborate!
