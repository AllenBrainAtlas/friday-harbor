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
from resources.Experiment import ExperimentManager
import os

exp_manager = ExperimentManager()

# Create density maps:
f_proj = h5py.File('data/src/projection_density.hdf5', 'w')
for e in exp_manager:
    if os.path.isfile(e.data_file_name):
        f_in = h5py.File(e.data_file_name, 'r')
        density_vals = f_in['density'].value
        f_in.close()
        f_proj[str(e.id)] = density_vals
    
f_proj.close()
