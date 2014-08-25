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
import struct
from friday_harbor.paths import Paths
import numpy as np
import os

class Lines( object ):
    '''
    This class provides some helper methods for breaking into the lines directory.
    '''

    def __init__(self, data_dir='.'):
        '''
        Initialize the paths object.
        '''
        self.paths = Paths(data_dir)

    def by_target_voxel(self, target_voxel):
        '''
        Convert the target voxel to a file name within the lines directory and read it.
        Returns a experiment_id -> experiment dictionary for experiments within the file.
        '''
        coord = [ int(v) * 100 for v in target_voxel ]
        file_name = '%s/%d/%d_%d_%d' % (self.paths.lines_directory, coord[0], coord[0], coord[1], coord[2])
        return read_lines_file(file_name)

    def by_experiment_id(self, experiment_id):
        '''
        Scan through all of the target voxel files for experiments matching
        the input experiment id.  Return a dictionary from voxel -> experiment
        of all matching voxels.
        '''
        experiments = {}
        for root, sub_folders, file_names in os.walk(self.paths.lines_directory):
            for file_name in file_names:
                full_file_name = os.path.join(root, file_name)
                file_experiments = read_lines_file(full_file_name)

                if experiment_id in file_experiments:
                    coord_strings = file_name.split('_')
                    
                    coord = tuple([ int(cs)/100 for cs in coord_strings ])
                    
                    experiments[coord] = file_experiments[experiment_id]

                return experiments

        return experiments


def read_lines_file(file_name):
    '''
    The target search path lines are stored in a custom binary file.  Each file
    contains a list of experiments and the path from each experiment injection
    site to the target voxel.  Also, the projections signal density along the path.

    TODO: take as input an optional experiment id and only read relevant paths.  
    '''

    # give up if the file does not exist
    if not os.path.exists(file_name):
        return {}

    with open(file_name, 'rb') as f:

        # read in the number of experiments
        bytes_read = f.read(struct.calcsize('=I')) # unsigned int
        num_experiments = struct.unpack('=I', bytes_read)[0]

        # This is what each experiment entry looks like
        # struct TargetMapFileHeaderEntry
        # {
        #     unsigned int rowId;
        #     float value;
        #     unsigned int transgenicLineId;
        #     unsigned int fileOffset;
        #     unsigned int numPoints;
        # };

        experiment_fmt = '=IfIII'
        experiment_bytes = struct.calcsize(experiment_fmt)

        # This s what each point looks like 
        # struct StreamTracePoint3d
        # {
        #     float	coord[3];
        #     float	density, intensity;
        # };

        point_fmt = '=fffff'
        point_bytes = struct.calcsize(point_fmt)

        # read in the experiment list
        experiment_list = []
        experiments = {}

        for i in xrange(num_experiments):

            # read the header entry
            bytes_read = f.read(experiment_bytes)
            row_id, value, transgenic_line_id, file_offset, num_points = struct.unpack(experiment_fmt, bytes_read)

            experiment = {
                'row_id': row_id, 
                'value': value, 
                'transgenic_line_id': transgenic_line_id, 
                'file_offset': file_offset, 
                'num_points': num_points,
                'path': np.zeros([num_points, 3], dtype=np.uint16),
                'density': np.zeros([num_points], dtype=np.float16)
            }

            experiment_list.append(experiment)
            experiments[experiment['row_id']] = experiment

        # now read in the paths for each experiment
        for experiment in experiment_list:

            # read in one point at a time
            for i in xrange(experiment['num_points']):
                bytes_read = f.read(point_bytes)
                x,y,z,density,intensity = struct.unpack(point_fmt, bytes_read)
                            
                experiment['path'][i] = np.array([x,y,z])
                experiment['density'][i] = density

    return experiments
                        
                             

                
            
                
