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

import pickle as pkl
import os
import numpy as np
import re
import h5py
import Experiment

def pickle(data, file_name):
    
    f = open( file_name, "wb" )
    pkl.dump(data, f)
    f.close()

def unpickle(file_name):
    
    f = open( file_name, "rb" )
    data = pkl.load(f)
    f.close()
    
    return data

def extract_volume(load_dir, file_name_prefix, dtype):

    f = open(os.path.join(load_dir, file_name_prefix) + '.mhd', 'r')
    header = f.read()
    f.close()
    f = open(os.path.join(load_dir, file_name_prefix) + '.raw', 'r')
    raw = f.read()
    f.close()

    arr = np.frombuffer(raw, dtype=dtype)

    # parse the meta image header.  each line should be a 'key = value' pair.
    metaLines = header.split('\n')
    metaInfo = dict(line.split(' = ') for line in metaLines if line)

    # convert values to numeric types as appropriate
    for k,v in metaInfo.iteritems():
        if re.match("^[\d\s]+$",v):
            nums = v.split(' ')
            if len(nums) > 1:
                metaInfo[k] = map(float, v.split(' '))
            else:
                metaInfo[k] = int(nums[0])

    # reshape the array to the appropriate dimensions.  Note the use of the fortran column ordering.
    arr = arr.reshape(metaInfo['DimSize'], order='F')
    
    return (header,arr,metaInfo)

def get_density_from_LIMS_id(LIMS_id):
    
    # Create injection masks:
    f_proj = h5py.File(os.path.join(os.path.dirname(__file__),'../data/src/projection_density.hdf5'), 'r')
    density_vals = f_proj[str(LIMS_id)].value
    f_proj.close()
    
    density_vals[np.where(density_vals < 0)] = 0
    
    return density_vals

def write_dictionary_to_group(group, dictionary, create_name = None):
    
    if create_name != None:
        group = group.create_group(create_name)
    for key, val in dictionary.items():
        group[str(key)] = val
    
    return

def read_dictionary_from_group(group):
    
    dictionary = {}
    for name in group:
        dictionary[str(name)] = group[name].value
        
    return dictionary


