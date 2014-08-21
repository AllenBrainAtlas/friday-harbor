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
from friday_harbor.mask import Mask 
from friday_harbor.paths import Paths

class Experiment(object):
    '''
    Experiment imports metadata from a data downloaded from the Allen Institute API
    and provides support methods for extracting density, injection, and other 
    arrays from hdf5 files downloaded via friday_harbor.data scripts.
    
    '''

    @staticmethod
    def from_json(e_dict, paths):
        '''
        Take a dictionary, which is expected to contain the fields resulting from
        a json import of API-downloaded experiment metadata, sanitize the keys and 
        data types, and create an Experiment instance.
        '''
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

        return Experiment(paths, **import_dict)

    def __init__(self, paths, **kwargs):
        '''
        A fairly generic Experiment constructor.  The Experiment needs a 
        friday_harbor.paths.Paths instance so it knows where the relevant 
        hdf5 files live.  
        The rest of the properties of the experiment are initialized from keyword 
        arguments.  Note that this can be rather dangerous, since it's
        easy for property names to accidentally collide.
        
        '''
        self.paths = paths

        for key, val in kwargs.iteritems():
            setattr(self, key, val)
        
    def injection(self, mask_obj=None):
        ''' Extract the injection volume voxel data from the hdf5 file if it exists. '''
        f = h5py.File(self.paths.injection_volumes_file_name, 'r')
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

    def density(self, mask_obj=None):
        ''' Extract the density volume voxel data from the hdf5 file if it exists. '''
        f = h5py.File(self.paths.projection_densities_file_name, 'r')

        try:
            vals = f[str(self.id)].value
        except KeyError as e:
            f.close()
            raise e

        f.close()

        if mask_obj:
            return vals[mask_obj.mask]
        else:
            return vals
        
    def injection_mask(self, shell=False):
        ''' Extract the injection mask from the hdf5 file if it exists. '''        
        if shell == False:
            return Mask.read_from_hdf5(self.paths.injection_masks_file_name, subgroup=str(self.id))
        else:
            return Mask.read_from_hdf5(self.paths.injection_masks_shell_file_name, subgroup=str(self.id))
    
#     @property
#     def injection_mask_inverse(self):
#         ''' Extract the injection mask inverse from the hdf5 file if it exists. '''        
#         return Mask.read_from_hdf5(self.paths.injection_masks_file_name, subgroup='%s_inverse' % str(self.id))

class ExperimentManager( object ):
    '''
    ExperimentManager is a light wrapper around a list of Experiments that
    provides some simple filtering methods for extracting experiment subsets
    (wild type, cre, etc).
    
    '''

    def __init__(self, data_dir=None):

        self.paths = Paths(data_dir)
        experiment_json_file_name = self.paths.experiment_json_file_name
        raw_data_dir = self.paths.experiment_raw_data_directory
            
        self.experiment_list = []

        # Get data:
        with open(experiment_json_file_name) as f:
            experiment_data = json.load(f)

            self.experiment_list = [ Experiment.from_json(d, self.paths) for d in experiment_data['msg'] ]

        self.experiments_by_id = { e.id: e for e in self.experiment_list }

    def all(self):
        ''' Return the entire list of experiments. '''
        return self.experiment_list

    def wildtype(self):
        ''' Return a generator for just the wild type experiments. '''
        return ( e for e in self.experiment_list if e.wildtype == True )

    def cre(self):
        ''' Return a generator for just the cre experiments. '''
        return ( e for e in self.experiment_list if e.wildtype == False )

    def cortex(self):
        ''' Return a generator for just the cortical injections. '''
        return ( e for e in self.experiment_list if 315 in e.path_to_root )

    def noncortex(self):
        ''' Return a generator for just the cortical injections. '''
        return ( e for e in self.experiment_list if not (315 in e.path_to_root) )
        
    def experiment_by_id(self, experiment_id):
        ''' Get a handle to an experiment by its id. '''
        return self.experiments_by_id[experiment_id]

    def __iter__(self):
        ''' By default, iterating over the manager will iterate through all of the experiments. '''
        return iter(self.experiment_list)

