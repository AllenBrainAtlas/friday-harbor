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
import resources.paths as paths

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

    @staticmethod
    def from_json(e_dict, raw_data_dir):
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
        
        if import_dict['strain'] == 'C57BL/6J':
            import_dict['wildtype'] = True 
        else:
            import_dict['wildtype'] = False

        return Experiment(**import_dict)

    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        for key, val in kwargs.iteritems():
            setattr(self, key, val)
        
    @property
    def injection(self, mask_obj=None):
        f = h5py.File(paths.injection_volumes_file_name, 'r')
        try:
            vals = f[str(self.id)].value
        except KeyError as e:
            f.close()
            raise e

        f.close()

        if mask_obj:
            return vals[mask_obj]
        else:
            return vals

    @property
    def density(self, mask_obj=None):
        f = h5py.File(paths.injection_densities_file_name, 'r')

        try:
            vals = f[str(self.id)].value
        except KeyError as e:
            f.close()
            raise e

        f.close()

        if mask_obj:
            return vals[mask_obj]
        else:
            return vals
        
    @property
    def injection_mask(self, shell=False):
        if shell:
            return Mask.read_from_hdf5(paths.injection_masks_file_name, subgroup=str(self.id))
        else:
            return Mask.read_from_hdf5(paths.injection_masks_shell_file_name, subgroup=str(self.id))
    
    @property
    def injection_mask_inverse(self):
        return Mask.read_from_hdf5(paths.injection_masks_file_name, subgroup='%s_inverse' % str(self.id))

class ExperimentManager( object ):
    def __init__(self, experiment_json_file_name=None, raw_data_dir=None):
        if experiment_json_file_name is None:
            experiment_json_file_name = paths.experiment_json_file_name

        if raw_data_dir is None:
            raw_data_dir = paths.experiment_raw_data_directory
            
        self.experiment_list = []

        # Get data:
        with open(experiment_json_file_name) as f:
            raw_json = json.load(f)

            self.experiment_list = [ Experiment.from_json(d, raw_data_dir) for d in raw_json['msg'] ]

        self.experiments_by_id = { e.id: e for e in self.experiment_list }

    def all(self):
        return self.experiment_list

    def wildtype(self):
        return ( e for e in experiment_list if e.wildtype == True )

    def cre(self):
        return ( e for e in experiment_list if e.wildtype == False )
        
    def experiment_by_id(self, experiment_id):
        return self.experiments_by_id[experiment_id]

    def __iter__(self):
        return iter(self.experiment_list)

