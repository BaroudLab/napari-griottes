"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/guides.html#widgets

Replace code below according to your needs.
"""
import griottes
import napari
import networkx as nx
import numpy
import numpy as np
import pandas as pd
from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget

FUNCS = {
    "Geometric graph": griottes.generate_geometric_graph,
    "Delaunay": griottes.generate_delaunay_graph,
    "Contact_graph": griottes.generate_contact_graph,
}
CNAME = "Connections"
viewer = napari.current_viewer()


@magic_factory(
    auto_call=False,
    graph={
        "widget_type": "ComboBox",
        "choices": FUNCS.keys(),
    },
    distance={
        "widget_type": "Slider",
        "min": 10,
        "max": 150,
    },
    thickness={
        "widget_type": "Slider",
        "min": 1,
        "max": 5,
    },
)
def make_graph(
    label_layer: "napari.layers.Labels",
    point_layer: "napari.layers.Points",
    graph: "str",
    distance: "int" = 35,
    thickness: "int" = 1,
) -> napari.types.LayerDataTuple:

    # print(f"you have selected {img_layer}, {img_layer.data.shape}")
    if point_layer is None:
        print("No points, generating")
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
                    {"name": "Centers", "properties": centers},
                    "points",
                ),
            ]
        except KeyError:
            # print("centers 2D")
            centers = raw_centers.rename(
                columns={
                    "centroid-0": "y",
                    "centroid-1": "x",
                }
            )
            return [
                (
                    centers[["y", "x"]],
                    {"name": "Centers", "properties": centers},
                    "points",
                ),
            ]
    data = pd.DataFrame(point_layer.properties)
    repr(data.head())
    weights = thickness
    if "z" in data.columns:
        try:
            print("Graph in 3D")
            weights = thickness * 0.2
            G = FUNCS[graph](
                data[["z", "y", "x", "label"]],
                distance=distance,
            )

            pos = nx.get_node_attributes(G, "pos")
            lines = np.array(
                [[pos[i] for i in ids] for ids in list(G.edges)], dtype="int"
            )
            print(
                f"{len(lines)} lines for {len(pos)}  positions computed, rendering..."
            )
            # print(lines)
            try:
                viewer.layers.remove(CNAME)
            except ValueError:
                pass
            return [
                (
                    lines,
                    {
                        "shape_type": "line",
                        "name": CNAME,
                        "metadata": {"graph": G},
                    },
                    "shapes",
                )
            ]
        except ValueError:
            print("ValueError")
    else:
        try:
            print("Graph in 2D,")

            G = FUNCS[graph](
                data[["x", "y", "label"]],
                image_is_2D=True,
                distance=distance,
            )

            pos = nx.get_node_attributes(G, "pos")
            # yx = {k:(v[1], v[0]) for k,v in pos.items()}
            lines = [[pos[i] for i in ids] for ids in list(G.edges)]
        except TypeError:
            print("contact graph")
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
                print(
                    "weights failed!",
                )

    return [
        (
            lines,
            {
                "shape_type": "line",
                "name": CNAME,
                "edge_width": weights,
                "metadata": {"graph": G},
            },
            "shapes",
        )
    ]


class ExampleQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn = QPushButton("Click me!")
        btn.clicked.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

    def _on_click(self):
        print("napari has", len(self.viewer.layers), "layers")


@magic_factory
def example_magic_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")
