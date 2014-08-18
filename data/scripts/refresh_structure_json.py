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
import resources.paths as paths

# Settings:
json_file_save_dir = 'data/src'
json_file_name = 'structure_data.json'
anatomical_structure_info_url = 'http://api.brain-map.org/api/v2/data/Structure/query.json?criteria=[graph_id$eq1]&order=structures.graph_order&tabular=structures.id,structures.acronym,structures.graph_order,structures.color_hex_triplet,structures.structure_id_path,structures.name&start_row=0&num_rows=all'

# Get data:
raw_json = requests.request('get', anatomical_structure_info_url).json()

# Write 
with open(paths.structure_json_file_name, 'wb') as f:
    json.dump(raw_json, f)






