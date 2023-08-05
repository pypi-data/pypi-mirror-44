#    This file is part of KTBS <http://liris.cnrs.fr/sbt-dev/ktbs>
#    Copyright (C) 2011-2012 Pierre-Antoine Champin <pchampin@liris.cnrs.fr> /
#    Universite de Lyon <http://www.universite-lyon.fr>
#
#    KTBS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    KTBS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with KTBS.  If not, see <http://www.gnu.org/licenses/>.

"""
Utility functions for method implementations.
"""
from rdflib import BNode, Graph, URIRef
from rdfrest.util import check_new, make_fresh_uri

from ..namespace import KTBS

def replace_obsels(computed_trace, raw_graph, inherit=False):
    """
    Replace the @obsels graph of computed_trace with raw_graph.

    If raw_graph contains blank obsels, a URI will be generated for them.
    Except for that, no processing or verification is done on raw_graph,
    so it must be valid.
    """
    obsels = computed_trace.obsel_collection
    rg_add = raw_graph.add
    ct_uri = computed_trace.uri

    if inherit:
        rg_val = raw_graph.value
        getobs = computed_trace.service.get
        triples = raw_graph.triples((None, KTBS.hasSourceObsel, None))
        for newnode, _, olduri in triples:
            # if ktbs:hasTrace is not specified,
            # it must be smartly set and *not* inherited:
            rg_add((newnode, KTBS.hasTrace, ct_uri))
            oldobs = getobs(olduri)
            for _, prop, val in oldobs.state.triples((olduri, None, None)):
                if rg_val(newnode, prop) is None:
                    rg_add((newnode, prop, val))

    bnodes = [ i for i in raw_graph.subjects(KTBS.hasBegin, None)
               if isinstance(i, BNode) ]
    bnode_map = None
    if bnodes:
        bnode_map = {}
        for bnode in bnodes:
            new_uri = make_fresh_uri(raw_graph, ct_uri + "o-")
            bnode_map[bnode] = new_uri
            rg_add((new_uri, KTBS.hasTrace, ct_uri))

    with obsels.edit(_trust=True) as editable:
        obsels._empty() # friend #pylint: disable=W0212
        if bnodes:
            bm_get = bnode_map.get
            triples = ( [ bm_get(x, x) for x in triple] for triple in raw_graph )
        else:
            triples = iter(raw_graph)
        editable.addN( (s, p, o, editable) for s, p, o in triples )

def translate_node(node, transformed_trace, src_uri, multiple_sources, prevent=None):
    """
    If node is a URI, translate its URI to put it in transfored_trace. Else,
    leave it unchanged.
    """
    if not isinstance(node, URIRef):
        return node
    if not node.startswith(src_uri):
        return node
    if multiple_sources:
        _, tid, oid = node.rsplit("/", 2)
        new_id = "%s_%s" % (tid, oid)
    else:
        _, new_id = node.rsplit("/", 1)
    ret = URIRef("%s%s" % (transformed_trace.uri, new_id))
    if prevent is not None and prevent(ret):
        ret = None
    return ret

def copy_obsel(obsel_uri, computed_trace, source_trace, new_obs_uri=None, check_new_obs=None):
    """
    I prepare a graph for an transformed obsel being a copy of ``obsel``.
    """
    new_obs_graph = Graph()
    new_obs_add = new_obs_graph.add

    if check_new_obs:
        _target_obsels = computed_trace.obsel_collection.state
        def check_new_obs(uri):
            return check_new(_target_obsels, uri)

    source_uri = source_trace.uri
    source_triples = source_trace.obsel_collection.state.triples
    if new_obs_uri is None:
        new_obs_uri = translate_node(obsel_uri, computed_trace, source_uri, False)

    new_obs_add((new_obs_uri, KTBS.hasTrace, computed_trace.uri))
    new_obs_add((new_obs_uri, KTBS.hasSourceObsel, obsel_uri))

    for _, pred, obj in source_triples((obsel_uri, None, None)):
        if pred == KTBS.hasTrace  or  pred == KTBS.hasSourceObsel:
            continue
        new_obj = translate_node(obj, computed_trace, source_uri,
                                 False, check_new_obs)
        if new_obj is None:
            continue # skip relations to nodes that are filtered out or not created yet
        new_obs_add((new_obs_uri, pred, new_obj))

    for subj, pred, _ in source_triples((None, None, obsel_uri)):
        if pred == KTBS.hasTrace  or  pred == KTBS.hasSourceObsel:
            continue
        new_subj = translate_node(subj, computed_trace, source_uri,
                                  False, check_new_obs)
        if new_subj is None:
            continue # skip relations from nodes that are filtered out or not created yet
        new_obs_add((new_subj, pred, new_obs_uri))

    return new_obs_graph


def boolean_parameter(value):
    return value.strip().lower() not in { "false", "no", "0" }

