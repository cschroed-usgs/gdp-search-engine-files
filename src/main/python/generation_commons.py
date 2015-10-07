import argparse
import os
import errno
from owslib.csw import CatalogueServiceWeb 
from lxml import etree

#define xpaths relative to a gmd:MD_Metadata element
attribute_to_xpath_fragment = {
    #author
    "creator" : "/gmd:contact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString/text()",
    #organization
    "publisher": "/gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString/text()"
}
namespaces = {
    'gmd' : 'http://www.isotc211.org/2005/gmd',
    'csw' : 'http://www.opengis.net/cat/csw/2.0.2',
    'gco' : 'http://www.isotc211.org/2005/gco',
    'gml32' : 'http://www.opengis.net/gml/3.2'
}

record_xpath_template = "//gmd:MD_Metadata[gmd:fileIdentifier/gco:CharacterString[text() ='{0}']]"

"""
Retrieve csw records of GDP data sets from the csw endpoint
    csw_endpoint - String url for a csw server
    extended - Boolean if true, perform additional querying and parsing to retrieve more
            information

"""
def get_datasets_from_csw(csw_endpoint, extended):
    print 'Retrieving data sets from %s' % csw_endpoint

    csw = CatalogueServiceWeb(csw_endpoint)
    csw.getrecords2(esn='full', maxrecords=1000)
    parsed_records = csw.records.values()
    if extended:
        #request the data a second time in an encoding with different information
        #manually parse the second response and join the information in to the existing records 
        csw.getrecords2(esn='full', maxrecords=1000, outputschema=namespaces['gmd'])
        unparsed_response = csw.response
        root = etree.XML(unparsed_response)
   
        for record in parsed_records:
            record_id = record.identifier
            xpath_record_fragment = record_xpath_template.format(record_id)
            for attribute, xpath_fragment in attribute_to_xpath_fragment.iteritems():
                xpath_attribute_fragment = xpath_record_fragment + xpath_fragment
                value = root.xpath(xpath_attribute_fragment, namespaces=namespaces)
                if len(value) != 0:
                    #unpack list
                    value = value[0]
                else:
                    value = ""
                
                setattr(record, attribute, value)
                
            print(vars(record))
       
    return {
            'datasets' : parsed_records,
    }

'''
parse commandline args and return a dictionary
'''
def parse_args (argv):
    
    DEFAULT_CSW_ENDPOINT = 'http://cida.usgs.gov/gdp/csw/'
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


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
