import numpy as np

import requests
from xml.etree import ElementTree

import sys
import os
import time 

def get_block_code(lng, lat): 
    '''Returns census block code given longitude and latitude.'''
    params = {'longitude': str(lng), 'latitude': str(lat)}
    r = requests.get("http://data.fcc.gov/api/block/2010/find", params=params)
    tree = ElementTree.fromstring(r.content)

    for child in tree.iter('{http://data.fcc.gov/api}Block'):
        return child.attrib['FIPS']

def main(): 

    # load dataset 
    print 'loading dataset'
    data_path = '../data/raw/foursquare-nyc-check-ins/dataset_TSMC2014_NYC.npy'
    dataset = np.load(data_path)[:10]

    # create tmp directories 
    tmp_dir = os.path.dirname('./tmp/')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    # init block_codes
    block_codes = np.empty((len(dataset), 2)) #index, blockCode    
    block_codes.fill(-1)
    block_codes[:, 0] = np.arange(len(dataset))
    print 'data shape', block_codes.shape

    if len(sys.argv) > 1:
        # load checkpointed file
        checkpoint_path = sys.argv[1]
        block_codes_chkpt = np.genfromtxt(checkpoint_path, delimiter=',')
        block_codes[:len(block_codes_chkpt)] = block_codes_chkpt
        print 'loading checkpoint from', checkpoint_path
    
    # compute block codes for all where field is '-1' 
    start_time = time.time()    
    unfinished = block_codes[block_codes[:, 1] == -1]

    while len(unfinished) > 0: 
        first_unfinished = unfinished[0]
        idx = int(first_unfinished[0])
        
        if idx > 0 and idx % 100 == 0:
            elapsed = time.time() - start_time
            print 'processing', idx, 'elapsed:', time.strftime("%H:%M:%S", time.gmtime(elapsed))
            
            np.savetxt(tmp_dir + 'block_codes_checkpoint.csv', block_codes, fmt='%d,%d')

        try: 
            block_code = get_block_code(dataset[idx][5], dataset[idx][4])
            block_codes[idx, 1] = block_code
        except Exception as e: 
            print 'exception at idx', idx, e.args
            
        unfinished = block_codes[block_codes[:, 1] == -1]

    # convert to census tracts, according to: 'XXYYYZZZZZZAAAA where X=State, Y=County, Z=Tract, A=Block'
    census_tracts = np.empty((len(dataset), 2)) #index, blockCode
    census_tracts[:, 0] = np.arange(len(dataset))
    census_tracts[:, 1] = (block_codes[:,1]/1e4)
    out_file = '../data/processed/census_tracts_per_checkin.csv'
    print 'saving to ', out_file
    np.savetxt(out_file, census_tracts, fmt='%d,%d')
    
    # remove tmp directory 
    os.rmdir(tmp_dir)

if __name__ == '__main__': 
    main()
