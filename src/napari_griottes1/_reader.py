"""
This module is an example of a barebones numpy reader plugin for napari.

It implements the Reader specification, but your plugin may choose to
implement multiple readers or even other plugin contributions. see:
https://napari.org/plugins/stable/guides.html#readers
"""
import numpy as np
import pandas
from tifffile import imread


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


def colorized_points(data, **kwargs):
    return [
        (
            data[["z", "y", "x"]].values,
            {
                **dict(
                    ndim=3,
                    size=5,
                    properties=data,
                    face_color="cell_type",
                    face_color_cycle=["#ff00ff", "#ffff00", "#00ffff"],
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
    arrays = [np.load(_path) for _path in paths]
    # stack arrays into single array
    data = np.squeeze(np.stack(arrays))

    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {}

    layer_type = "image"  # optional, default is "image"
    return [(data, add_kwargs, layer_type)]
