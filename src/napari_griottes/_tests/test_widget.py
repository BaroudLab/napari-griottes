import numpy as np

from napari_griottes._widget import make_graph, save_graph, POINT_PARAMS, FUNCS

import os


def test_delaunay_graph(make_napari_viewer, capsys):
    viewer = make_napari_viewer()
    viewer.open_sample("napari-griottes", "zebra")
    nlayers = len(viewer.layers)
    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = make_graph()

    # if we "call" this object, it'll execute our function
    my_widget(viewer.layers["labels"])

    assert len(viewer.layers) == nlayers + 1

    my_widget(viewer.layers["labels"], viewer.layers[POINT_PARAMS["name"]], "Delaunay")

    assert len(viewer.layers) == nlayers + 2
    
    saver = save_graph()
    savepath = os.path.join(os.path.curdir, "test.tif")
    
    saver(viewer.layers[-1], path=savepath)

    assert os.path.exists(savepath+".json")
    os.remove(savepath+".json")


def test_contact_graph(make_napari_viewer, capsys):
    viewer = make_napari_viewer()
    viewer.open_sample("napari-griottes", "zebra")
    nlayers = len(viewer.layers)
    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = make_graph()

    # if we "call" this object, it'll execute our function
    my_widget(viewer.layers["labels"])

    assert len(viewer.layers) == nlayers + 1

    my_widget(viewer.layers["labels"], viewer.layers[POINT_PARAMS["name"]], "Contact_graph")

    assert len(viewer.layers) == nlayers + 2
    
    saver = save_graph()
    savepath = os.path.join(os.path.curdir, "test.tif")
    
    saver(viewer.layers[-1], path=savepath)

    assert os.path.exists(ppp:=savepath+".json")

    layers = viewer.open(ppp, plugin="napari-griottes")
    assert len(layers) == 2

    os.remove(savepath+".json")

def test_geometric_graph(make_napari_viewer, capsys):
    viewer = make_napari_viewer()
    viewer.open_sample("napari-griottes", "zebra")
    nlayers = len(viewer.layers)
    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = make_graph()

    # if we "call" this object, it'll execute our function
    my_widget(viewer.layers["labels"])

    assert len(viewer.layers) == nlayers + 1

    my_widget(viewer.layers["labels"], viewer.layers[POINT_PARAMS["name"]], "Geometric graph")

    assert len(viewer.layers) == nlayers + 2
    
    saver = save_graph()
    savepath = os.path.join(os.path.curdir, "test.tif")
    
    saver(viewer.layers[-1], path=savepath)

    assert os.path.exists(savepath+".json")
    os.remove(savepath+".json")