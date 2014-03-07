import json
import requests
import os

# Settings:
json_file_save_dir = '../src'
json_file_name = 'structure_data.json'
anatomical_structure_info_url = 'http://api.brain-map.org/api/v2/data/Structure/query.json?criteria=[graph_id$eq1]&order=structures.graph_order&tabular=structures.id,structures.acronym,structures.graph_order,structures.color_hex_triplet,structures.structure_id_path,structures.name&start_row=0&num_rows=all'


# Get data:
raw_json = requests.request('get', anatomical_structure_info_url).json()

# Write 
f = open(os.path.join(json_file_save_dir, json_file_name),'wb')
json.dump(raw_json, f)
f.close()





