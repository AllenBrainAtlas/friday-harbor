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

import friday_harbor.structure as structure
import friday_harbor.experiment as experiment
import friday_harbor.mask as mask
import numpy as np

def test_structure_list_length():
    base_ontology = structure.Ontology(data_dir='../friday_harbor/data')
    assert len(base_ontology.structure_list) == 1205
    
def test_experiment_list_length():
 
    experiment_manager = experiment.ExperimentManager(data_dir='../friday_harbor/data')
    assert len(experiment_manager.experiment_list) == 1772
    assert len([e for e in experiment_manager.wildtype()]) == 469

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
    assert LGd_mask.mask[0].sum() + LGd_mask.mask[0].sum() + LGd_mask.mask[0].sum() == 70176
    
    LGd_mask = ontology.get_mask_from_id_nonzero(LGd_id)
    assert LGd_mask.mask[0].sum() + LGd_mask.mask[0].sum() + LGd_mask.mask[0].sum() == 140067
    LGd_mask = ontology.get_mask_from_id_right_hemisphere_nonzero(LGd_id)
    assert LGd_mask.mask[0].sum() + LGd_mask.mask[0].sum() + LGd_mask.mask[0].sum() == 69891

def test_centroid():
    
    ontology = structure.Ontology(data_dir='../friday_harbor/data')
    MOp_id = ontology.acronym_id_dict['MOp']
    MOp_mask = ontology.get_mask_from_id_nonzero(MOp_id)
    assert tuple(map(int,MOp_mask.centroid)) == (43, 21, 56)
    
def test_cortex():
    experiment_manager = experiment.ExperimentManager(data_dir='../friday_harbor/data')
    assert len([e for e in experiment_manager.cortex()]) == 648
    
def test_noncortex():
    experiment_manager = experiment.ExperimentManager(data_dir='../friday_harbor/data')
    assert len([e for e in experiment_manager.noncortex()]) == 1124
        
if __name__ == "__main__":
    test_structure_list_length()
    test_experiment_list_length()
    test_mask()
    test_union()
    test_intersection()
    test_structure()
    test_centroid()
    test_cortex()
    test_noncortex()
