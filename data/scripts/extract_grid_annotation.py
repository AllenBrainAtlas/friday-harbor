import h5py
import os
import numpy as np
from resources.utilitys import extract_volume
from resources.hdf5_tools import write_dictionary_to_group
from resources.Voxel_Mask import VoxelMask

# Settings:
grid_annotation_dir = '../src'
grid_annotation_file_name_prefix = 'grid_annotation'

# Extract grid annotation:
_, arr_grid_annotation, _ = extract_volume(grid_annotation_dir, grid_annotation_file_name_prefix, dtype = np.uint32)

save_file_name = os.path.join(grid_annotation_dir, '%s.hdf5' % grid_annotation_file_name_prefix)

f = h5py.File(save_file_name, 'w')
f['grid_annotation'] = arr_grid_annotation
f.close()