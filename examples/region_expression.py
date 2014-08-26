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

from friday_harbor.structure import Ontology
from friday_harbor.mask import Mask
import friday_harbor.experiment as experiment

# Settings:
data_dir = '../friday_harbor/data'
my_target_structure_acronym_list = ['VISp1', 'VISp2/3', 'VISp4', 'VISp5', 'VISp6a', 'VISp6b'] 
my_LIMS_id = 100141598 # LGd Injection

# Initialize:
ontology = Ontology(data_dir=data_dir)
experiment_manager = experiment.ExperimentManager(data_dir=data_dir)

# Grab the particular experiment:
my_experiment = experiment_manager.experiment_by_id(my_LIMS_id)

'''
Print the mean projection density in VISp, broken down by layer
some PD values are negative, and are ignored
    -1: insufficient pixels data in a grid voxel to have reliable values
    -2: missing tile
    -3: no data (manually annotated)
'''
print "%7s: %3s %7s" % ('Area', '#:', 'mean:')
for curr_acronym in my_target_structure_acronym_list:
    curr_id = ontology.acronym_id_dict[curr_acronym]
    m_right = ontology.get_mask_from_id_right_hemisphere_nonzero(curr_id)
    density_vals = my_experiment.density(mask_obj=m_right)
    density_vals_clean = density_vals[density_vals>=0]
    print "%7s: %3s %7.4f" % (curr_acronym, len(density_vals_clean), density_vals_clean.mean()) 





