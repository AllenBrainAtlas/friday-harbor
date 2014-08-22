import friday_harbor.experiment as experiment

# Settings:
data_dir = '../friday_harbor/data'

# Get the experiment manager:
experiment_manager = experiment.ExperimentManager(data_dir=data_dir)

# Print some data about each 
for e in experiment_manager.experiment_list:
    print e.id, e.transgenic_line, e.injection_coordinates, e.injection_volume