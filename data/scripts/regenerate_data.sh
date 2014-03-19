#!/bin/bash
#
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
#
#
#
# Generate connectivity data
#

echo "Refreshing structure information"
python refresh_structure_json.py
echo "    Done."

echo "Refreshing experiment information"
python refresh_experiment_json.py
echo "    Done."

echo "Refreshing raw data"
python refresh_raw_data.py
echo "    Done."

echo "Extracting experiments to hdf5"
python extract_experiment_to_hdf5.py
echo "    Done."

echo "Extracting grid annotation"
python refresh_grid_annotation.py
echo "    Done."

echo "Creating masks"
python create_masks.py
echo "    Done."

echo "Creating density matrix"
python create_density.py
echo "    Done."



