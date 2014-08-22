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

import scipy.io as sio

# Load the data (ipsi is right hemisphere):
# Row is source, col is target
D_W_ipsi = sio.loadmat('../linear_model/W_ipsi.mat')
D_W_contra = sio.loadmat('../linear_model/W_contra.mat')
D_PValue_ipsi = sio.loadmat('../linear_model/PValue_ipsi.mat')
D_PValue_contra = sio.loadmat('../linear_model/PValue_contra.mat')

# Each data dictionary has 3 keys: 'row_labels', 'col_labels', and 'data'
def get_value(data_dictionary, source_acronym, target_acronym):
    source_ind = map(lambda x:x.strip(), map(str, list(data_dictionary['row_labels']))).index(source_acronym)
    target_ind = map(lambda x:x.strip(), map(str, list(data_dictionary['col_labels']))).index(target_acronym)
    return data_dictionary['data'][source_ind, target_ind]

# Get the LGd to ipsi-to-ipsi connection strength and PValue:
print get_value(D_W_ipsi, 'LGd', 'VISp'), get_value(D_PValue_ipsi, 'LGd', 'VISp')
