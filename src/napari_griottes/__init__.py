try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from ._reader import napari_get_reader
from ._sample_data import make_cell_properties, make_zebrafish_data
from ._widget import ExampleQWidget, example_magic_widget, make_graph
from ._writer import save_graph

__ALL__ = [
    napari_get_reader,
    make_cell_properties,
    make_zebrafish_data,
    example_magic_widget,
    make_graph,
    save_graph,
]
