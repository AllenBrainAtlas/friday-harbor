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

def refresh_experiment_json(data_dir='.', injection_structures=None, wild=True, cre=True):

    # default value for injection structures is gray (structure id 8)
    if injection_structures is None:
        injection_structures = [8]

    paths = Paths(data_dir)

    injection_structures = ','.join([str(i) for i in injection_structures])
    experiment_info_url = 'http://api.brain-map.org/api/v2/data/query.json?' + \
                          'criteria=service::mouse_connectivity_injection_structure[num_rows$eq3000]' + \
                          '[primary_structure_only$eqtrue]' + \
                          '[injection_structures$eq'+injection_structures+']'

    if wild is True and cre is False:
        # if we are restricted to wild type experiments only, add that filter to the query (id for wild = 0)
        experiment_info_url += '[transgenic_lines$eq0]'
    elif wild is False and cre is True:
        # this is the list of all of the transenic lines with projection experiments public as of 8/21/14
        experiment_info_url += '[transgenic_lines$eq177838542,177837446,177838108,177837315,287226763,177837281,177838225,177839159,177838331,177838138,182693192,182846862,177838907,177838259,177837834,177835893,177839004,177839022,177838899,177837979,177839513,266649644,182761781,177838266,177836019,177838361,177839468,177838877,177838584,177838828,177838302,177839174,177839285,177838502,177838803,177838496,272833052,177839494,177838942,177837788,177839135,177837364,177839044,256980970,177839406,177839331,183238310,177837713,177837275,177839376,177838953,182761918,177838927,177837779,177839425,177838755,183941572,177838022,177839481,177839075,177837262,182901722,177838494,177837858,177838435,179697864,177837695,177837481,177837516,177837637,177837777,177838048,180526080,177837324,177839090,177838074,177838781,177838681,177839294,177837625,177838710,177837328,177839216,177838715,177838730,177837797,177837611,265180449,177838633,177839186,177838622,177838665,177839108,177837585]'
    elif wild is False and cre is False:
        return 

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
    





