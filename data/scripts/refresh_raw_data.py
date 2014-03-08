import requests
import os
from resources.Experiment import experiment_list
import zipfile
import shutil

# Settings:
file_save_dir = '../src/raw_data'

for e in experiment_list:

    # Initializations:
    file_name = os.path.join(os.path.dirname(__file__), file_save_dir, 'experiment_%s.zip' % e.id)
    experiment_info_url = 'http://testwarehouse:9000/grid_data/download/%s?include=density,injection' % e.id
    
    # Get data:
    with open(file_name,'wb') as handle:
        request = requests.get(experiment_info_url, stream=True)
        for block in request.iter_content(1024):
            if not block:
                break
            handle.write(block)
    handle.close()
    
    # Unzip:
    unzip_path = os.path.join(os.path.dirname(__file__), file_save_dir, '%s' % e.id)
    shutil.rmtree(unzip_path, unzip_path)
    os.mkdir(unzip_path)
    zf = zipfile.ZipFile(file_name, 'r')
    zf.extractall(unzip_path)
    zf.close()
    os.remove(file_name)
    print file_name
    
