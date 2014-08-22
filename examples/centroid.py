from friday_harbor.structure import Ontology
from friday_harbor.mask import Mask

# Settings:
data_dir = '../friday_harbor/data'
my_structure_acronym_list = ['LGd', 'VISp', 'MOs'] 

# Construct the ontology from the data directory:
ontology = Ontology(data_dir=data_dir)

# Print the centroids (each hemisphere and in total) for structures:
for a in my_structure_acronym_list:
    curr_id = ontology.acronym_id_dict[a]
    m_left = ontology.get_mask_from_id_left_hemisphere_nonzero(curr_id)
    m_right = ontology.get_mask_from_id_right_hemisphere_nonzero(curr_id)
    m_all = ontology.get_mask_from_id_nonzero(curr_id)
    print '%4s:' % a,  m_left.centroid, m_right.centroid, m_all.centroid