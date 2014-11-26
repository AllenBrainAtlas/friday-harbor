from friday_harbor.mask import Mask
from friday_harbor.structure import Structure
from friday_harbor.paths import Paths
import json

class Ontology(object):
    def __init__(self, data_dir='.'):
        self.paths = Paths(data_dir)
        file_name = self.paths.structure_json_file_name

        # Get data:
        self.structure_list = []
        with open(file_name) as f:
            structure_data = json.load(f)
            self.structure_list = [ Structure.from_json(d) for d in structure_data]

        # Set child list:
        for s in self.structure_list:
            s.child_list = [s2 for s2 in self.structure_list if s2.is_child_of(s)]
 
        # Create easy_access dictionaries:
        self.id_structure_dict = {}
        self.acronym_structure_dict = {}
        self.id_acronym_dict = {}
        self.acronym_id_dict = {}
        for s in self.structure_list:
            self.id_structure_dict[s.structure_id] = s
            self.acronym_structure_dict[s.acronym] = s
            self.id_acronym_dict[s.structure_id] = s.acronym
            self.acronym_id_dict[s.acronym] = s.structure_id

    def get_mask(self, structure_id, hemisphere='both'):
        curr_acronym = self.id_acronym_dict[structure_id]
        if hemisphere == 'both':
            return Mask.read_from_hdf5(self.paths.structure_masks_file_name, subgroup='%s_nonzero' % curr_acronym)
        elif hemisphere == 'left':
            return Mask.read_from_hdf5(self.paths.structure_masks_file_name, subgroup='%s_left_nonzero' % curr_acronym)
        elif hemisphere == 'right':
            return Mask.read_from_hdf5(self.paths.structure_masks_file_name, subgroup='%s_right_nonzero' % curr_acronym)
        else:
            raise ValueError

    def structure_by_id(self, structure_id):
        return self.id_structure_dict[structure_id]
    
    def structure_by_acronym(self, acronym):
        return self.acronym_structure_dict[acronym]

    def __iter__(self):
        return iter(self.structure_list)