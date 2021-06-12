"""
    Dummy conftest.py for kubi.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

# import pytest
import os
import glob
import shutil
import urllib.request

path_in =  './tests/in/'
path_out =  './tests/out/'

def pytest_configure(config):
  # remove output folder
    if not os.path.exists(path_out):
        os.makedirs(path_out)

    if  os.path.exists(path_out+'/sub'):
        shutil.rmtree(path_out+'/sub')

    if  os.path.exists(path_out+'/tiled'):
        shutil.rmtree(path_out+'/tiled')
        
    for f in glob.glob(path_out+'*', recursive=True):
        os.remove(f)

    # create input folder
    if not os.path.exists(path_in):
        os.makedirs(path_in)

    # download test images
    test_images= {
        "basemap.tif": "https://geoservice.dlr.de/eoc/basemap/wms?VERSION=1.1.1&REQUEST=GetMap&SRS=epsg:4326&BBOX=-180,-90,180,90&WIDTH=4096&HEIGHT=2048&FORMAT=image/geotiff&LAYERS=basemap",
        "baseoverlay.tif": "https://geoservice.dlr.de/eoc/basemap/wms?VERSION=1.1.1&REQUEST=GetMap&SRS=epsg:4326&BBOX=-180,-90,180,90&WIDTH=3072&HEIGHT=1536&FORMAT=image/geotiff&TRANSPARENT=true&LAYERS=baseoverlay",
     }

    for file in test_images.items():
        if not os.path.exists(path_in + file[0]):
            with urllib.request.urlopen(file[1]) as response, open(path_in + file[0], 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

    shutil.copyfile(path_in + "basemap.tif", path_out + "bm.tif")