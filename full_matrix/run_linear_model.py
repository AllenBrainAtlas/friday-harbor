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
import os
import h5py
import resources.utilities as utilities
from resources.LinearModel import LinearModel as LM
import scipy.optimize as sopt

# Settings:
load_file_name = 'experiment_matrices.hdf5'
rel_data_dir = './results'
save_dir = './results'
save_file_name_ipsi = 'W_ipsi.hdf5'
save_file_name_contra = 'W_contra.hdf5'

# Initializations:
path_to_this_file = os.path.dirname(os.path.realpath(__file__))

# Load data:
f = h5py.File(os.path.join(path_to_this_file, rel_data_dir, load_file_name), 'r')
experiment_dict = utilities.read_dictionary_from_group(f)
f.close()

def fit_linear_model(A, B, col_labels, row_labels):
    
    X = np.zeros((np.shape(A)[1], np.shape(B)[1]))
    for jj, col in enumerate(B.T):
        b = col.T
        X[:,jj] = sopt.nnls(A, b)[0]
        
    return LM(X, col_labels, row_labels)

# Ipsilateral fit:
A = experiment_dict['experiment_source_matrix']
B = experiment_dict['experiment_target_matrix_ipsi']
col_labels = experiment_dict['col_label_list_target']
row_labels = experiment_dict['col_label_list_source']
ipsi_LM = fit_linear_model(A, B, col_labels, row_labels)
ipsi_LM.run_regression(A, B, col_labels, row_labels)
ipsi_LM.save_to_hdf5(os.path.join(save_dir, save_file_name_ipsi))

# Contralateral fit:
A = experiment_dict['experiment_source_matrix']
B = experiment_dict['experiment_target_matrix_contra']
col_labels = experiment_dict['col_label_list_target']
row_labels = experiment_dict['col_label_list_source']
contra_LM = fit_linear_model(A, B, col_labels, row_labels)
contra_LM.run_regression(A, B, col_labels, row_labels)
contra_LM.save_to_hdf5(os.path.join(save_dir, save_file_name_contra))
    

    
