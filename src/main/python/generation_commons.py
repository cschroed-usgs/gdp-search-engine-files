import argparse
import os
import errno
from owslib.csw import CatalogueServiceWeb 
import re


"""
Retrieve csw records of GDP data sets from the csw endpoint
    csw_endpoint - String url for a csw server

"""
def get_datasets_from_csw(csw_endpoint):
    csw = CatalogueServiceWeb(csw_endpoint)
    csw.getrecords2(esn='full', maxrecords=1000)
    return csw.records.values()

'''
parse commandline args and return a dictionary
'''
def parse_args (argv):
    
    DEFAULT_CSW_ENDPOINT = 'http://cida.usgs.gov/gdp/csw'
    DEFAULT_ROOT_URL = 'http://cida.usgs.gov/gdp/'
    
    parser = argparse.ArgumentParser(description='Generate sitemap.xml for NWC')
    parser.add_argument('--csw_endpoint', 
                        help='CSW endpoint used to retrieve data sets. Defaults to %s' % DEFAULT_CSW_ENDPOINT, 
                        default=DEFAULT_CSW_ENDPOINT)
    parser.add_argument('--root_url', 
                        help='The application\'s root url. Defaults to %s' % DEFAULT_ROOT_URL,
                        default=DEFAULT_ROOT_URL)
    parser.add_argument('--destination_dir', 
                        help='Destination directory for the sitemap.xml file. Defaults to the directory where the script is run.',
                        default='.')
    args = parser.parse_args(args=argv[1:])
    return args

'''
get dataset items
'''
def get_datasets(csw_endpoint):
    return get_datasets_from_csw(csw_endpoint)

'''
get nwc data from geoserver and sciencebase.
returns a dictionary of data from the servers
'''
def get_gdp_data(csw_endpoint):
    print 'Retrieving data sets from %s' % csw_endpoint
    return {
            'datasets' : get_datasets(csw_endpoint),
    }

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise