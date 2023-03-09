"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/guides.html#widgets

Replace code below according to your needs.
"""
import griottes
import napari
import networkx as nx
import numpy as np
import pandas as pd
from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget
import logging
import pickle

logger = logging.getLogger("griottes.widget")
logger.setLevel(logging.INFO)

FUNCS = {
    "Delaunay": griottes.generate_delaunay_graph,
    "Contact_graph": griottes.generate_contact_graph,
    "Geometric graph": griottes.generate_geometric_graph,
}
CNAME = "Connections"
POINT_PARAMS = {"size":10,  "opacity": .8, "name": "Centers"}

@magic_factory()
def save_graph(
    graph_layer: "napari.layers.Vectors",
    path: str
):
    graph = graph_layer.metadata["graph"]
    return _save_graph(graph=graph, path=path)
    

@magic_factory(
    auto_call=True,
    graph={
        "widget_type": "ComboBox",
        "choices": FUNCS.keys(),
    },
    distance={
        "widget_type": "Slider",
        "min": 10,
        "max": 150,
    },
)
def make_graph(
    label_layer: "napari.layers.Labels",
    point_layer: "napari.layers.Points",
    graph: "str",
    distance: "int" = 85,
    thickness: "int" = 1,
) -> napari.types.LayerDataTuple:

    # logger.info(f"you have selected {img_layer}, {img_layer.data.shape}")
    datapath = label_layer.source.path
    savepath = None if datapath is None else datapath + ".graph.griottes"

    if point_layer is None:
        return make_point_layer(label_layer=label_layer)
    data = pd.DataFrame(point_layer.properties)
    repr(data.head())
    weights = thickness
    logger.info(f"{len(data)} nodes")
    logger.info(f"{graph}")
    if "z" in data.columns:
        try:
            logger.info("Graph in 3D")
            weights = thickness * 0.2
            G = FUNCS[graph](
                data[["z", "y", "x", "label"]],
                distance=distance,
            )

            pos = nx.get_node_attributes(G, "pos")
            lines = np.array(
                [[pos[i] for i in ids] for ids in list(G.edges)], dtype="int"
            )
            vectors = [np.vstack([v[0],np.diff(v, axis=0)]) for v in lines]
            logger.info(
                f"{len(lines)} edges for {len(pos)}  positions computed, rendering..."
            )
            return [
                (
                    vectors,
                    {
                        "name": CNAME,
                        "metadata": {"graph": G},
                    },
                    "vectors",
                )
            ]
        except ValueError:
            logger.error("ValueError")
    else:
        try:
            logger.info("Graph in 2D")

            G = FUNCS[graph](
                data[["x", "y", "label"]],
                image_is_2D=True,
                distance=distance,
            )

            pos = nx.get_node_attributes(G, "pos")
            # yx = {k:(v[1], v[0]) for k,v in pos.items()}
            lines = [[pos[i] for i in ids] for ids in list(G.edges)]

            vectors = [np.vstack([v[0],np.diff(v, axis=0)]) for v in lines]
            logger.info(
                f"{len(lines)} edges for {len(pos)}  positions computed, rendering...")
        except TypeError:
            logger.info("contact graph")
            G = FUNCS[graph](
                label_layer.data,
            )
            pos = nx.get_node_attributes(G, "pos")
            lines = [[pos[i] for i in ids] for ids in list(G.edges)]
            try:
                weights = [
                    0.2 * thickness * e[2]["weight"]
                    for e in G.edges(data=True)
                ]
            except IndexError:
                logger.info(
                    "weights failed!",
                )

    return [
        (
            vectors,
            {
                "name": CNAME,
                "edge_width": weights,
                "metadata": {"graph": G},
            },
            "vectors",
        )
    ]

def save_and_return_layer(vectors, graph, weights=None, path=None):
    if path:
        _save_graph(graph=graph, path=path)
    return [
        (
            vectors,
            {
                "name": CNAME,
                "edge_width": weights if weights is not None else 1,
                "metadata": {"graph": graph},
            },
            "vectors",
        )
    ]


def _save_graph(graph, path):
    try:
        pickle.dump(
            graph,
            (
                ppp := (
                    path if path.endswith(".griottes") else path + ".griottes"
                )
            ),
        )
        print(f"Saved graph to {ppp}")
        return [ppp]
    except Exception as e:
        print(f"Unable to save the graph: {e}")
        return None

def make_point_layer(label_layer):
    logger.info("No points, generating")
    raw_centers = (
        griottes.analyse.cell_property_extraction.get_nuclei_properties(
            label_layer.data, mask_channel=None
        )
    )
    try:
        centers = raw_centers.rename(
            columns={
                "centroid-0": "z",
                "centroid-1": "y",
                "centroid-2": "x",
            }
        )
        return [
            (
                centers[["z", "y", "x"]],
                {"properties": centers, **POINT_PARAMS},
                "points",
            ),
        ]
    except KeyError:
        # logger.info("centers 2D")
        centers = raw_centers.rename(
            columns={
                "centroid-0": "y",
                "centroid-1": "x",
            }
        )
        return [
            (
                centers[["y", "x"]],
                {"properties": centers, **POINT_PARAMS},
                "points",
            ),
        ]
