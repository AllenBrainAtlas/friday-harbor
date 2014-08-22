# Copyright 2014 Allen Institute for Brain Science
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Nicholas Cain
# Allen Institute for Brain Science
# June 11 2014
# nicholasc@alleninstitute.org

import sys

from friday_harbor.data.refresh_structure_json import refresh_structure_json
from friday_harbor.data.refresh_experiment_json import refresh_experiment_json
from friday_harbor.data.refresh_raw_data import refresh_raw_data
from friday_harbor.data.extract_experiment_to_hdf5 import extract_experiment_to_hdf5
from friday_harbor.data.refresh_grid_annotation import refresh_grid_annotation
from friday_harbor.data.create_masks import create_masks

def regenerate_data(data_dir='.', injection_structures=None, wild=True, cre=True):
    print "refreshing structure json"
    refresh_structure_json(data_dir)

    print "refreshing experiment json"
    refresh_experiment_json(data_dir, injection_structures, wild, cre)

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

