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
from friday_harbor.mask import Mask

class Lines( object ):
    '''
    This class provides some helper methods for breaking into the lines directory.
    '''

    def __init__(self, data_dir='.'):
        '''
        Initialize the paths object.
        '''
        self.paths = Paths(data_dir)

    def by_target_voxel(self, target_voxel, experiment_ids=None):
        '''
        Convert the target voxel to a file name within the lines directory and read it.
        Returns a experiment_id -> experiment dictionary for experiments within the file.
        If you want to restrict your results to a particular set of experiment ids, 
        supply an array of experiment_ids.
        '''
        coord = [ int(v) * 100 for v in target_voxel ]
        file_name = '%s/%d/%d_%d_%d' % (self.paths.lines_directory, coord[0], coord[0], coord[1], coord[2])
        return read_lines_file(file_name, experiment_ids)

    def by_experiment_id(self, experiment_id, mask=None):
        '''
        Scan through all of the target voxel files for experiments matching
        the input experiment id.  Return a dictionary from voxel -> experiment
        of all matching voxels.
        '''
        if mask is None:
            print "WARNING: Lines.by_experiment_id is incredibly slow. Use it sparingly, and when " + \
                "you do, consider restricting your search to a voxel mask."
            mask = Mask.read_from_hdf5(self.paths.brain_mask_file_name)

        # build up a set of unique voxels in this mask
        voxels = []
        for i in xrange(len(mask)):
            x = int(mask.mask[0][i] * 100)
            y = int(mask.mask[1][i] * 100)
            z = int(mask.mask[2][i] * 100)

            voxels.append((x,y,z))
        
        root = self.paths.lines_directory
        experiments = {}
   
        num_voxels = len(voxels)
        for i,voxel in enumerate(voxels):
            if i % 100 == 0:
                print "%d/%d voxels searched" % (i, num_voxels)

            file_name = os.path.join(root, str(voxel[0]), '%d_%d_%d' % (voxel[0], voxel[1], voxel[2]))
            file_experiments = read_lines_file(file_name, experiment_ids=[experiment_id])

            # there should only be one experiment here, since there is only one experiment input
            for file_experiment in file_experiments.iteritems():
                experiments[voxel] = file_experiment

        return experiments


def read_lines_file(file_name, experiment_ids=None):  
    '''
    The target search path lines are stored in a custom binary file.  Each file
    contains a list of experiments and the path from each experiment injection
    site to the target voxel.  Also, the projections signal density along the path.
    '''

    # give up if the file does not exist
    if not os.path.exists(file_name):
        return {}

    with open(file_name, 'rb') as f:

        header_size = 0

        # read in the number of experiments
        uintsize = struct.calcsize('=I')
        header_size += uintsize

        bytes_read = f.read(uintsize) # unsigned int
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

        for i in xrange(num_experiments):

            # read the header entry
            bytes_read = f.read(experiment_bytes)
            row_id, value, transgenic_line_id, file_offset, num_points = struct.unpack(experiment_fmt, bytes_read)
            header_size += experiment_bytes

            experiment_list.append({
                'experiment_id': row_id, 
                'value': value, 
                'transgenic_line_id': transgenic_line_id, 
                'file_offset': file_offset, 
                'num_points': num_points,
                'path': np.zeros([num_points, 3], dtype=np.uint16),
                'density': np.zeros([num_points], dtype=np.float16)
            })

        # if we're looking for particular experiments, filter to just those
        if experiment_ids is not None:
            experiment_list = [ e for e in experiment_list if e['experiment_id'] in experiment_ids ]

        # loop through the experiments we care about and read in the paths
        for experiment in experiment_list:

            # seek to the correct position in the file for this experiment
            f.seek(header_size + experiment['file_offset'], 0)

            # read in one point at a time
            for i in xrange(experiment['num_points']):
                bytes_read = f.read(point_bytes)
                x,y,z,density,intensity = struct.unpack(point_fmt, bytes_read)
                
                experiment['path'][i] = np.array([x,y,z])
                experiment['density'][i] = density
        
    return { e['experiment_id']: e for e in experiment_list }
                        
                             

                
            
                
