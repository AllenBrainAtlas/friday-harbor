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

import pickle as pkl
import os
import numpy as np
import re
import h5py

def pickle(data, file_name):
    
    f = open( file_name, "wb" )
    pkl.dump(data, f)
    f.close()

def unpickle(file_name):
    
    f = open( file_name, "rb" )
    data = pkl.load(f)
    f.close()
    
    return data

def extract_volume(load_dir, file_name_prefix, dtype):

    f = open(os.path.join(load_dir, file_name_prefix) + '.mhd', 'r')
    header = f.read()
    f.close()
    f = open(os.path.join(load_dir, file_name_prefix) + '.raw', 'r')
    raw = f.read()
    f.close()

    arr = np.frombuffer(raw, dtype=dtype)

    # parse the meta image header.  each line should be a 'key = value' pair.
    metaLines = header.split('\n')
    metaInfo = dict(line.split(' = ') for line in metaLines if line)

    # convert values to numeric types as appropriate
    for k,v in metaInfo.iteritems():
        if re.match("^[\d\s]+$",v):
            nums = v.split(' ')
            if len(nums) > 1:
                metaInfo[k] = map(float, v.split(' '))
            else:
                metaInfo[k] = int(nums[0])

    # reshape the array to the appropriate dimensions.  Note the use of the fortran column ordering.
    arr = arr.reshape(metaInfo['DimSize'], order='F')
    
    return (header,arr,metaInfo)

def get_density_from_LIMS_id(LIMS_id):
    
    # Create injection masks:
    f_proj = h5py.File(os.path.join(os.path.dirname(__file__),'../data/src/projection_density.hdf5'), 'r')
    density_vals = f_proj[str(LIMS_id)].value
    f_proj.close()
    
    density_vals[np.where(density_vals < 0)] = 0
    
    return density_vals

def write_dictionary_to_group(group, dictionary, create_name = None):
    
    if create_name != None:
        group = group.create_group(create_name)
    for key, val in dictionary.items():
        group[str(key)] = val
    
    return

def read_dictionary_from_group(group):
    
    dictionary = {}
    for name in group:
        dictionary[str(name)] = group[name].value
        
    return dictionary

def seconds_to_str(t):
    rediv = lambda ll,b : list(divmod(ll[0],b)) + ll[1:]
    return "%d:%02d:%02d.%03d" % tuple(reduce(rediv,[[t*1000,],1000,60,60]))