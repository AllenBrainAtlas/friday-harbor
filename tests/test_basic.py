
def test_structure_list_length():

    from resources.Structure import Ontology
    base_ontology = Ontology()
    
    assert len(base_ontology.structure_list) == 1205
    
# def test_experiment_list_length():
# 
#     from resources.Experiment import all_experiment_LIMS_list, wildtype_experiment_LIMS_list
#     assert len(all_experiment_LIMS_list) == 1772
#     assert len(wildtype_experiment_LIMS_list) == 475


        
if __name__ == "__main__":
    test_structure_list_length()
#     test_experiment_list_length()