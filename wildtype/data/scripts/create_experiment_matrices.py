import os
from resources.utilities import unpickle
import numpy as np
from resources.Structure import Structure
from resources.Experiment import Experiment
from resources.Mask import Mask
import h5py
import resources.utilities as utilities

# Settings:
rel_data_dir = '../src/'
minimum_number_voxels_in_at_least_one_injection = 50
save_file_name = 'experiment_matrices.hdf5'

# Initializations:
path_to_this_file = os.path.dirname(os.path.realpath(__file__))

# Get data:
structure_id_list = unpickle('../src/structure_id_list.p')
LIMS_id_list = unpickle('../src/LIMS_id_list.p')

# Get injection masks:
PD_dict = {}
injection_mask_dict = {}
for curr_LIMS_id in LIMS_id_list:
    PD_dict[curr_LIMS_id] =  utilities.get_density_from_LIMS_id(curr_LIMS_id)
    injection_mask_dict[curr_LIMS_id] = Experiment.get_injection_mask(curr_LIMS_id)
    
# Get region masks:
region_mask_dict = {}
region_mask_ipsi_dict = {}
region_mask_contra_dict = {}
for curr_structure_id in structure_id_list:
    region_mask_dict[curr_structure_id] = Structure.get_mask_from_id_nonzero(curr_structure_id)
    region_mask_ipsi_dict[curr_structure_id] = Structure.get_mask_from_id_right_hemisphere_nonzero(curr_structure_id)
    region_mask_contra_dict[curr_structure_id] = Structure.get_mask_from_id_left_hemisphere_nonzero(curr_structure_id)

def get_integrated_PD(curr_LIMS_id, intersection_mask):
    if len(intersection_mask) > 0:
        curr_sum = PD_dict[curr_LIMS_id][intersection_mask.mask].sum()
    else:
        curr_sum = 0
        
    return curr_sum

# Organize matrices:
structures_above_threshold_ind_list = []
experiment_source_matrix_pre = np.zeros((len(LIMS_id_list), len(structure_id_list)))
experiment_target_matrix_ipsi_pre = np.zeros((len(LIMS_id_list), len(structure_id_list)))
experiment_target_matrix_contra_pre = np.zeros((len(LIMS_id_list), len(structure_id_list)))
for jj, curr_structure_id in enumerate(structure_id_list):

    # Get the region mask:
    curr_region_mask = region_mask_dict[curr_structure_id]
    curr_region_mask_ipsi = region_mask_ipsi_dict[curr_structure_id]
    curr_region_mask_contra = region_mask_contra_dict[curr_structure_id]
    
    ipsi_injection_volume_list = []
    for ii, curr_LIMS_id in enumerate(LIMS_id_list):

        # Get the injection mask:
        curr_experiment_mask = injection_mask_dict[curr_LIMS_id]

        # Compute integrated density, source:
        intersection_mask = Mask.intersection(curr_experiment_mask, curr_region_mask)
        experiment_source_matrix_pre[ii, jj] = get_integrated_PD(curr_LIMS_id, intersection_mask)
        
        # Compute integrated density, target, ipsi:
        difference_mask = curr_region_mask_ipsi.difference(curr_experiment_mask)
        experiment_target_matrix_ipsi_pre[ii, jj] = get_integrated_PD(curr_LIMS_id, difference_mask)
        
        # Compute integrated density, target, contra:    
        difference_mask = curr_region_mask_contra.difference(curr_experiment_mask)
        experiment_target_matrix_contra_pre[ii, jj] = get_integrated_PD(curr_LIMS_id, difference_mask)        
            
        ipsi_injection_volume_list.append(len(intersection_mask)) 

    ipsi_injection_volume_array = np.array(ipsi_injection_volume_list)
    number_of_experiments_above_threshold = len(np.nonzero(ipsi_injection_volume_array >= minimum_number_voxels_in_at_least_one_injection)[0])
    if number_of_experiments_above_threshold > 0:
        structures_above_threshold_ind_list.append(jj)

# Include only structures with sufficient injection information:
experiment_source_matrix = experiment_source_matrix_pre[:,structures_above_threshold_ind_list]
experiment_target_matrix_ipsi = experiment_target_matrix_ipsi_pre[:,structures_above_threshold_ind_list]
experiment_target_matrix_contra = experiment_target_matrix_contra_pre[:,structures_above_threshold_ind_list]
col_label_list = np.array(structure_id_list)[structures_above_threshold_ind_list]
row_label_list = np.array(LIMS_id_list) 
 
 
 
f = h5py.File(os.path.join(path_to_this_file, rel_data_dir, save_file_name), 'w')
f['experiment_source_matrix'] = experiment_source_matrix
f['experiment_target_matrix_ipsi'] = experiment_target_matrix_ipsi
f['experiment_target_matrix_contra'] = experiment_target_matrix_contra
f['row_label'] = row_label_list
f['col_label'] = col_label_list
f.close()



