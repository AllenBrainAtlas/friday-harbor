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

import sys
import os
import itertools
import h5py
import numpy as np
from friday_harbor.mask import Mask
from friday_harbor.ontology import Ontology
from friday_harbor.experiment_manager import ExperimentManager
from friday_harbor.annotation import StructureAnnotation
from friday_harbor.paths import Paths
import copy


def create_masks(data_dir='.'):
    paths = Paths(data_dir)

    structure_annotation = StructureAnnotation.from_hdf5(paths.structure_annotation_file_name)

    # Save off the brain mask: 
    brain_mask = Mask(np.where(structure_annotation != 0))
    brain_mask.write_to_hdf5(paths.brain_mask_file_name)
  
    # Save off the left hemisphere mask:
    left_hemisphere_mask = Mask(structure_annotation.left_hemisphere)
    left_hemisphere_mask.write_to_hdf5(paths.left_hemisphere_mask_file_name)
 
    # Save off the right hemisphere mask:
    right_hemisphere_mask = Mask(structure_annotation.right_hemisphere)
    right_hemisphere_mask.write_to_hdf5(paths.right_hemisphere_mask_file_name)
  
    # Save off the left hemisphere nonzero mask:
    left_hemisphere_nonzero_mask = Mask.intersection(brain_mask, left_hemisphere_mask)
    left_hemisphere_nonzero_mask.write_to_hdf5(paths.left_hemisphere_nonzero_mask_file_name)
 
    # Save off the right hemisphere nonzero mask:
    right_hemisphere_nonzero_mask = Mask.intersection(brain_mask, right_hemisphere_mask)
    right_hemisphere_nonzero_mask.write_to_hdf5(paths.right_hemisphere_nonzero_mask_file_name)
 
    # Create universe mask:
    universal_mask = Mask(np.where(structure_annotation != np.nan))
    universal_mask.write_to_hdf5(paths.universal_mask_file_name)
    
    # Create structure masks:
    f = h5py.File(paths.structure_masks_file_name,'w')
    for s in Ontology(data_dir):
        print "creating structure masks for", s.structure_id

        # Whole region:
        child_mask_list = [Mask(np.where(structure_annotation == s_child.structure_id)) for s_child in s.child_list]
        structure_mask= Mask.union(*child_mask_list)

        structure_mask.write_to_hdf5_group(f, create_name='%s_nonzero' % s.acronym)
      
        # Left hemisphere:
        structure_mask_nonzero_left = Mask.intersection(structure_mask, left_hemisphere_nonzero_mask)
        structure_mask_nonzero_left.write_to_hdf5_group(f, create_name='%s_left_nonzero' % s.acronym)
        
        # Right hemisphere:
        structure_mask_nonzero_right = Mask.intersection(structure_mask, right_hemisphere_nonzero_mask)
        structure_mask_nonzero_right.write_to_hdf5_group(f, create_name='%s_right_nonzero' % s.acronym)
    f.close()

    # Create injection masks (also with a shell):
    f_inj = h5py.File(paths.injection_masks_file_name, 'w')
    f_inj_shell = h5py.File(paths.injection_masks_shell_file_name, 'w')

    for e in ExperimentManager(data_dir):
        print "creating injection masks for", e.id
        injection_vals = e.injection()

        injection_mask = Mask(np.where(injection_vals != 0))    
        injection_mask.write_to_hdf5_group(f_inj, create_name=str(e.id))
#         injection_mask_inverse = copy.copy(universal_mask).difference(injection_mask)
#         injection_mask_inverse.write_to_hdf5_group(f_inj, create_name="%s_inverse" % str(e.id))


        for c_x, c_y, c_z in zip(*injection_mask.mask):
            for x_i, y_i, z_i in itertools.product(c_x+np.array([-1,0,1]),
                                                   c_y+np.array([-1,0,1]),
                                                   c_z+np.array([-1,0,1])):
                if 0<=x_i<np.shape(injection_vals)[0] and 0<=y_i<np.shape(injection_vals)[1] and 0<=z_i<np.shape(injection_vals)[2]: 
                    injection_vals[x_i, y_i, z_i] = 1
         
        injection_mask_shell = Mask(np.where(injection_vals != 0))
        injection_mask_shell.write_to_hdf5_group(f_inj_shell, create_name=str(e.id))
   
    f_inj.close()
    f_inj_shell.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        create_masks(sys.argv[1])
    else:
        create_masks()

# # Create injection masks with a shell, from manuscript annotation:    
# import scipy.io as sio
# f_inj = h5py.File('../src/injection_masks_shell.hdf5', 'w')
# XX = sio.loadmat('/local1/Connectivity/Connectivity_staging_dir/XX.mat')['XX']
# YY = sio.loadmat('/local1/Connectivity/Connectivity_staging_dir/YY.mat')['YY']
# ZZ = sio.loadmat('/local1/Connectivity/Connectivity_staging_dir/ZZ.mat')['ZZ']
# IJ_shell = sio.loadmat('/local1/Connectivity/Connectivity_staging_dir/IJ_shell.mat')['IJ_shell']
# IS = sio.loadmat('/local1/Connectivity/Connectivity_staging_dir/IS.mat')['IS']
# 
# for ii, curr_LIMS_id in enumerate(np.squeeze(IS)):
#     print ii
#     curr_annotation = copy.copy(Annotation.all_zero)
#     e = Experiment.LIMS_id_experiment_dict[curr_LIMS_id]
#     nonzero_inds = np.where(IJ_shell[ii, :] != 0)
#     x_inds = XX[nonzero_inds]
#     y_inds = YY[nonzero_inds]
#     z_inds = ZZ[nonzero_inds]
#     
#     for xi, yi, zi in zip(x_inds, y_inds, z_inds):
#         curr_annotation[xi, yi, zi] = 1
#     
#     curr_injection_mask = Mask(np.where(curr_annotation != 0))
#     curr_injection_mask.write_to_hdf5_group(f_inj, create_name=str(e.id))
# f_inj.close()

