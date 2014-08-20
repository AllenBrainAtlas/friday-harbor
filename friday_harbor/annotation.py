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
import numpy as np
import os
import friday_harbor.mhd as mhd

class StructureAnnotation( np.ndarray ):
    ''' 
    StructureAnnotation is just a numpy array with some helpful methods bolted
    on.  You can initialize it with another array as normal, or import
    from hdf5 or mhd.  Also, it takes care of generating index arrays
    for the left and right hemispheres.
    
    '''

    def __new__(cls, input_array):
        ''' This is what numpy says to do if you want to subclass np.ndarray. '''
        obj = np.asarray(input_array).view(cls)
        return obj

    def __array_finalize__(self, obj):
        ''' This is what numpy says to do if you want to subclass np.ndarray. '''
        if obj is None: return

    def __init__(self, input_array):
        ''' 
        The center of the brain is defaulted to the center of the Z axis.  Set this
        yourself after initialization if you like, but before you attempt to
        access the left/right_hemisphere properties.
        
        '''
        super(StructureAnnotation, self).__init__(input_array)

        self.center_index = int(self.shape[2] / 2)
        self._coordinates = None
        self._left_hemisphere = None
        self._right_hemisphere = None

    @staticmethod
    def from_hdf5(file_name):
        ''' import the grid annotation values from an hdf5 file '''
        f = h5py.File(file_name, 'r')
        a = f['grid_annotation'].value
        f.close()

        return StructureAnnotation(a)

    @staticmethod
    def from_mhd(file_name):
        ''' import the grid annotation values from a meta image file '''
        info, values = mhd.read(file_name)
        return StructureAnnotation(values)

    @property
    def coordinates(self):
        ''' Generate XYZ coordinates for the input array using meshgrid. '''
        if self._coordinates is None:
            s = self.shape
            self._coordinates = np.meshgrid(range(s[0]), range(s[1]), range(s[2]), indexing='ij')        

        return self._coordinates

    @property
    def XX(self):
        ''' Get just the X coordinates for the input array. '''   
        return self.coordinates[0]

    @property
    def YY(self):
        ''' Get just the Y coordinates for the input array. '''   
        return self.coordinates[1]

    @property
    def ZZ(self):
        ''' Get just the Z coordinates for the input array. '''   
        return self.coordinates[2]

    @property
    def left_hemisphere(self):
        ''' Get the index list of voxels in the left hemisphere. '''   
        if self._left_hemisphere is None:
            self._left_hemisphere = np.where(self.ZZ < self.center_index)

        return self._left_hemisphere

    @property
    def right_hemisphere(self):
        ''' Get the index list of voxels in the right hemisphere. '''   
        if self._right_hemisphere is None:
            self._right_hemisphere = np.where(self.ZZ >= self.center_index)

        return self._right_hemisphere

