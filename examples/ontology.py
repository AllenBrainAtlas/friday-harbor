from friday_harbor.structure import Ontology

# Settings:
data_dir = '../friday_harbor/data'

# Construct the ontology from the data directory:
ontology = Ontology(data_dir=data_dir)

# Print data about each possible structure:
for s in ontology.structure_list:
    print s.name, s.structure_id, s.acronym

