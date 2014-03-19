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

# Settings:
json_file_save_dir = '../src'
json_file_name = 'experiment_data.json'
experiment_info_url = 'http://api.brain-map.org/api/v2/data/query.json?criteria=service::mouse_connectivity_injection_structure[injection_domain$eqgrey][num_rows$eq3000][primary_structure_only$eqtrue][injection_structures$eqgrey]'


# Get data:
raw_json = requests.request('get', experiment_info_url).json()

# Write 
f = open(os.path.join(json_file_save_dir, json_file_name),'wb')
json.dump(raw_json, f)
f.close()







