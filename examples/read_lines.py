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

from friday_harbor.lines import Lines

# This should point to the data directory. Note that the lines are only included
# in the full 'data' directory distributed at the beginning of the course.  
data_dir = '.'

# The Lines object provides some simple accessors for the binary line files.
lines = Lines( data_dir )

# The line files are organized by target voxel.  This means that the it's quick
# to search for the list of experiments targeting a particular voxel.  This 
# voxel located in the thalamus.
target_voxel = ( 71, 37, 78 )

# This is a dictionary from experiment_id -> path info.  This will include the
# 3D coordinates of the path vertices, as well as the density values at those
# vertices.
experiments = lines.by_target_voxel( target_voxel )
print len(experiments), "experiments targeting", target_voxel

# Lines.by_target_voxel will restrict your results to a set of experiments if
# you like.
experiment_ids = [ 100148503, 183282970 ]
experiments = lines.by_target_voxel( target_voxel, experiment_ids )
print "paths from experiments", experiment_ids, "to", target_voxel, ":", len(experiments)

# The flip side to this is that it is very slow to search for all paths emanting
# from a particular experiment's injection site.  Every voxel file needs to be 
# searched for a record of that experiment.  The return value is a dictionary from 
# voxel coordinate -> path coordinates and density values.
paths = lines.by_experiment_id( 183282970 )
print len(paths), "voxels targeted by experiments", experiment_ids
