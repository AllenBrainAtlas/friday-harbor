import h5py
import numpy as np
from friday_harbor.experiment import ExperimentManager
from friday_harbor.mask import Mask
from friday_harbor.api import target_spatial_search

def refresh_lines(data_dir='.'):
    '''
    This will download lines into an hdf5. 
    NOTE: methods in friday_harbor.lines access the lines in a custom binary format,
    NOT the hdf5 files downloaded here.  
    '''
    em = ExperimentManager(data_dir)
    paths = em.paths

    experiment_ids = [ e.id for e in em ]
    brain_mask = Mask.read_from_hdf5(paths.brain_mask_file_name)

    lines_f = h5py.File(paths.lines_file_name, 'w')

    for i in xrange(len(brain_mask)):
        x = brain_mask.mask[0][i]
        y = brain_mask.mask[1][i]
        z = brain_mask.mask[2][i]

        target_experiments = target_spatial_search([x,y,z])

        if target_experiments is None or len(target_experiments) == 0:
            continue

        keep_target_experiments = [ te for te in target_experiments if te['id'] in experiment_ids ]
        
        for keep_e in keep_target_experiments:
            coords = np.array([p['coord'] for p in keep_e['path']]) / 100.0 # 
            densities = np.array([p['density'] for p in keep_e['path']])

            group = '/%d/%d/%d/%d' % (x,y,z,keep_e['id'])
            dgroup = group+'/density'
            cgroup = group+'/path'
            
            print group

            lines_f.create_dataset(dgroup, data=densities)
            lines_f.create_dataset(cgroup, data=coords)
                        
    lines_f.close()
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        refresh_lines(sys.argv[1])
    else:
        refresh_lines()
