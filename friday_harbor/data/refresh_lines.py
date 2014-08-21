import h5py
from friday_harbor.experiment import ExperimentManager
from friday_harbor.mask import Mask
from friday_harbor.api import target_spatial_search

def refresh_lines(data_dir='.'):
    em = ExperimentManager(data_dir)
    paths = em.paths

    experiment_ids = [ e.id for e in em ]
    brain_mask = Mask.read_from_hdf5(paths.brain_mask_file_name)
    
    for i in xrange(len(brain_mask)):
        x = brain_mask.mask[0][i]
        y = brain_mask.mask[1][i]
        z = brain_mask.mask[2][i]

        target_experiments = target_spatial_search([x,y,z])

        keep_target_experiments = [ te for te in target_experiments if te['id'] in experiment_ids ]
        
        
        return
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        refresh_lines(sys.argv[1])
    else:
        refresh_lines()
