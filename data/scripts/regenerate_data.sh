#!/bin/bash
#
# Generate connectivity data
#

echo "Refreshing structure information"
#python refresh_structure_json.py
echo "    Done."

echo "Refreshing experiment information"
#python refresh_experiment_json.py
echo "    Done."

echo "Refreshing raw data"
#python refresh_raw_data.py
echo "    Done."

echo "Processing data"
matlab -nodisplay -nosplash -nodesktop -r 'generate_matrix;exit'
echo "    Done."






