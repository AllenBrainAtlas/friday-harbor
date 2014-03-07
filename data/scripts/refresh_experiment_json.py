import json
import requests
import os

# Settings:
json_file_save_dir = '../src'
json_file_name = 'experiment_data.json'
experiment_info_url = 'http://testwarehouse:9000/api/v2/data/query.json?criteria=service::mouse_connectivity_injection_structure[injection_domain$eqgrey][num_rows$eq3000][primary_structure_only$eqtrue][injection_structures$eqgrey]'


# Get data:
raw_json = requests.request('get', experiment_info_url).json()

# Write 
f = open(os.path.join(json_file_save_dir, json_file_name),'wb')
json.dump(raw_json, f)
f.close()







