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
from friday_harbor.experiment_manager import ExperimentManager

def pickle(data, file_name):
    
    f = open( file_name, "wb" )
    pkl.dump(data, f)
    f.close()

def unpickle(file_name):
    
    f = open( file_name, "rb" )
    data = pkl.load(f)
    f.close()
    
    return data

def get_density_from_experiment_id(experiment_id, zero_invalid_data=True):
    m = ExperimentManager()

    density_vals = m.experiment_by_id(experiment_id).density

    if zero_invalid_data:
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
