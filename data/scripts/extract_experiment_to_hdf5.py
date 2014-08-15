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
import numpy as np
from resources.utilities import extract_volume
from resources.utilities import write_dictionary_to_group

# Settings:
raw_data_dir = 'data/src/raw_data'
save_file_name_prefix = 'density_energy_injection'

# Extract volumes of PD and injection sites:
for experiment_id in os.listdir(raw_data_dir):
    curr_dir = os.path.join(raw_data_dir, experiment_id)
    
    _, arr_density, _ = extract_volume(curr_dir, 'density', dtype = np.float32)
    _, arr_injection, _ = extract_volume(curr_dir, 'injection', dtype = np.float32)
    
    save_file_name = os.path.join(curr_dir, '%s_%s.hdf5' % (save_file_name_prefix, experiment_id))
    f = h5py.File(save_file_name, 'w')
    write_dictionary_to_group(f, {'density':arr_density, 'injection':arr_injection})
    f.close()
    
