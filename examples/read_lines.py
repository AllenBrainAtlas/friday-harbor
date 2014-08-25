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

# The flip side to this is that it is very slow to search for all paths emanting
# from a particular experiment's injection site.  Every voxel file needs to be 
# searched for a record of that experiment.  This experiment id corresponds to
# an injection into the primary motor cortex.
# http://connectivity.brain-map.org/projection/experiment/182616478
experiment_id = 182616478

# The return value is a dictionary from voxel coordinate -> path coordinates
# and density values.
paths = lines.by_experiment_id( experiment_id )
