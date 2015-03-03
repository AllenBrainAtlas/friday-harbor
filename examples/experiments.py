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

from friday_harbor.experiment_manager import ExperimentManager

# Settings:
data_dir = '.'

# Get the experiment manager:
experiment_manager = ExperimentManager(data_dir=data_dir)

# Print some data about each one:
for e in experiment_manager.experiment_list:
    print e.id, e.transgenic_line, e.injection_coordinates, e.injection_volume
