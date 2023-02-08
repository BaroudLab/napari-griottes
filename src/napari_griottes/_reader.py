"""
This module is an example of a barebones numpy reader plugin for napari.

It implements the Reader specification, but your plugin may choose to
implement multiple readers or even other plugin contributions. see:
https://napari.org/plugins/stable/guides.html#readers
"""
import networkx as nx
import numpy as np
import pandas
import pandas as pd
from tifffile import imread

from ._widget import CNAME


def napari_get_reader(path):
    """A basic implementation of a Reader contribution.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    # if we know we cannot read the file, we immediately return None.
    if path.endswith(".tif") or path.endswith(".tiff"):
        return read_tif

    if path.endswith(".csv"):
        return read_csv

    if path.endswith(".griottes"):
        return read_griottes

    # otherwise we return the *function* that can read ``path``.
    if path.endswith(".npy"):
        return reader_numpy

    return None


def read_tif(path="", **kwargs):
    print(f"Opening {path}")
    data = imread(path)
    print(f"input shape: {data.shape}")
    if data.shape[-1] < 10:
        dims = list(range(data.ndim))
        last_dim = dims.pop()
        dims.insert(0, last_dim)
        data = data.transpose(*dims)
        print(f"transpose -> {data.shape}")

    return [(data, {"channel_axis": 0, **kwargs}, "image")]


def read_csv(path, **kwargs):
    data = pandas.read_csv(path, index_col=None)
    try:
        return colorized_points(data, metadata={"path": path})
    except KeyError:
        return [
            (
                data[["y", "x"]].values,
                {"metadata": {"path": path}, **kwargs},
                "points",
            )
        ]


def read_griottes(
    path,
):

    G = nx.read_gpickle(path)
    pos = nx.get_node_attributes(G, "pos")

    try:
        centers = pd.DataFrame(
            [
                {"z": v[0], "y": v[1], "x": v[2], "label": k}
                for k, v in pos.items()
            ]
        )
        out = centers[["z", "y", "x"]]
    except IndexError:
        centers = pd.DataFrame(
            [{"y": v[0], "x": v[1], "label": k} for k, v in pos.items()]
        )
        out = centers[["y", "x"]]

    lines = [[pos[i] for i in ids] for ids in list(G.edges)]
    try:
        weights = [0.2 * 1 * e[2]["weight"] for e in G.edges(data=True)]
    except (IndexError, KeyError):
        print("no weights")
        weights = [1] * len(lines)

    print(
        f"{len(lines)} lines for {len(centers)}  positions recovered, rendering..."
    )
    return [
        (
            out,
            {"name": "Centers", "properties": centers},
            "points",
        ),
        (
            lines,
            {
                "shape_type": "line",
                "name": CNAME,
                "edge_width": weights,
                "metadata": {"graph": G},
            },
            "shapes",
        ),
    ]


def colorized_points(data, **kwargs):
    data.loc[:,"colors_napari"] = data["cell_type"] / data["cell_type"].max()
    return [
        (
            data[["z", "y", "x"]].values,
            {
                **dict(
                    ndim=3,
                    size=5,
                    properties=data,
                    face_color="colors_napari",
                    face_colormap='viridis',
                    opacity=0.5,
                ),
                **kwargs,
            },
            "points",
        )
    ]


def reader_numpy(path):
    """Take a path or list of paths and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of
        layer.
        Both "meta", and "layer_type" are optional. napari will default to
        layer_type=="image" if not provided
    """
    # handle both a string and a list of strings
    paths = [path] if isinstance(path, str) else path
    # load all files into array
    arrays = [np.load(_path, allow_pickle=True).item()["masks"] for _path in paths]
    # stack arrays into single array
    data = np.squeeze(np.stack(arrays))

    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {}

    layer_type = "image"  # optional, default is "image"
    return [(data, add_kwargs, layer_type)]
