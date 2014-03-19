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
from resources.Structure import id_acronym_dict
import scipy.io as sio
from resources.LinearModel import LinearModel

# Import data:
LM = LinearModel.load_from_hdf5('./W_ipsi_manuscript.hdf5')
f = h5py.File('./W_ipsi_manuscript.hdf5')
W = f['W'].value
P = f['P'].value
col_labels = f['col_labels'].value
row_labels = f['row_labels'].value
f.close()
 
# Create convenient lookup dictionary:
W_dict = {}
for ii, curr_row_label in enumerate(row_labels):
    for jj, curr_col_label in enumerate(col_labels):
        curr_row_acronym = id_acronym_dict[curr_row_label]
        curr_col_acronym = id_acronym_dict[curr_col_label]
        W_dict[curr_row_acronym, curr_col_acronym] = W[ii, jj]
        
# Load reference data:
published = sio.loadmat('./xls_csv_mat/W_ipsi.mat')
W_final = published['data']
row_labels = [str(x).strip() for x in published['row_labels']]
col_labels = [str(x).strip() for x in published['col_labels']]

# Create convenient lookup dictionary:
W_dict_published = {}
for ii, curr_row_acronym in enumerate(row_labels):
    for jj, curr_col_acronym in enumerate(col_labels):
        W_dict_published[curr_row_acronym, curr_col_acronym] = W_final[ii, jj]

# Discrepancy caused by new IJ/IJ_shell values from improved segmentation
max_delta=-1
delta_list = []
for ii, curr_row_acronym in enumerate(row_labels):
    for jj, curr_col_acronym in enumerate(col_labels):
        curr_delta = np.abs(W_dict_published[curr_row_acronym, curr_col_acronym] - LM.get_w_val(curr_row_acronym, curr_col_acronym))
        delta_list.append(curr_delta) 
        if curr_delta > max_delta:
            max_delta = curr_delta
        
print max_delta, np.array(delta_list).mean()