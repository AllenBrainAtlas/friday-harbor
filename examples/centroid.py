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

from friday_harbor.ontology import Ontology
from friday_harbor.mask import Mask

# Settings:
data_dir = '../friday_harbor/data'
my_structure_acronym_list = ['LGd', 'VISp', 'MOs'] 

# Construct the ontology from the data directory:
ontology = Ontology(data_dir=data_dir)

# Print the centroids (each hemisphere and in total) for structures:
for a in my_structure_acronym_list:
    curr_id = ontology.acronym_id_dict[a]
    m_left = ontology.get_mask_from_id_left_hemisphere_nonzero(curr_id)
    m_right = ontology.get_mask_from_id_right_hemisphere_nonzero(curr_id)
    m_all = ontology.get_mask_from_id_nonzero(curr_id)
    print '%4s:' % a,  m_left.centroid, m_right.centroid, m_all.centroid
