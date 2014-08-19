import os

class Paths( object ):
    def __init__(self, data_dir='.'):
        self.data_dir = data_dir
        
        self.experiment_raw_data_directory = os.path.normpath(os.path.join(self.data_dir, 'raw_data'))
        
        self.structure_json_file_name = os.path.normpath(os.path.join(self.data_dir, 'structure_data.json'))
        self.experiment_json_file_name = os.path.normpath(os.path.join(self.data_dir, 'experiment_data.json'))

        self.structure_annotation_file_name = os.path.normpath(os.path.join(self.data_dir, 'grid_annotation.hdf5'))
        self.structure_masks_file_name = os.path.normpath(os.path.join(self.data_dir, 'structure_masks.hdf5'))

        self.injection_volumes_file_name = os.path.normpath(os.path.join(self.data_dir, 'injection_volumes.hdf5'))
        self.injection_masks_file_name = os.path.normpath(os.path.join(self.data_dir, 'injection_masks.hdf5'))
        self.injection_masks_shell_file_name = os.path.normpath(os.path.join(self.data_dir, 'injection_masks_shell.hdf5'))
        self.projection_densities_file_name = os.path.normpath(os.path.join(self.data_dir, 'projection_density.hdf5'))

        self.left_hemisphere_mask_file_name = os.path.normpath(os.path.join(self.data_dir, 'left_hemisphere_mask.hdf5'))
        self.left_hemisphere_nonzero_mask_file_name = os.path.normpath(os.path.join(self.data_dir, 'left_hemisphere_nonzero_mask.hdf5'))

        self.right_hemisphere_mask_file_name = os.path.normpath(os.path.join(self.data_dir, 'right_hemisphere_mask.hdf5'))
        self.right_hemisphere_nonzero_mask_file_name = os.path.normpath(os.path.join(self.data_dir, 'right_hemisphere_nonzero_mask.hdf5'))

        self.brain_mask_file_name = os.path.normpath(os.path.join(self.data_dir, 'brain_mask.hdf5'))
        self.universal_mask_file_name = os.path.normpath(os.path.join(self.data_dir, 'universal_mask.hdf5'))



