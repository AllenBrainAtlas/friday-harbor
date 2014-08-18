# Copyright 2014 Allen Institute for Brain Science
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Nicholas Cain
# Allen Institute for Brain Science
# June 11 2014
# nicholasc@alleninstitute.org

import h5py
import numpy as np
import resources.mhd as mhd
import requests
import os
import zipfile
import shutil

# Settings:
file_save_dir = 'data/src'
grid_annotation_url = 'http://api.brain-map.org/api/v2/well_known_file_download/197676381'
file_name = os.path.join(file_save_dir, 'grid_annotation.zip')

# Get data:
with open(file_name,'wb') as handle:
    request = requests.get(grid_annotation_url, stream=True)
    for block in request.iter_content(1024):
        if not block:
            break
        handle.write(block)
handle.close()

# Unzip:
unzip_path = os.path.join(file_save_dir, 'grid_annotation')
shutil.rmtree(unzip_path, unzip_path)
os.mkdir(unzip_path)
zf = zipfile.ZipFile(file_name, 'r')
zf.extractall(unzip_path)
zf.close()
os.remove(file_name)

mhd_path = os.path.join(file_save_dir, "grid_annotation", "gridAnnotation.mhd")
annotation_info, annotation_values = mhd.read(mhd_path)

h5_path = os.path.join(file_save_dir, "grid_annotation.hdf5")
f = h5py.File(h5_path, "w")
f['grid_annotation'] = annotation_values
f.close()
