'''
Created on Jan 25, 2013

@author: nicholasc
'''

import os
import json
import h5py
from resources.Mask import Mask 

# Settings:
json_file_save_dir = os.path.join(os.path.dirname(__file__), '../data/src')
raw_data_file_save_dir = os.path.join(os.path.dirname(__file__), '../data/src/raw_data')
json_file_name = 'experiment_data.json'
injection_mask_file_name = os.path.join(os.path.dirname(__file__), '../data/src/injection_masks.hdf5')

# Get data:
f = open(os.path.join(os.path.dirname(__file__), json_file_save_dir, json_file_name))
raw_json = json.load(f)
f.close()

# Useful function:
def read_dictionary_from_group(group):
    dictionary = {}
    for name in group:
        dictionary[str(name)] = group[name].value
        
    return dictionary

class Experiment(object):
    '''
    classdocs
    '''


    def __init__(self, import_dict):
        '''
        Constructor
        '''
        
        for key, val in import_dict.items():
            setattr(self, key, val)
            
    def load_hdf5(self, mask_obj=None):
        
        f = h5py.File(self.data_file_name, 'r')
        d = read_dictionary_from_group(f)
        f.close()
        
        if mask_obj != None:
            return {'injection':d['injection'][mask_obj.mask], 'density':d['density'][mask_obj.mask]}
        else:
            return d
        
    @staticmethod
    def get_injection_mask(LIMS_id):
        return Mask.read_from_hdf5(injection_mask_file_name, subgroup=str(LIMS_id))
    
    @staticmethod
    def get_injection_mask_inverse(LIMS_id):
        return Mask.read_from_hdf5(injection_mask_file_name, subgroup='%s_inverse' % str(LIMS_id))

# Create experiment list:
experiment_list = []
for e_dict in raw_json['msg']:
    
    import_dict = {}
    import_dict['num_voxels'] = int(e_dict['num-voxels'])
    import_dict['name'] = str(e_dict['name'])
    import_dict['structure_name'] = str(e_dict['structure-name'])
    import_dict['transgenic_line'] = str(e_dict['transgenic-line'])
    import_dict['gender'] = str(e_dict['gender'])
    import_dict['injection_volume'] = float(e_dict['injection-volume'])
    import_dict['structure_abbrev'] = str(e_dict['structure-abbrev'])
    import_dict['id'] = int(e_dict['id'])
    import_dict['strain'] = str(e_dict['strain'])
    import_dict['injection_coordinates'] = e_dict['injection-coordinates']

    
    # Special case, injection structures:
    injection_structures_list = e_dict['injection-structures']
    injection_structures_acronym_list = []
    for s in injection_structures_list:
        if s['abbreviation'] == 'SUM ':
            curr_acronym = 'SUM'
        else:
            curr_acronym = str(s['abbreviation'])
        injection_structures_acronym_list.append(curr_acronym)
    import_dict['injection_structures_acronym_list'] = injection_structures_acronym_list 

    import_dict['structure_color'] = str(e_dict['structure-color'])
    import_dict['structure_id'] = int(e_dict['structure-id'])
    import_dict['sum'] = float(e_dict['sum'])

    import_dict['data_file_name'] = os.path.join(raw_data_file_save_dir, str(import_dict['id']),'density_injection_%s.hdf5' % import_dict['id'])

    curr_experiment = Experiment(import_dict)
    experiment_list.append(curr_experiment)
    