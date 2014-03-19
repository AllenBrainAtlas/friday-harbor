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

class Annotation(np.ndarray):
    
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return

# Structure annotation:
f = h5py.File(os.path.join(os.path.dirname(__file__), '../data/src/grid_annotation/gridAnnotation.hdf5'), 'r')
structure_annotation = Annotation(f['grid_annotation'].value)
f.close()

# X-coordinates:
XX = Annotation(np.zeros(np.shape(structure_annotation)))
for ii in range(np.shape(structure_annotation)[0]):
    XX[ii,:,:] = ii
    
# Y-coordinates:
YY = Annotation(np.zeros(np.shape(structure_annotation)))
for ii in range(np.shape(structure_annotation)[1]):
    YY[:,ii,:] = ii
    
# Z-coordinates:
ZZ = Annotation(np.zeros(np.shape(structure_annotation)))
for ii in range(np.shape(structure_annotation)[2]):
    ZZ[:,:,::] = ii
    
# Hemisphere annotation:
center_ind = 57
hemisphere_annotation = Annotation(np.zeros(np.shape(structure_annotation), dtype=str))
for ii in np.arange(0,center_ind):
    hemisphere_annotation[:,:,ii] = 'L'
for ii in np.arange(center_ind+1,np.shape(structure_annotation)[2]):
    hemisphere_annotation[:,:,ii] = 'R'
hemisphere_annotation[:,:,center_ind] = 'R'

# All zero annotation:
all_zero = Annotation(np.zeros(np.shape(structure_annotation)))


    
