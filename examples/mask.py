from friday_harbor.structure import Ontology
from friday_harbor.mask import Mask
import friday_harbor.experiment as experiment

# Settings:
data_dir = '../friday_harbor/data'
my_structure_acronym = 'VISp' 
my_LIMS_id = 100141598

# Initializations:
ontology = Ontology(data_dir=data_dir)
experiment_manager = experiment.ExperimentManager(data_dir=data_dir)

# Grab the particular experiment:
my_experiment = experiment_manager.experiment_by_id(my_LIMS_id)

# Get the injection site mask for this experiment:
inj_mask = my_experiment.injection_mask()

# Print the integrated density for the injection site:
print my_experiment.density(mask_obj=inj_mask)

# Get the mask and use it to compute

#     curr_id = ontology.acronym_id_dict[a]
#     m_left = ontology.get_mask_from_id_left_hemisphere_nonzero(curr_id)
#     m_right = ontology.get_mask_from_id_right_hemisphere_nonzero(curr_id)
#     m_all = ontology.get_mask_from_id_nonzero(curr_id)
#     print '%4s:' % a,  m_left.centroid, m_right.centroid, m_all.centroid

