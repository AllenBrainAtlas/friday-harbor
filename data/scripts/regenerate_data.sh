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

echo "Extracting experiments to hdf5"
#python extract_experiment_to_hdf5.py
echo "    Done."

echo "Extracting grid annotation"
#python extract_grid_annotation.py
echo "    Done."

echo "Creating masks"
#python create_masks.py
echo "    Done."

echo "Creating density matrix"
#python create_density.py
echo "    Done."



