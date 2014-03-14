import h5py
import resources.Experiment as Experiment 

# Create injection masks:
f_proj = h5py.File('../src/projection_density.hdf5', 'w')
for e in Experiment.experiment_list:
    
    f_in = h5py.File(e.data_file_name, 'r')
    density_vals = f_in['density'].value
    f_in.close()
    f_proj[str(e.id)] = density_vals
    
f_proj.close()