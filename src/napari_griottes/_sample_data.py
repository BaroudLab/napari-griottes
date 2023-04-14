"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/plugins/stable/guides.html#sample-data

Replace code below according to your needs.
"""
from __future__ import annotations

import os
import pathlib

from ._reader import read_csv, read_tif

GRIOTTES_DATA = [
    ("zebrafish_brain_cell_labels.tiff", read_tif),
    ("zebrafish_cell_properties.csv", read_csv),
]


def make_zebrafish_data():
    data = _load_griottes_sample_data(*GRIOTTES_DATA[0])[0][0]
    return[
        (
            d, {"name": name}, layer_type) \
            for d, name, layer_type in \
            zip(
                data, 
                ["ch 1", "ch 2", "ch 3", "ch 4", "labels"],
                ["image", "image", "image", "image", "labels" ]
            )
    ]


def make_cell_properties():

    return _load_griottes_sample_data(*GRIOTTES_DATA[1])


def download_url_to_file(
    url,
    file_path,
):
    import shutil

    import urllib3

    print(f"Downloading {url}")
    c = urllib3.PoolManager()
    with c.request("GET", url, preload_content=False) as resp, open(
        file_path, "wb"
    ) as out_file:
        shutil.copyfileobj(resp, out_file)
    resp.release_conn()
    print(f"Saved {file_path}")
    return file_path


def _load_griottes_sample_data(image_name, readfun=read_tif, **kwargs):

    cp_dir = pathlib.Path.home().joinpath(".griottes")
    cp_dir.mkdir(exist_ok=True)
    data_dir = cp_dir.joinpath("data")
    data_dir.mkdir(exist_ok=True)

    url = (
        "https://github.com/BaroudLab/Griottes/releases/download/v1.0-alpha/"
        + image_name
    )

    cached_file = str(data_dir.joinpath(image_name))
    if not os.path.exists(cached_file):
        print(f"Downloading {image_name}")
        download_url_to_file(url, cached_file)
    return readfun(cached_file, **kwargs)
