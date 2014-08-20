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

import json
import requests
import os
import sys
from friday_harbor.paths import Paths

def refresh_experiment_json(data_dir='.', injection_structures=None, wild_only=False):

    # default value for injection structures is gray (structure id 8)
    if injection_structures is None:
        injection_structures = [8]

    paths = Paths(data_dir)

    injection_structures = ','.join([str(i) for i in injection_structures])
    experiment_info_url = 'http://api.brain-map.org/api/v2/data/query.json?' + \
                          'criteria=service::mouse_connectivity_injection_structure[num_rows$eq3000]' + \
                          '[primary_structure_only$eqtrue]' + \
                          '[injection_structures$eq'+injection_structures+']'

    # if we are restricted to wild type experiments only, add that filter to the query (id for wild = 0)
    if wild_only:
        experiment_info_url += '[transgenic_lines$eq0]'
        
    # Get data:
    raw_json = requests.request('get', experiment_info_url).json()
    
    # Write 
    with open(paths.experiment_json_file_name,'wb') as f:
        json.dump(raw_json, f)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        refresh_experiment_json(sys.argv[1])
    else:
        refresh_experiment_json()
    







