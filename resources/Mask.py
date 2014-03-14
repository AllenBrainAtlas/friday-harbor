import os
import numpy as np
import resources.Annotation as Annotation
import h5py

class Mask(object):
    
    def __init__(self, mask_tuple):
        
        self.mask = mask_tuple
        
        pass
    
    def __len__(self):
        return len(self.mask[0])
    
    def write_to_hdf5_group(self, group, create_name=None):
        if create_name != None:
            group = group.create_group(create_name)
        for ind_array, ind_dim_name in zip(self.mask,['XX', 'YY', 'ZZ']):
            group[ind_dim_name] = ind_array
            
    def write_to_hdf5(self, file_name):
        f = h5py.File(file_name, 'w')
        self.write_to_hdf5_group(f)
        f.close()
            
    @staticmethod
    def read_from_hdf5_group(group):
        return Mask(tuple([group[ind_dim_name].value for ind_dim_name in ['XX', 'YY', 'ZZ']]))
        
    @staticmethod
    def read_from_hdf5(file_name, subgroup=None):
        f = h5py.File(file_name, 'r')
        if subgroup == None:
            mask_obj = Mask.read_from_hdf5_group(f)
        else:
            mask_obj = Mask.read_from_hdf5_group(f[subgroup])
        f.close()
        
        return mask_obj
    
    @staticmethod
    def intersection(m1, m2):
        
        if len(m1) == 0 or len(m2) == 0:
            xx, yy, zz = np.array([]), np.array([]), np.array([])
            
        else:
            m1_set = set(zip(*m1.mask))
            m2_set = set(zip(*m2.mask))
            
            intersection_set = m1_set.intersection(m2_set) 
            if len(intersection_set) == 0:
                xx, yy, zz = np.array([]), np.array([]), np.array([])
            else:
                xx, yy, zz = zip(*list(intersection_set))
            
        return Mask((np.array(xx), np.array(yy), np.array(zz)))
    
    @staticmethod
    def union(m1, m2):
        
        if len(m1) == 0 and len(m2) == 0:
            xx, yy, zz = np.array([]), np.array([]), np.array([])
        elif len(m1) == 0:
            return m2
        elif len(m2) == 0:
            return m1
        else:
        
            m1_set = set(zip(*m1.mask))
            m2_set = set(zip(*m2.mask))
            
            union_set = m1_set.union(m2_set)
            xx, yy, zz = zip(*list(union_set))
            
        return Mask((np.array(xx), np.array(yy), np.array(zz)))
    
    def difference(self, mask_to_subtract):
        if len(self) == 0:
            xx, yy, zz = np.array([]), np.array([]), np.array([])
        else:
            self_set = set(zip(*self.mask))
            other_set = set(zip(*mask_to_subtract.mask))
            
            new_set = set()
            for x in self_set:
                if not x in other_set:
                    new_set.add(x)
                    
            xx, yy, zz = zip(*list(new_set))
            
            
        return Mask((np.array(xx), np.array(yy), np.array(zz)))
        


 



