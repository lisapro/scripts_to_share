import requests as rq
import json

'''
to port forward from gcloud
gcloud container clusters get-credentials k8s-dev 

for metadata : 
kubectl port-forward metaflow-4166970183-3b5xr 4000:5000
'''
path_meta  = "http://localhost:4000"
path_data = "http://localhost:3000/ts/"

def get_list():
    pass

def get_data(start,end,var_uuid):
    stuff = rq.get(path_data,
                   params={'uuid': var_uuid})     
    data = stuff.json()
    return data 

def get_metadata():
    '''Here uuid is for platform ''' 
    stuff = rq.get(path_meta,
                   params={'uuid': '274c62b8-758d-4062-af53-c00cd2bdf10e','parts':'2'})
    meta = stuff.json()
    return meta
    
    #json.dump(in_data, 'meta.json')
    
#m = get_metadata()
##with open('data.json', 'w') as outfile:  
#    json.dump(m, outfile, indent=4)
    
    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example code on how to query meta structure for a platform/vessel
and also create a dictionary with all the time series elements
"""
import json
import requests as rq

META_SOURCE = "http://127.0.0.1:4000"
#PLATFORM_PATH = "TF"  # Color Fantasy
PLATFORM_PATH = "FA"  # Color Fantasy


def _walk_tree(top):
    """walk a tree of parts and yield all time series objects"""
    if top.get("parts", False) and len(top["parts"]) > 0:
        for t in top["parts"]:
            for ct in _walk_tree(t):
                yield ct
    if top.get("ttype") in ["tseries", "qctseries", "gpstrack"]:
        yield top


# Get "root" meta data for platform
par = {"path": PLATFORM_PATH, "unique": True}
r = rq.get(META_SOURCE, params=par)
in_data = r.json()
#print(in_data)
assert("t" in in_data)
platform = in_data["t"]
print(platform)

# Get full tree for platform
par = {"uuid": platform["uuid"], "parts": 100}
r = rq.get(META_SOURCE, params=par)
platform_tree = r.json()["t"]
print(json.dumps(platform_tree, indent=4))

# Get list of all time series objects
ts_list = [ts for ts in _walk_tree(platform_tree)]
#for ts in ts_list:
#    print(ts)


# Create lookup dictionary for the time series
name_lookup = {ts["name"]: ts for ts in ts_list if "name" in ts}
print(json.dumps(name_lookup, indent=4))
    
    
    