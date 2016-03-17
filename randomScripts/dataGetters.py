# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 12:48:48 2016

@author: pfenerty
"""

import pandas as pd
import json
import urllib2

def j2p(url,index):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    data = json.loads(response.read())
    headers = data['resultSets'][index]['headers']
    rows = data['resultSets'][index]['rowSet']
    data_dict = [dict(zip(headers, row)) for row in rows]
    return pd.DataFrame(data_dict)
    
def getJson(url,index):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    data = json.loads(response.read())
    data = data['resultSets'][index]['rowSet']
    return data