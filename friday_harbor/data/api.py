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
import zipfile
import shutil
import os

API_HOST = 'http://api.brain-map.org/'
API_BASE_URL = API_HOST + 'api/v2/data/query.json?criteria='

def query(q):
    url = API_BASE_URL + q

    r = requests.get(url)
    rjson = r.json()

    success = rjson.get('success', False)

    if not success:
        return None
    else:
        return rjson['msg']

def structure_search():
    q = 'model::Structure[graph_id$eq1],rma::options[order$eqstructures.graph_order]&tabular=structures.id,structures.acronym,structures.graph_order,structures.color_hex_triplet,structures.structure_id_path,structures.name&start_row=0&num_rows=all'

    return query(q)

def save_experiment_grid_data(experiment_id, file_name, include=None):
    if include is None:
        include = [ "density", "injection", "intensity" ]
        
    exp_info_url_pattern = API_HOST + 'grid_data/download/%s?include=%s'
    experiment_info_url =  exp_info_url_pattern % (experiment_id, ','.join(include))

    # Get data:
    with open(file_name,'wb') as handle:
        request = requests.get(experiment_info_url, stream=True)
        for block in request.iter_content(1024):
            if not block:
                break
            handle.write(block)

def unzip_experiment_grid_data(zip_file_name, directory, remove_zip=True):
    shutil.rmtree(directory, directory)
    os.mkdir(directory)
    zf = zipfile.ZipFile(zip_file_name, 'r')
    zf.extractall(directory)
    zf.close()
    if remove_zip:
        os.remove(zip_file_name)
    
def experiment_search(injection_structures=None, wild=True, cre=True):

    # default value for injection structures is gray (structure id 8)
    if injection_structures is None:
        injection_structures = [8]

    injection_structures = ','.join([str(i) for i in injection_structures])

    q = 'service::mouse_connectivity_injection_structure[num_rows$eq3000]' + \
        '[primary_structure_only$eqtrue]' + \
        '[injection_structures$eq'+injection_structures+']'

    if wild is True and cre is False:
        # if we are restricted to wild type experiments only, add that filter to the query (id for wild = 0)
        q += '[transgenic_lines$eq0]'
    elif wild is False and cre is True:
        # this is the list of all of the transenic lines with projection experiments public as of 8/21/14
        q += '[transgenic_lines$eq177838542,177837446,177838108,177837315,287226763,177837281,177838225,177839159,177838331,177838138,182693192,182846862,177838907,177838259,177837834,177835893,177839004,177839022,177838899,177837979,177839513,266649644,182761781,177838266,177836019,177838361,177839468,177838877,177838584,177838828,177838302,177839174,177839285,177838502,177838803,177838496,272833052,177839494,177838942,177837788,177839135,177837364,177839044,256980970,177839406,177839331,183238310,177837713,177837275,177839376,177838953,182761918,177838927,177837779,177839425,177838755,183941572,177838022,177839481,177839075,177837262,182901722,177838494,177837858,177838435,179697864,177837695,177837481,177837516,177837637,177837777,177838048,180526080,177837324,177839090,177838074,177838781,177838681,177839294,177837625,177838710,177837328,177839216,177838715,177838730,177837797,177837611,265180449,177838633,177839186,177838622,177838665,177839108,177837585]'
    elif wild is False and cre is False:
        return None

    print q
    return query(q)

def target_spatial_search(target_voxel, experiments=None):
    coord_str = ','.join( [ str(c*100) for c in target_voxel ] )

    url = 'service::mouse_connectivity_target_spatial' + \
        '[seed_point$eq%s]' % ( coord_str )

    if experiments is not None:
        experiment_str = ','.join( [ str(e) for e in experiments ] )
        url += '[section_data_set$in%s]' % experment_str

    return query(url)
    

if __name__ == "__main__":
    q = 'model::SectionDataSet,products[id$eq5]'
    r = query(q)
    print r
    
