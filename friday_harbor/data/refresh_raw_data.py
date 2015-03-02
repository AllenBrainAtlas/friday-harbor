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

import requests
import os
import sys
from friday_harbor.experiment_manager import ExperimentManager
from friday_harbor.paths import Paths
from friday_harbor.data.api import save_experiment_grid_data
from friday_harbor.data.api import unzip_experiment_grid_data

def refresh_raw_data(data_dir='.', include=None):
    paths = Paths(data_dir)

    # Settings:
    exp_manager = ExperimentManager(data_dir)

    # Make sure the directory exists
    try:
        os.makedirs(paths.experiment_raw_data_directory)
    except:
        pass # don't care if it already exists
    
    # Get list of experiments:
    for experiment in exp_manager:
        # Initializations:
        file_name = os.path.join(paths.experiment_raw_data_directory, 'experiment_%s.zip' % experiment.id)
        unzip_path = os.path.join(paths.experiment_raw_data_directory, '%s' % experiment.id)        

        save_experiment_grid_data(experiment.id, file_name, include)
        unzip_experiment_grid_data(file_name, unzip_path)

        print file_name

if __name__ == "__main__":
    nargs = len(sys.argv)
    if nargs == 2:
        refresh_raw_data(sys.argv[1])
    elif nargs > 2:
        refresh_raw_data(sys.argv[1], sys.argv[2:])
    else:
        refresh_raw_data()
    
