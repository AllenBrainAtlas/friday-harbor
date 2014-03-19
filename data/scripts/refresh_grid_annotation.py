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
from resources.utilities import extract_volume
import requests
import os
import zipfile
import shutil

# Settings:
file_save_dir = '../src'
grid_annotation_url = 'http://api.brain-map.org/api/v2/well_known_file_download/197676381'
file_name = os.path.join(os.path.dirname(__file__), file_save_dir, 'grid_annotation.zip')

# Get data:
with open(file_name,'wb') as handle:
    request = requests.get(grid_annotation_url, stream=True)
    for block in request.iter_content(1024):
        if not block:
            break
        handle.write(block)
handle.close()

# Unzip:
unzip_path = os.path.join(os.path.dirname(__file__), file_save_dir, 'grid_annotation')
shutil.rmtree(unzip_path, unzip_path)
os.mkdir(unzip_path)
zf = zipfile.ZipFile(file_name, 'r')
zf.extractall(unzip_path)
zf.close()
os.remove(file_name)

# Settings:
file_save_dir = '../src/grid_annotation'
grid_annotation_file_name_prefix = 'gridAnnotation'
 
# Extract grid annotation:
_, arr_grid_annotation, _ = extract_volume(file_save_dir, grid_annotation_file_name_prefix, dtype = np.uint32)
save_file_name = os.path.join(file_save_dir, '%s.hdf5' % grid_annotation_file_name_prefix)
f = h5py.File(save_file_name, 'w')
f['grid_annotation'] = arr_grid_annotation
f.close()