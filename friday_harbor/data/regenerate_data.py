import sys
from friday_harbor.data.refresh_structure_json import refresh_structure_json
from friday_harbor.data.refresh_experiment_json import refresh_experiment_json
from friday_harbor.data.refresh_raw_data import refresh_raw_data
from friday_harbor.data.extract_experiment_to_hdf5 import extract_experiment_to_hdf5
from friday_harbor.data.refresh_grid_annotation import refresh_grid_annotation
from friday_harbor.data.create_masks import create_masks

def regenerate_data(data_dir='.'):
    print "refreshing structure json"
    refresh_structure_json(data_dir)

    print "refreshing experiment json"
    refresh_experiment_json(data_dir)

    print "refreshing raw data"
    refresh_raw_data(data_dir)

    print "extracting raw data to hdf5"
    extract_experiment_to_hdf5(data_dir)

    print "refreshing grid annotation"
    refresh_grid_annotation(data_dir)

    print "refreshing structure and injection masks"
    create_masks(data_dir)
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        regenerate_data(sys.argv[1])
    else:
        regenerate_data()

