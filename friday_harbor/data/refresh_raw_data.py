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
import zipfile
import shutil
import sys
from friday_harbor.experiment import ExperimentManager
from friday_harbor.paths import Paths


def refresh_raw_data(data_dir=None):
    paths = Paths(data_dir)

    # Settings:
    exp_manager = ExperimentManager(data_dir)
    exp_info_url_pattern = 'http://api.brain-map.org/grid_data/download/%s?include=density,injection'

    # Make sure the directory exists
    try:
        os.makedirs(paths.experiment_raw_data_directory)
    except:
        pass # don't care if it already exists
    
    # Get list of experiments:
    for experiment in exp_manager:
        # Initializations:
        file_name = os.path.join(paths.experiment_raw_data_directory, 'experiment_%s.zip' % experiment.id)
        experiment_info_url =  exp_info_url_pattern % experiment.id
        
        # Get data:
        with open(file_name,'wb') as handle:
            request = requests.get(experiment_info_url, stream=True)
            for block in request.iter_content(1024):
                if not block:
                    break
                handle.write(block)

        # Unzip:
        unzip_path = os.path.join(paths.experiment_raw_data_directory, '%s' % experiment.id)
        shutil.rmtree(unzip_path, unzip_path)
        os.mkdir(unzip_path)
        zf = zipfile.ZipFile(file_name, 'r')
        zf.extractall(unzip_path)
        zf.close()
        os.remove(file_name)
        print file_name

if __name__ == "__main__":
    if len(sys.argv) == 2:
        refresh_raw_data(sys.argv[1])
    else:
        refresh_raw_data()
    
