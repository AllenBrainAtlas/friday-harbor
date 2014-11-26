from friday_harbor.experiment import Experiment
from friday_harbor.paths import Paths
from friday_harbor.ontology import Ontology
import json

class ExperimentManager( object ):
    '''
    ExperimentManager is a light wrapper around a list of Experiments that
    provides some simple filtering methods for extracting experiment subsets
    (wild type, cre, etc).
    
    '''

    def __init__(self, data_dir=None):

        self.paths = Paths(data_dir)
        self.ontology = Ontology(data_dir)
        experiment_json_file_name = self.paths.experiment_json_file_name
        raw_data_dir = self.paths.experiment_raw_data_directory
            
        self.experiment_list = []

        # Get data:
        with open(experiment_json_file_name) as f:
            experiment_data = json.load(f)

            self.experiment_list = [ Experiment.from_json(d, self.paths, self.ontology) for d in experiment_data ]

        self.experiments_by_id = { e.id: e for e in self.experiment_list }

    def all(self):
        ''' Return the entire list of experiments. '''
        return self.experiment_list

    def wildtype(self):
        ''' Return a generator for just the wild type experiments. '''
        return ( e for e in self.experiment_list if e.wildtype == True )

    def cre(self):
        ''' Return a generator for just the cre experiments. '''
        return ( e for e in self.experiment_list if e.wildtype == False )

    def cortex(self):
        ''' Return a generator for just the cortical injections. '''
        return ( e for e in self.experiment_list if 315 in e.structure.path_to_root )

    def noncortex(self):
        ''' Return a generator for just the cortical injections. '''
        return ( e for e in self.experiment_list if not (315 in e.structure.path_to_root) )
        
    def experiment_by_id(self, experiment_id):
        ''' Get a handle to an experiment by its id. '''
        return self.experiments_by_id[experiment_id]

    def __iter__(self):
        ''' By default, iterating over the manager will iterate through all of the experiments. '''
        return iter(self.experiment_list)