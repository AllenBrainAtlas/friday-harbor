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

import numpy as np
import scipy.io as sio
from resources.LinearModel import LinearModel

# Import data:        
LM = LinearModel.load_from_hdf5('./W_ipsi_manuscript.hdf5')

# Load reference data:
published = sio.loadmat('./xls_csv_mat/PValue_ipsi.mat')
P_final = published['data']
row_labels = [str(x).strip() for x in published['row_labels']]
col_labels = [str(x).strip() for x in published['col_labels']]

# Create convenient lookup dictionary:
P_dict_published = {}
for ii, curr_row_acronym in enumerate(row_labels):
    for jj, curr_col_acronym in enumerate(col_labels):
        P_dict_published[curr_row_acronym, curr_col_acronym] = P_final[ii, jj]

# Discrepancy caused by new IJ/IJ_shell values from improved segmentation
delta_list = []
for ii, curr_row_acronym in enumerate(row_labels):
    for jj, curr_col_acronym in enumerate(col_labels):
        
        p_published = P_dict_published[curr_row_acronym, curr_col_acronym] 
        p_new = LM.get_p_val(curr_row_acronym, curr_col_acronym)
        curr_delta = np.abs(p_new - p_published)
        if not np.isnan(curr_delta) and not curr_delta == np.inf:
            delta_list.append(curr_delta)
        
print np.array(delta_list).mean()