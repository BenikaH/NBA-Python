# -*- coding: utf-8 -*-
"""
Created on Fri Feb 05 11:13:09 2016

@author: pfenerty
"""
import pandas as pd
import json
import urllib2

#get JSON from API url and store to pandas df
def j2p(url,index):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    data = json.loads(response.read())
    headers = data['resultSets'][index]['headers']
    rows = data['resultSets'][index]['rowSet']
    data_dict = [dict(zip(headers, row)) for row in rows]
    return pd.DataFrame(data_dict)