"""
This module is an example of a barebones writer plugin for napari.

It implements the Writer specification.
see: https://napari.org/plugins/stable/guides.html#writers

Replace code below according to your needs.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, Tuple, Union

import networkx as nx
import json

if TYPE_CHECKING:
    DataType = Union[Any, Sequence[Any]]
    FullLayerData = Tuple[DataType, dict, str]

import numpy as np

def numpy_to_python(value):
    if isinstance(value, np.generic):
        return value.tolist()
    return value

def save_graph_to_json(graph, filename):
    
    with open(filename, 'w') as file:
        json.dump({
            "nodes": list(graph.nodes.data()),
            "edges": list(graph.edges.data())
        }, file, default=_ser)
    return [filename]

def _ser(o):
    """convert types for json.dumps to work"""
    try:
        if isinstance(o, (int,np.int32, np.intc)):
            return int(o)
        elif isinstance(o, (float, str)):
            return o
        else:
            return list(0)
    except TypeError as e:
        print(o, type(o))
        raise e

def save_graph(path: str, data: FullLayerData, props: dict, **kwargs):
    """Writes a single layer graph"""
    try:
        ppp = path if path.endswith(".json") else path + ".json"
        out = save_graph_to_json(data.metadata["graph"], ppp)
        print(f"Saved graph to {out}")
    except KeyError:
        print("Grapth not found, choose another layer")
    return [out]


# (
#     '/home/aaristov/test',

#     [
#         <class 'numpy.ndarray'> (2, 2) float64,
#         <class 'numpy.ndarray'> (2, 2) float64,
#         <class 'numpy.ndarray'> (2, 2) float64
#     ],

#     {
#         'name': 'Connections',
#         'metadata':
#         {
#             'graph': <networkx.classes.graph.Graph object at 0x7f39a5a71d60>
#         },
#         'scale': [1.0, 1.0],
#         'translate': [0.0, 0.0],
#         'rotate': [[1.0, 0.0], [0.0, 1.0]],
#         'shear': [0.0],
#         'opacity': 0.7,
#         'blending': 'translucent',
#         'visible': True,
#         'experimental_clipping_planes': [],
#         'ndim': 2,
#         'properties': {},
#         'property_choices': {},
#         'text': {'values': <class 'numpy.ndarray'> (0,) <U32,
#         'visible': True,
#         'size': 12,
#         'color': <class 'numpy.ndarray'> (4,) float64,
#         'blending': <Blending.TRANSLUCENT: 'translucent'>,
#         'anchor': <Anchor.CENTER: 'center'>,
#         'translation': 0, 'rotation': 0},
#         'shape_type': ['line', 'line', 'line'],
#         'z_index': [0, 0, 0],
#         'edge_width': [1, 1, 1],
#         'face_color': <class 'numpy.ndarray'> (3, 4) float64,
#         'face_color_cycle': <class 'numpy.ndarray'> (2, 4) float32,
#         'face_colormap': 'viridis', 'face_contrast_limits': None,
#         'edge_color': <class 'numpy.ndarray'> (3, 4) float64,
#         'edge_color_cycle': <class 'numpy.ndarray'> (2, 4) float32,
#         'edge_colormap': 'viridis',
#         'edge_contrast_limits': None,
#         'features': Empty DataFrame
#     Columns: []
#     Index: [0, 1, 2]
#     }
# )
