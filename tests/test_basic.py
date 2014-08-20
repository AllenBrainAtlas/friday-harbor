import friday_harbor.structure as structure
import friday_harbor.experiment as experiment

def test_structure_list_length():
    base_ontology = structure.Ontology(data_dir='../friday_harbor/data')
    assert len(base_ontology.structure_list) == 1205
    
def test_experiment_list_length():
 
    experiment_manager = experiment.ExperimentManager(data_dir='../friday_harbor/data')
    assert len(experiment_manager.experiment_list) == 1772
    assert len([e for e in experiment_manager.wildtype()]) == 475

def test_mask():
    experiment_manager = experiment.ExperimentManager(data_dir='../friday_harbor/data')
    e = experiment_manager.experiment_list[1]
    print e.id
    ij = e.injection_mask
    print ij.mask
    print e.density(mask=ij)
        
if __name__ == "__main__":
    test_structure_list_length()
    test_experiment_list_length()
    test_mask()