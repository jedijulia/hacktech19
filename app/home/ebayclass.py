#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 10:57:50 2019

@author: vivekmishra
"""
import os
import sys
from optparse import OptionParser

#sys.path.insert(0, '%s/../' % os.path.dirname(__file__))


#from common import dump

#import ebaysdk
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError

class mainBay():
    def init_options(self):
        return("hello","swallow")
        #usage = "usage: %prog [options]"
        parser = OptionParser()
    
        parser.add_option("-d", "--debug",
                          action="store_true", dest="debug", default=False,
                          help="Enabled debugging [default: %default]")
        parser.add_option("-y", "--yaml",
                          dest="yaml", default='ebay.yaml',
                          help="Specifies the name of the YAML defaults file. [default: %default]")
        parser.add_option("-a", "--appid",
                          dest="appid", default=None,
                          help="Specifies the eBay application id to use.")
        parser.add_option("-n", "--domain",
                          dest="domain", default='svcs.ebay.com',
                          help="Specifies the eBay domain to use (e.g. svcs.sandbox.ebay.com).")
    
        (opts, args) = parser.parse_args()
        
        return(opts, args)

    def run(self,search):

        #return(search)    
        try:
            api = finding(debug=False, appid=None, domain='svcs.ebay.com',
                          config_file='ebay.yaml', warnings=True)
    
            api_request = {
                #'keywords': u'niño',
                'keywords': str(search),
                'affiliate': {'trackingId': 1},
                'sortOrder': 'CountryDescending',
            }
    
            response = api.execute('findItemsAdvanced', api_request)
    
            return(response)
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
    