def generate_optimization_matrices(source_id_list, target_id_list, minimum_number_voxels_in_at_least_one_injection = 50, LIMS_id_list = Experiment.all_experiment_LIMS_list, source_shell=False):

    from resources.Mask import Mask
    from resources.Structure import Structure
    
    # Get injection masks:
    PD_dict = {}
    injection_mask_dict = {}
    injection_mask_dict_shell = {}
    for curr_LIMS_id in LIMS_id_list:
        PD_dict[curr_LIMS_id] =  get_density_from_LIMS_id(curr_LIMS_id)
        injection_mask_dict[curr_LIMS_id] = Experiment.Experiment.get_injection_mask(curr_LIMS_id)
        if source_shell == True:
            injection_mask_dict_shell[curr_LIMS_id] = Experiment.Experiment.get_injection_mask(curr_LIMS_id, shell=True)
            
    # Get region masks:
    region_mask_dict = {}
    region_mask_ipsi_dict = {}
    region_mask_contra_dict = {}
    for curr_structure_id in source_id_list + target_id_list:
        region_mask_dict[curr_structure_id] = Structure.get_mask_from_id_nonzero(curr_structure_id)
        region_mask_ipsi_dict[curr_structure_id] = Structure.get_mask_from_id_right_hemisphere_nonzero(curr_structure_id)
        region_mask_contra_dict[curr_structure_id] = Structure.get_mask_from_id_left_hemisphere_nonzero(curr_structure_id)
    
    def get_integrated_PD(curr_LIMS_id, intersection_mask):
        if len(intersection_mask) > 0:
            curr_sum = PD_dict[curr_LIMS_id][intersection_mask.mask].sum()
        else:
            curr_sum = 0
            
        return curr_sum
    
    # Initialize matrices:
    structures_above_threshold_ind_list = []
    experiment_source_matrix_pre = np.zeros((len(LIMS_id_list), len(source_id_list)))
    
    # Source:
    for jj, curr_structure_id in enumerate(source_id_list):

        # Get the region mask:
        curr_region_mask = region_mask_dict[curr_structure_id]
        
        ipsi_injection_volume_list = []
        for ii, curr_LIMS_id in enumerate(LIMS_id_list):
    
            # Get the injection mask:
            curr_experiment_mask = injection_mask_dict[curr_LIMS_id]
    
            # Compute integrated density, source:
            intersection_mask = Mask.intersection(curr_experiment_mask, curr_region_mask)
            experiment_source_matrix_pre[ii, jj] = get_integrated_PD(curr_LIMS_id, intersection_mask)        
            ipsi_injection_volume_list.append(len(intersection_mask)) 
    
        # Determine if current structure should be included in source list:
        ipsi_injection_volume_array = np.array(ipsi_injection_volume_list)
        number_of_experiments_above_threshold = len(np.nonzero(ipsi_injection_volume_array >= minimum_number_voxels_in_at_least_one_injection)[0])
        if number_of_experiments_above_threshold > 0:
            structures_above_threshold_ind_list.append(jj)
            
    # Determine which experiments should be included:
    expermiments_with_one_nonzero_structure_list = [] 
    for ii, row in enumerate(experiment_source_matrix_pre):
        if row.sum() > 0.:
            expermiments_with_one_nonzero_structure_list.append(ii)

    if len(structures_above_threshold_ind_list) < len(source_id_list):
        raise Exception
    
    experiment_source_matrix = experiment_source_matrix_pre[:,structures_above_threshold_ind_list][expermiments_with_one_nonzero_structure_list,:]
    row_label_list = np.array(LIMS_id_list)[expermiments_with_one_nonzero_structure_list]
    col_label_list_source = np.array(source_id_list)[structures_above_threshold_ind_list]
     
    # Target:
    experiment_target_matrix_ipsi = np.zeros((len(row_label_list), len(target_id_list)))
    experiment_target_matrix_contra = np.zeros((len(row_label_list), len(target_id_list)))
    for jj, curr_structure_id in enumerate(target_id_list):

        # Get the region mask:
        curr_region_mask_ipsi = region_mask_ipsi_dict[curr_structure_id]
        curr_region_mask_contra = region_mask_contra_dict[curr_structure_id]
        
        for ii, curr_LIMS_id in enumerate(row_label_list):
    
            # Get the injection mask:
            if source_shell == True:
                curr_experiment_mask = injection_mask_dict_shell[curr_LIMS_id]
            else:
                curr_experiment_mask = injection_mask_dict[curr_LIMS_id]
            
            # Compute integrated density, target, ipsi:
            difference_mask = curr_region_mask_ipsi.difference(curr_experiment_mask)
            experiment_target_matrix_ipsi[ii, jj] = get_integrated_PD(curr_LIMS_id, difference_mask)
            
            # Compute integrated density, target, contra:    
            difference_mask = curr_region_mask_contra.difference(curr_experiment_mask)
            experiment_target_matrix_contra[ii, jj] = get_integrated_PD(curr_LIMS_id, difference_mask) 

    # Include only structures with sufficient injection information, and experiments with one nonzero entry in row:
    experiment_dict = {}
    experiment_dict['experiment_source_matrix'] = experiment_source_matrix
    experiment_dict['experiment_target_matrix_ipsi'] = experiment_target_matrix_ipsi
    experiment_dict['experiment_target_matrix_contra'] = experiment_target_matrix_contra
    experiment_dict['col_label_list_source'] = col_label_list_source 
    experiment_dict['col_label_list_target'] = np.array(target_id_list)
    experiment_dict['row_label_list'] = row_label_list 
    
    return experiment_dict

def seconds_to_str(t):
    rediv = lambda ll,b : list(divmod(ll[0],b)) + ll[1:]
    return "%d:%02d:%02d.%03d" % tuple(reduce(rediv,[[t*1000,],1000,60,60]))