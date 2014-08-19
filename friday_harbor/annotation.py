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
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __init__(self, input_array):
        super(StructureAnnotation, self).__init__(input_array)

        self.center_index = int(self.shape[2] / 2)
        self._coordinates = None
        self._left_hemisphere = None
        self._right_hemisphere = None

    def __array_finalize__(self, obj):
        if obj is None: return

    @staticmethod
    def from_hdf5(file_name):
        f = h5py.File(file_name, 'r')
        a = f['grid_annotation'].value
        f.close()

        return StructureAnnotation(a)

    @staticmethod
    def from_mhd(file_name):
        info, values = mhd.read(file_name)
        return StructureAnnotation(values)

    @property
    def coordinates(self):
        if self._coordinates is None:
            s = self.shape
            self._coordinates = np.meshgrid(range(s[0]), range(s[1]), range(s[2]), indexing='ij')        

        return self._coordinates

    @property
    def XX(self):
        return self.coordinates[0]

    @property
    def YY(self):
        return self.coordinates[1]

    @property
    def ZZ(self):
        return self.coordinates[2]

    @property
    def left_hemisphere(self):
        if self._left_hemisphere is None:
            self._left_hemisphere = np.where(self.ZZ < self.center_index)

        return self._left_hemisphere

    @property
    def right_hemisphere(self):
        if self._right_hemisphere is None:
            self._right_hemisphere = np.where(self.ZZ >= self.center_index)

        return self._right_hemisphere

