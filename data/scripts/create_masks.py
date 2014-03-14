import h5py
from resources.Mask import Mask
import resources.Annotation as Annotation
import numpy as np
import resources.Structure as Structure
import resources.Experiment as Experiment

# # Save off the nonzero mask: 
# nonzero_ind_mask = Mask(np.where(Annotation.structure_annotation != 0))
# nonzero_ind_mask.write_to_hdf5('../src/nonzero_ind_mask.hdf5')
# 
# # Save off the left hemisphere mask:
# left_hemisphere_mask = Mask(np.where(Annotation.hemisphere_annotation == 'L'))
# left_hemisphere_mask.write_to_hdf5('../src/left_hemisphere_mask.hdf5')
#
# Save off the right hemisphere mask:
# right_hemisphere_mask = Mask(np.where(Annotation.hemisphere_annotation == 'R'))
# right_hemisphere_mask.write_to_hdf5('../src/right_hemisphere_mask.hdf5')
# 
# # Save off the left hemisphere nonzero mask:
# left_hemisphere_nonzero_ind_mask = Mask.intersection(nonzero_ind_mask, left_hemisphere_mask)
# left_hemisphere_nonzero_ind_mask.write_to_hdf5('../src/left_hemisphere_nonzero_ind_mask.hdf5')
#
# Save off the right hemisphere nonzero mask:
# right_hemisphere_nonzero_ind_mask = Mask.intersection(nonzero_ind_mask, right_hemisphere_mask)
# right_hemisphere_nonzero_ind_mask.write_to_hdf5('../src/right_hemisphere_nonzero_ind_mask.hdf5')

# Create universe mask:
# universal_mask = Mask(np.where(Annotation.structure_annotation != np.nan))
# universal_mask.write_to_hdf5('../src/universal_mask.hdf5')

# Create structure masks:
# f = h5py.File('../src/structure_masks.hdf5','w')
# for s in Structure.structure_list:
#         
#     # Whole region:
#     child_mask_list = [Mask(np.where(Annotation.structure_annotation == s_child.structure_id)) for s_child in s.child_list]
#     structure_mask=reduce(Mask.union, child_mask_list)
#     structure_mask.write_to_hdf5_group(f, create_name='%s_nonzero' % s.acronym)
#     
#     # Left hemisphere:
#     structure_mask_nonzero_left = Mask.intersection(structure_mask, left_hemisphere_nonzero_ind_mask)
#     structure_mask_nonzero_left.write_to_hdf5_group(f, create_name='%s_left_nonzero' % s.acronym)
#     
#     # Right hemisphere:
#     structure_mask_nonzero_right = Mask.intersection(structure_mask, right_hemisphere_nonzero_ind_mask)
#     structure_mask_nonzero_right.write_to_hdf5_group(f, create_name='%s_right_nonzero' % s.acronym)
# f.close()

# Create injection masks:
f_inj = h5py.File('../src/injection_masks.hdf5', 'w')
for e in Experiment.experiment_list:
     
    print e.id
     
    f_in = h5py.File(e.data_file_name, 'r')
    injection_vals = f_in['injection'].value
    f_in.close()
    injection_mask = Mask(np.where(injection_vals != 0))
    injection_mask.write_to_hdf5_group(f_inj, create_name=str(e.id))
  
f_inj.close()

