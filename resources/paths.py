import os

paths_dir = os.path.dirname(__file__)
data_dir = os.path.normpath(os.path.join(paths_dir, '../data/src'))
experiment_raw_data_directory = os.path.normpath(os.path.join(paths_dir, '../data/src/raw_data'))

structure_json_file_name = os.path.normpath(os.path.join(data_dir, 'structure_data.json'))
experiment_json_file_name = os.path.normpath(os.path.join(data_dir, 'experiment_data.json'))

structure_annotation_file_name = os.path.normpath(os.path.join(data_dir, 'grid_annotation.hdf5'))
structure_masks_file_name = os.path.normpath(os.path.join(data_dir, 'structure_masks.hdf5'))

injection_volumes_file_name = os.path.normpath(os.path.join(data_dir, 'injection_volumes.hdf5'))
injection_masks_file_name = os.path.normpath(os.path.join(data_dir, 'injection_masks.hdf5'))
injection_masks_shell_file_name = os.path.normpath(os.path.join(data_dir, 'injection_masks_shell.hdf5'))
projection_densities_file_name = os.path.normpath(os.path.join(data_dir, 'projection_density.hdf5'))

left_hemisphere_mask_file_name = os.path.normpath(os.path.join(data_dir, 'left_hemisphere_mask.hdf5'))
left_hemisphere_nonzero_mask_file_name = os.path.normpath(os.path.join(data_dir, 'left_hemisphere_nonzero_mask.hdf5'))

right_hemisphere_mask_file_name = os.path.normpath(os.path.join(data_dir, 'right_hemisphere_mask.hdf5'))
right_hemisphere_nonzero_mask_file_name = os.path.normpath(os.path.join(data_dir, 'right_hemisphere_nonzero_mask.hdf5'))

brain_mask_file_name = os.path.normpath(os.path.join(data_dir, 'brain_mask.hdf5'))
universal_mask_file_name = os.path.normpath(os.path.join(data_dir, 'universal_mask.hdf5'))



