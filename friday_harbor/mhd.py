# Copyright 2014 Allen Institute for Brain Science
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Nicholas Cain
# Allen Institute for Brain Science
# June 11 2014
# nicholasc@alleninstitute.org

import os, string
import numpy as np

# map from meta number types to numpy number types and back.
# note: for some reason np.uint8 != np.dtype('uint8').  both are acceptable
#       when constructing an array, but the latter is what's returned from 
#       array.dtype, so it's easier to use that as a key.
TYPE_MAP = {
    'MET_UCHAR': np.dtype('uint8'),
    'MET_USHORT': np.dtype('uint16'),
    'MET_UINT': np.dtype('uint32'),
    'MET_FLOAT': np.dtype('float32')
}

INV_TYPE_MAP = { v:k for k,v in TYPE_MAP.iteritems() }

# some meta image readers assume that the header values are stored in
# a particular order.  I'm looking at you, ITK-SNAP.
KEY_ORDER = [
    'ObjectType',
    'NDims',
    'BinaryData',
    'BinaryDataByteOrderMSB',
    'CompressedData',
    'TransformMatrix',
    'Offset',
    'CenterOfRotation',
    'AnatomicalOrientation',
    'ElementSpacing',
    'DimSize',
    'ElementType',
    'ElementDataFile'
]

# These values will be used to write an mhd file if none are explicitly
# given to the writing function.
DEFAULT_HEADER_VALUES = {
    'ObjectType': 'Image',
    'NDims': '3',
    'BinaryData': 'True',
    'BinaryDataByteOrderMSB': 'False',
    'CompressedData': 'False',
    'TransformMatrix': '1 0 0 0 1 0 0 0 1',
    'Offset': '0 0 0',
    'CenterOfRotation': '0 0 0',
    'AnatomicalOrientation': 'RAI',
    'ElementSpacing': '100 100 100'
}

def read(header_file_name):
    '''
    Given and mhd file, this assumes that the data is stored as a binary blob
    in the 'ElementDataFile' listed the header.  
    Returns a tuple of the form (meta_data_dictionary, numpy_array).
    '''
    header_file_name = os.path.abspath(header_file_name)

    print "reading", header_file_name

    meta = {}
    with open(header_file_name, 'rb') as header_file:
        for line in header_file:
            key, val = [ string.strip(s) for s in line.split("=") ]
            meta[key] = val

    header_dir = os.path.dirname(header_file_name)

    raw_file_name = os.path.join(header_dir, meta['ElementDataFile'])

    print "reading", raw_file_name

    dtype = meta['ElementType']
    dims = [ int(d) for d in meta['DimSize'].split() ]
    
    raw = np.fromfile(raw_file_name, TYPE_MAP[dtype])

    # note the 'F'! if you want the dims to match the order in the meta file, 
    # you need to read in fortran order.
    raw = raw.reshape(dims, order='F')

    return meta, raw

def write(header_file_name, meta, raw):
    '''
    Write an .mhd file with the given meta data and numpy array.  Appropriate header
    values will be set based on the size and shape of the array, however the 
    remainder will be pulled from the supplied 'meta' dictionary.  If they
    do not exist there, DEFAULT_HEADER_VALUES are used.
    '''
    base, ext = os.path.splitext(header_file_name)
    assert ext == '.mhd', "%s is not an MHD file" % (header_file_name)

    raw_file_name = base + ".raw"
    meta['ElementDataFile'] = raw_file_name
    meta['DimSize'] = ' '.join([ str(i) for i in raw.shape ])
    meta['ElementType'] = INV_TYPE_MAP[raw.dtype]

    with open(header_file_name, 'wb') as header_file:
        for k in KEY_ORDER:
            if k in meta:
                header_file.write(k + ' = ' + meta[k] + '\n')
            else:
                header_file.write(k + ' = ' + DEFAULT_HEADER_VALUES[k] + '\n')

    # note the transpose! numpy.tofile writes in 'C' order only, so transpose to 'F'.
    raw.transpose().tofile(raw_file_name)
