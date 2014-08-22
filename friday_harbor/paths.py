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

        self.lines_directory = os.path.normpath(os.path.join(self.data_dir, 'lines'))



