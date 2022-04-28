"""
This module is an example of a barebones writer plugin for napari.

It implements the Writer specification.
see: https://napari.org/plugins/stable/guides.html#writers

Replace code below according to your needs.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, Tuple, Union

import networkx as nx

if TYPE_CHECKING:
    DataType = Union[Any, Sequence[Any]]
    FullLayerData = Tuple[DataType, dict, str]


def save_graph(path: str, data: FullLayerData, props: dict, **kwargs):
    """Writes a single layer graph"""
    try:
        # nx.write_gpickle(props["metadata"]["graph"], (ppp:=(path if path.endswith(".griottes") else path + ".griottes")))
        nx.write_gpickle(props["metadata"]["graph"], path)
        # print(f'Saved graph to {ppp}')
    except KeyError:
        print("Grapth not found, choose another layer")


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
