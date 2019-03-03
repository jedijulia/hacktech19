#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 10:57:50 2019

@author: vivekmishra
"""
import os
import sys
from optparse import OptionParser
import json
import pandas as pd

#sys.path.insert(0, '%s/../' % os.path.dirname(__file__))


#from common import dump

#import ebaysdk

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
        from ebaysdk.finding import Connection as finding
        #return(search)    
        try:
            api = finding(debug=False, appid=None, domain='svcs.ebay.com',
                          config_file='ebay.yaml', warnings=True)
    
            api_request = {
                #'keywords': u'niño',
                'keywords': str(search),
                'affiliate': {'trackingId': 1},
                'sortOrder': 'CountryDescending',
                'outputSelector':'AspectHistogram'
            }
    
            response = api.execute('findItemsAdvanced', api_request)
    
            return(response)
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
            
    def get_singeItem(self,itemID):
        from ebaysdk.shopping import Connection as Shopping
        api = Shopping(debug=True, appid=None,
                          config_file='ebay.yaml', warnings=True)
        
        response = api.execute('GetSingleItem',{'ItemID':itemID, 'IncludeSelector':'ItemSpecifics,Details'})
    
        return response
    
    def getAppendedResults(self,search_results):
        appended_list = []
        for item in search_results:
            temp = {}
            temp['gallleryURL'] = item['galleryURL']
            temp['itemId'] = item['itemId']
            temp['title'] = item['title']
            temp['price'] = item['sellingStatus']['currentPrice']['value']
            #Material
            resp = self.get_singeItem(temp['itemId'])
            #return(resp)
            resp = resp.json()
            resp = json.loads(resp)
            Item = resp['Item']
            specifics = Item['ItemSpecifics']        
            listval = specifics['NameValueList']
            for item in listval:
                name = item['Name']
                if name == 'Material':
                    material = item['Value']
                    
            temp['material'] = material
            #print(material)
            #Get emission for this material
            if 'Nylon' in material or 'Resin' in material or 'Paper' in material or 'Jute' in material or 'Plastic' in material or 'Glass' in material or 'Aluminum' in material or 'Steel' in material:  
                #appended_list.append(temp)
                #Find emission
                #reference_set = pd.read_csv('emission.csv')
                #Sake of avoiding writing code to search through 4 columns hard coding values
                if 'Nylon' in material:
                    temp['emission'] = 7.9
                elif 'Resin' in material:
                    temp['emission'] = 3.67
                elif 'Paper' in material:
                    temp['emission'] = 2.42
                elif 'Jute' in material:
                    temp['emission'] = 0.76
                elif 'Plastic' in material:
                    temp['emission'] = 3.56
                elif 'Glass' in material:
                    temp['emission'] = 4.4
                elif 'Aluminum' in material:
                    temp['emission'] = 11.89
                elif 'Steel' in material:
                    temp['emission'] = 3.64
                    
                appended_list.append(temp)
                
        return appended_list
    