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