# napari-griottes1

[![License](https://img.shields.io/pypi/l/napari-griottes1.svg?color=green)](https://github.com/aaristov/napari-griottes1/raw/main/LICENSE)
<!-- [![PyPI](https://img.shields.io/pypi/v/napari-griottes1.svg?color=green)](https://pypi.org/project/napari-griottes1) -->
[![Python Version](https://img.shields.io/pypi/pyversions/napari-griottes1.svg?color=green)](https://python.org)
[![tests](https://github.com/aaristov/napari-griottes1/workflows/tests/badge.svg)](https://github.com/aaristov/napari-griottes1/actions)
[![codecov](https://codecov.io/gh/aaristov/napari-griottes1/branch/main/graph/badge.svg)](https://codecov.io/gh/aaristov/napari-griottes1)
<!-- [![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-griottes1)](https://napari-hub.org/plugins/napari-griottes1) -->

Create graphs

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/plugins/stable/index.html
-->

## Installation

You can install `napari-griottes1` via [pip]:

    Not available yet



To install latest development version :

    pip install git+https://github.com/aaristov/napari-griottes1.git

## Usage

### Starting with labels:

1. Open the plugin in Plugins/napari-griottes1
2. Make sure the layer with labels is selected 
3. Click Run once to get centers
4. Click Run second time to get graph
5. Select the right kind of graph in the drop-down menu
6. Adjust the distance
7. Adjust thickness

![Screenshot from three labels geometric contact mp4](https://user-images.githubusercontent.com/11408456/167371516-05db2ba5-cdfc-47c4-a488-8f46afd0ae5b.png)


https://user-images.githubusercontent.com/11408456/167371532-796650fe-dd19-4fed-a328-a7ccd627c883.mp4

### Starting with Segmented cells

1. Open sample data: File / Open Sample / napari-griottes1 / Zebrafish 2D with labels
2. Convert the segmented layer to napari labels (right click - Convert to labels)
3. Proceed with graph creation
![Screenshot from cells graphs mp4](https://user-images.githubusercontent.com/11408456/167372895-3c9036b9-af50-4575-bcf3-1805eb261bd7.png)



https://user-images.githubusercontent.com/11408456/167372921-305e9e3d-1480-430a-b1e5-5416d178c55b.mp4

### Saving and recovering the graph

Any graph you see in napari can be saved in .griottes format which is networkx.gpickle inside.
1. Select he layers with connections
2. Click File/Save Selected Layer
3. Choose Griottes in drop-down menu
4. Save

In order to recover a previously saved graph in napari, you can simply drag-n-drop your file into napari, or use file open fialog.

Otherwise, you can open the graph with [neworkx.read_gpickle](https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.gpickle.read_gpickle.html) function 

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-griottes1" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/aaristov/napari-griottes1/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
