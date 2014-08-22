from friday_harbor.structure import Ontology
from friday_harbor.mask import Mask
import friday_harbor.experiment as experiment

# Settings:
data_dir = '../friday_harbor/data'
my_structure_acronym = 'VISp' 
my_LIMS_id = 277714322 #100141598

# Initializations:
ontology = Ontology(data_dir=data_dir)
experiment_manager = experiment.ExperimentManager(data_dir=data_dir)

# Grab the particular experiment:
my_experiment = experiment_manager.experiment_by_id(my_LIMS_id)

# Get the injection site mask for this experiment, and assocaited density values:
inj_mask = my_experiment.injection_mask()
inj_mask_as_tuple_list = zip(*inj_mask.mask)
density_vals = my_experiment.density(mask_obj=inj_mask)

# For 
for voxel, density in zip(inj_mask_as_tuple_list, density_vals):
    print voxel, density



