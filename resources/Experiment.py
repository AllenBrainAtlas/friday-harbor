'''
Created on Jan 25, 2013

@author: nicholasc
'''

import os
import json

# Settings:
json_file_save_dir = '../data/src'
json_file_name = 'experiment_data.json'

# Get data:
f = open(os.path.join(os.path.dirname(__file__), json_file_save_dir, json_file_name))
raw_json = json.load(f)
f.close()

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

    curr_experiment = Experiment(import_dict)
    experiment_list.append(curr_experiment)

#  u'structure-color', u'structure-id', u'sum']

#     structure_list.append(Structure(structure_id, acronym, graph_order, rgb, path_to_root, name))



# # Import important stuff:
# import numpy as np
# import scipy.io as sio
# import Data
# import os
# 
# # Settings:
# rel_data_dir = '../data/src/'
# 
# # Load data:
# path_to_this_file = os.path.dirname(os.path.realpath(__file__))
# data_dir = os.path.join(path_to_this_file, rel_data_dir)
# ISTA = sio.loadmat(data_dir + 'ISTA.mat')['ISTA']
# ISTI = sio.loadmat(data_dir + 'ISTI.mat')['ISTI']
# IS = np.squeeze(sio.loadmat(data_dir + 'IS.mat', struct_as_record=False)['IS'])
# acronym_id_dict = Data.acronym_id_dict
# id_acronym_dict = Data.id_acronym_dict
# 
# # Create the dictionary:
# LIMS_id_primary_secondary_dict = {}
# f = open(data_dir + 'secondary_structure_query.dat','r')
# LIMS_primary_secondary_raw = f.readlines()
# f.close()
# for curr_line in LIMS_primary_secondary_raw[2:-2]:
#     LIMS_as_str, primary_as_str, primary_and_secondary_as_str = [x.strip() for x in curr_line.split('|')]
#     curr_LIMS_id, curr_primary = int(LIMS_as_str), int(primary_as_str)
#     if not curr_LIMS_id in [116903230, 174361040]:
#         primary_and_secondary_list = [int(x) for x in primary_and_secondary_as_str.split('/')]
#     else:
#         primary_and_secondary_list = [curr_primary]
#     curr_secondary_list = list(set(primary_and_secondary_list).difference(set([curr_primary]))) 
#     
#     curr_primary_as_str = id_acronym_dict[curr_primary]
#     curr_secondary_list_as_str = [id_acronym_dict[curr_secondary] for curr_secondary in curr_secondary_list]
#     LIMS_id_primary_secondary_dict[curr_LIMS_id] = [curr_primary_as_str, curr_secondary_list_as_str]
# 
# # Double-check that the structures are valid:
# for curr_lims_id, primary_and_secondary_tuple in LIMS_id_primary_secondary_dict.items():
# #    print curr_lims_id, primary_and_secondary_tuple
#     curr_primary, curr_secondary = primary_and_secondary_tuple    
#     for val in curr_secondary:
#         if val not in acronym_id_dict.keys():
#             print "UHOH 1! %s %s" % (curr_lims_id, val)
#     if curr_primary not in acronym_id_dict.keys():
#         print "UHOH 2! %s %s" % (curr_primary, curr_primary)
# 
# # Double-check that every LIMS from the data is in the dictionary:
# for curr_lims_id in IS:
#     if not curr_lims_id in LIMS_id_primary_secondary_dict.keys():
#         print "UHOH 3! %s" % curr_lims_id
# 
# # Create experiment list:
# experiment_list = []
# for ind in range(len(IS)):
#     LIMS_id = IS[ind]
#     primary_injection_region = str(ISTA[ind].strip())
#     primary_injection_region_id = ISTI[ind][0]
#     secondary_injection_region = [str(x.strip()) for x in LIMS_id_primary_secondary_dict[LIMS_id][1]]
#     secondary_injection_region_id = []
#     for region in secondary_injection_region:
#         secondary_injection_region_id.append(acronym_id_dict[region])
#     experiment_list.append(Experiment(ind, LIMS_id, primary_injection_region, primary_injection_region_id, secondary_injection_region, secondary_injection_region_id))
# 
# # Create a dictionary from LIMS_id to experiment:
# LIMS_id_experiment_dict = {}
# for experiment in experiment_list:
#     LIMS_id_experiment_dict[experiment.LIMS_id] = experiment
    