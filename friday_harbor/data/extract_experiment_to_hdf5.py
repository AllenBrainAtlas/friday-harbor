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
import os
import sys
import numpy as np

from friday_harbor import mhd 
from friday_harbor.Mask import Mask
from friday_harbor.utilities import write_dictionary_to_group
from friday_harbor.paths import Paths

def extract_experiment_to_hdf5(data_dir=None):
    paths = Paths(data_dir)

    raw_data_dir = paths.experiment_raw_data_dir

    # Settings:
    f_proj = h5py.File(paths.projection_densities_file_name, 'w')
    f_inj_vol = h5py.File(paths.injection_volumes_file_name, 'w')

    # Extract volumes of PD and injection sites:
    for experiment_id in os.listdir(raw_data_dir):
        curr_dir = os.path.join(raw_data_dir, experiment_id)
  
        density_mhd = os.path.join(curr_dir, 'density.mhd')
        density_info, density_array = mhd.read(density_mhd)
        
        f_proj[experiment_id] = density_array
    
        injection_mhd = os.path.join(curr_dir, 'injection.mhd')
        injection_info, injection_array = mhd.read(injection_mhd)

        f_inj_vol[experiment_id] = injection_array

    f_proj.close()
    f_inj_vol.close()

if __name__ == "__main__":
    if len(sys.argv == 2):
        extract_experiment_to_hdf5(sys.argv[1])
    else:
        extract_experiment_to_hdf5()
