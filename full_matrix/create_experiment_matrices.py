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

import os
import resources.utilities as utilities
import h5py
import resources.Experiment as Experiment

# Settings:
rel_data_dir = './results/'
save_file_name = 'experiment_matrices.hdf5'
LIMS_id_list = Experiment.wildtype_experiment_LIMS_list

# Initializations:
path_to_this_file = os.path.dirname(os.path.realpath(__file__))

# Load data:
source_id_list = utilities.unpickle('../data/src/structure_id_list.p')
target_id_list = utilities.unpickle('../data/src/structure_id_list.p')

# Create experiment:
experiment_dict = utilities.generate_optimization_matrices(source_id_list, target_id_list, LIMS_id_list=LIMS_id_list, minimum_number_voxels_in_at_least_one_injection = 50)
 
# Save to file:
f = h5py.File(os.path.join(path_to_this_file, rel_data_dir, save_file_name), 'w')
utilities.write_dictionary_to_group(f, experiment_dict)
f.close()



