import friday_harbor.structure as structure
import friday_harbor.experiment as experiment
import friday_harbor.mask as mask
import numpy as np

def test_structure_list_length():
    base_ontology = structure.Ontology(data_dir='../friday_harbor/data')
    print len(base_ontology.structure_list)
    assert len(base_ontology.structure_list) == 1205
    
def test_experiment_list_length():
 
    experiment_manager = experiment.ExperimentManager(data_dir='../friday_harbor/data')
    assert len(experiment_manager.experiment_list) == 1772
    assert len([e for e in experiment_manager.wildtype()]) == 475

def test_mask():
    experiment_manager = experiment.ExperimentManager(data_dir='../friday_harbor/data')
    e = experiment_manager.experiments_by_id[180436360]
    assert e.density(mask_obj=e.injection_mask()).sum() == 2289.300048828125
    
def test_union():
    
    def union(m1, m2):
        
        if len(m1) == 0 and len(m2) == 0:
            xx, yy, zz = np.array([]), np.array([]), np.array([])
        elif len(m1) == 0:
            return m2
        elif len(m2) == 0:
            return m1
        else:
        
            m1_set = set(zip(*m1.mask))
            m2_set = set(zip(*m2.mask))
            
            union_set = m1_set.union(m2_set)
            xx, yy, zz = zip(*list(union_set))
            
        return np.array(xx), np.array(yy), np.array(zz)
    
    ontology = structure.Ontology(data_dir='../friday_harbor/data')
    LGd_id = ontology.acronym_id_dict['LGd']
    VISp_id = ontology.acronym_id_dict['VISp']
    LGd_mask = ontology.get_mask_from_id_left_hemisphere_nonzero(LGd_id)
    VISp_mask = ontology.get_mask_from_id_right_hemisphere_nonzero(VISp_id)
    for ii in range(2):
        list_1 = sorted(union(LGd_mask, VISp_mask)[ii])
        list_2 = sorted(mask.Mask.union(LGd_mask, VISp_mask).mask[ii])
        assert list_1 == list_2
        
def test_intersection():
    
    def intersection(m1, m2):
        
        if len(m1) == 0 or len(m2) == 0:
            xx, yy, zz = np.array([]), np.array([]), np.array([])
            
        else:
            m1_set = set(zip(*m1.mask))
            m2_set = set(zip(*m2.mask))
            
            intersection_set = m1_set.intersection(m2_set) 
            if len(intersection_set) == 0:
                xx, yy, zz = np.array([]), np.array([]), np.array([])
            else:
                xx, yy, zz = zip(*list(intersection_set))
            
        return (np.array(xx), np.array(yy), np.array(zz))

    ontology = structure.Ontology(data_dir='../friday_harbor/data')
    VIS_id = ontology.acronym_id_dict['VIS']
    VISp_id = ontology.acronym_id_dict['VISp']
    VIS_mask = ontology.get_mask_from_id_left_hemisphere_nonzero(VIS_id)
    VISp_mask = ontology.get_mask_from_id_left_hemisphere_nonzero(VISp_id)
    for ii in range(2):
        list_1 = sorted(intersection(VIS_mask, VISp_mask)[ii])
        list_2 = sorted(mask.Mask.intersection(VIS_mask, VISp_mask).mask[ii])
        assert list_1 == list_2

def test_structure():
    ontology = structure.Ontology(data_dir='../friday_harbor/data')
    LGd_id = ontology.acronym_id_dict['LGd']
    LGd_mask = ontology.get_mask_from_id_left_hemisphere_nonzero(LGd_id)


#     MOp_structure
        
if __name__ == "__main__":
    test_structure_list_length()
    test_experiment_list_length()
    test_mask()
    test_union()
    test_intersection()
    test_structure()