from friday_harbor.paths import Paths

class Lines( object ):
    def __init__(self, data_dir='.'):
        self.paths = Paths(data_dir)

    def by_target_voxel(self, target_voxel):
        pass

    def by_experiment_id(self, experiment_id):
        pass

        
