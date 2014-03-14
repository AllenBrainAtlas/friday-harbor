import h5py
import os
import numpy as np
from resources.utilities import extract_volume
from resources.hdf5_tools import write_dictionary_to_group, read_dictionary_from_group

# Settings:
raw_data_dir = '../src/raw_data'
save_file_name_prefix = 'density_injection'

# Extract volumes of PD and injection sites:
for curr_LIMS_id in os.listdir(raw_data_dir):
    curr_dir = os.path.join(raw_data_dir, curr_LIMS_id)
    
    _, arr_density, _ = extract_volume(curr_dir, 'density', dtype = np.float32)
    _, arr_injection, _ = extract_volume(curr_dir, 'injection', dtype = np.float32)
    
    print np.shape(arr_density)
    
    save_file_name = os.path.join(curr_dir, '%s_%s.hdf5' % (save_file_name_prefix, curr_LIMS_id))

    f = h5py.File(save_file_name, 'w')
    write_dictionary_to_group(f, {'density':arr_density, 'injection':arr_injection})
    f.close()
    