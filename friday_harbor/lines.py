import h5py
from friday_harbor.paths import Paths

class Lines( object ):
    def __init__(self, data_dir='.'):
        self.paths = Paths(data_dir)

    def by_target_voxel(self, target_voxel):
        f = h5py.File(self.paths.lines_file_name, 'r')

        experiments = {
        }

        try:
            group_name = '/%d/%d/%d' % (target_voxel[0], target_voxel[1], target_voxel[2])
            g = f[group_name]
            for k in g.keys():
                experiment_id = int(k)
                d = g[k]
                experiments[experiment_id] = {
                    'density': d['density'].value,
                    'path': d['path'].value
                }
        except Exception as e:
            f.close()
            print e
            return None

        f.close()
        return experiments

    def by_experiment_id(self, experiment_id):
        f = h5py.File(self.paths.lines_file_name, 'r')
        
        experiments = {}

        # first loop on x coords
        for x in f:
            xg = f[x]

            # loop on y coords
            for y in xg:
                yg = xg[y]

                # loop on z coords
                for z in yg:
                    zg = yg[z]

                    # see if the experiment exists
                    eid = str(experiment_id)
                    
                    if eid in zg:
                        coord = ( int(x), int(y), int(z) )

                        eg = zg[eid]
                        
                        experiments[coord] = {
                            'density': eg['density'].value,
                            'path': eg['path'].value
                        }

        f.close()

        return experiments

        
