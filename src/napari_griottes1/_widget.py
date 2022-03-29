"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/guides.html#widgets

Replace code below according to your needs.
"""
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton
from magicgui import magic_factory
import griottes
import networkx as nx
import numpy as np
import napari
import pandas as pd

FUNCS = {
    "Contact_graph": griottes.generate_contact_graph,
    "Geometric graph": griottes.generate_geometric_graph,
    "Delaunay": griottes.generate_delaunay_graph,
}

@magic_factory(
    auto_call=True,
    graph={"widget_type": "ComboBox", "choices": FUNCS.keys(),},
    distance={"widget_type": "Slider", "min":10, "max":150, }
)
def make_contact_graph(
    label_layer: "napari.layers.Labels",
    point_layer: "napari.layers.Points",
    graph:"str" = list(FUNCS.keys())[0],
    distance:"int" = 35) -> napari.types.LayerDataTuple :

    # print(f"you have selected {img_layer}, {img_layer.data.shape}")
    if point_layer is None:
        print('No points, generating')
        centers = griottes.analyse.cell_property_extraction.get_nuclei_properties(label_layer.data, mask_channel = None)
        try:
            centers = centers.rename(columns={'centroid-0' : 'x', 'centroid-1' : 'y', 'centroid-2' : 'z'})
            return [
                (
                    centers[['z','y','x']], 
                    {"name":"Centers", "properties": centers},
                    'points'
                ),
            ]
        except KeyError:
            centers = centers.rename(columns={'centroid-0' : 'x', 'centroid-1' : 'y', })
            return [
                (
                    centers[['y','x']], 
                    {"name":"Centers", "properties": centers},
                    'points'
                ),
            ]
    data = pd.DataFrame(point_layer.properties)
    try:
        G = FUNCS[graph](
            data,
            descriptors=['label', 'cell_type', 'x', 'y', 'z','cell_properties'],
            dCells=distance,
        )
    except (TypeError, AttributeError):
        G = FUNCS[graph](
            data,
            analyze_fluo_channels=False,
        )
    except AssertionError:
        G = FUNCS[graph](
            data,
            dCells=distance,
        )

    pos = nx.get_node_attributes(G, 'pos')
    zyx = {k:(v[0], v[2], v[1]) for k,v in pos.items()}
    lines = [[zyx[i] for i in ids] for ids in list(G.edges)]

    return [
        (
            np.array(lines),
            {"shape_type":"line", "name":"Connections", "edge_color":"white"},
            'shapes'
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

