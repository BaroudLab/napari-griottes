import numpy as np

from napari_griottes._widget import make_graph, save_graph, POINT_PARAMS, FUNCS

import os


def test_make_graph(make_napari_viewer, capsys):
    viewer = make_napari_viewer()
    viewer.open_sample("napari-griottes", "zebra")
    nlayers = len(viewer.layers)
    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = make_graph()

    # if we "call" this object, it'll execute our function
    points, meta, _ = my_widget(viewer.layers["labels"])[0]

    assert len(viewer.layers) == nlayers + 1

    vectors, meta, _ = my_widget(viewer.layers["labels"], viewer.layers[POINT_PARAMS["name"]])[0]

    assert len(viewer.layers) == nlayers + 2
    
    saver = save_graph()
    savepath = os.path.join(os.path.curdir, "test.griottes")
    
    saver(viewer.layers[-1], path=savepath)

    assert os.path.exists(savepath)
    os.remove(savepath)
