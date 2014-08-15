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

import os
import json
import h5py
from resources.Mask import Mask 

# Settings:
JSON_FILE_SAVE_DIR = os.path.join(os.path.dirname(__file__), '../data/src')
RAW_DATA_FILE_SAVE_DIR = os.path.join(os.path.dirname(__file__), '../data/src/raw_data')
JSON_FILE_NAME = 'experiment_data.json'
INJECTION_MASK_FILE_NAME = os.path.join(os.path.dirname(__file__), '../data/src/injection_masks.hdf5')
INJECTION_MASK_FILE_NAME_SHELL = os.path.join(os.path.dirname(__file__), '../data/src/injection_masks_shell.hdf5')

# Useful function:
def read_dictionary_from_h5_group(group):
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
        d = read_dictionary_from_h5_group(f)
        f.close()
        
        if mask_obj != None:
            return {'injection':d['injection'][mask_obj.mask], 'density':d['density'][mask_obj.mask]}
        else:
            return d
        
    def get_injection(self):
        return self.load_hdf5()['injection']
    
    @property
    def mask(self):
        return Experiment.get_injection_mask(self.id)
        
    @staticmethod
    def get_injection_mask(LIMS_id, shell=False):
        
        if shell == False:
            return Mask.read_from_hdf5(INJECTION_MASK_FILE_NAME, subgroup=str(LIMS_id))
        elif shell == True:
            return Mask.read_from_hdf5(INJECTION_MASK_FILE_NAME_SHELL, subgroup=str(LIMS_id))
        else:
            raise Exception
    
    @staticmethod
    def get_injection_mask_inverse(LIMS_id):
        return Mask.read_from_hdf5(INJECTION_MASK_FILE_NAME, subgroup='%s_inverse' % str(LIMS_id))
        
def experiment_lists():
    # Get data:
    f = open(os.path.join(os.path.dirname(__file__), JSON_FILE_SAVE_DIR, JSON_FILE_NAME))
    raw_json = json.load(f)
    f.close()

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

        import_dict['data_file_name'] = os.path.join(RAW_DATA_FILE_SAVE_DIR, str(import_dict['id']),'density_energy_injection_%s.hdf5' % import_dict['id'])

        if import_dict['strain'] == 'C57BL/6J':
            import_dict['wildtype'] = True 
        else:
            import_dict['wildtype'] = False

        curr_experiment = Experiment(import_dict)
        experiment_list.append(curr_experiment)

    LIMS_id_experiment_dict = {}
    for e in experiment_list:
        LIMS_id_experiment_dict[e.id] = e

    return {
        'all': [ e.id for e in experiment_list],
        'wildtype': [ e.id for e in experiment_list if e.wildtype == True ]
    }

