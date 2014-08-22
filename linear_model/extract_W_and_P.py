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
# nicholasc@alleninstitute.orgimport numpy as np

import scipy.io as sio
import numpy as np

file_name_prefix_list = ['W_ipsi', 'W_contra', 'PValue_ipsi', 'PValue_contra']

for file_name_prefix in file_name_prefix_list:

    f = open(file_name_prefix + '.csv', 'r')
    row_labels = []
    col_labels = []
    data = []
    for ii, line in enumerate(f):
        if ii != 0:
            data.append([])
        for jj, val in enumerate(line.split(',')):
            if ii == 0 and jj != 0:
                row_labels.append(val)
            elif ii !=0 and jj == 0:
                col_labels.append(val)
            elif ii != 0 and jj != 0:
                data[-1].append(float(val))
                
    # Convert matlab format:
    data = np.array(data)
    row_labels = np.array(row_labels)
    col_labels = np.array(col_labels)
    sio.savemat(file_name_prefix+'.mat', {'row_labels':row_labels, 'col_labels':col_labels, 'data':data})