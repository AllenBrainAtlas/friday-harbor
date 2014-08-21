import requests

API_BASE_URL = 'http://api.brain-map.org/api/v2/data/query.json?criteria='

def query(q):
    url = API_BASE_URL + q

    r = requests.get(url)
    rjson = r.json()

    success = rjson.get('success', False)

    if not success:
        return None
    else:
        return rjson['msg']

def target_spatial_search(target_voxel, experiments=None):
    coord_str = ','.join( [ str(c*100) for c in target_voxel ] )

    url = 'service::mouse_connectivity_target_spatial' + \
        '[seed_point$eq%s]' % ( coord_str )

    if experiments is not None:
        experiment_str = ','.join( [ str(e) for e in experiments ] )
        url += '[section_data_set$in%s]' % experment_str

    return query(url)
    

if __name__ == "__main__":
    q = 'model::SectionDataSet,products[id$eq5]'
    r = query(q)
    print r
    
