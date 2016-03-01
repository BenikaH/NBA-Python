# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 12:04:55 2016

@author: pfenerty
"""

import json
import urllib2

def get_json(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    data = json.loads(response.read())
    return data
    
class location:
    def __init__(self, city, state, zipc, lat, lon, elev):        
        self.city = city
        self.state = state
        self.zip = zipc
        self.lat = lat
        self.long = lon
        self.elev = elev
        
class temp:
    def __init__(self,f,c):
        self.f = f
        self.c = c
        
class wind:
    def __init__(self,desc,direction,deg,mph,gmph):
        self.description = desc
        self.direction = direction
        self.degree = deg
        self.speed = mph
        self.gustSpeed = gmph

class pressure:
    def __init__(self,mb,inch):
        self.millibars = mb
        self.inches = inch
        
class 

class City_Weather:
    url = "http://api.wunderground.com/api/f65ecaa665e30e69/conditions/q/{state}/{City}.json"

    def __init__(self, city, state):
        fullData = get_json(self.url.format(state = state, City = city))
        ld = fullData['current_observation']['display_location']
        self.location = location(ld['city'],ld['state'],ld['zip'],ld['latitude'], \
                                 ld['longitude'],ld['elevation'])    
    class location:
        def __init__(self, city, state, zipc, lat, lon, elev):        
            self.city = ""
            self.state = ""
            self.zipc = ""
            self.lat = ""
            self.lon = ""
            self.elev = ""    
        
        
SanFran = City_Weather("San_Fransisco", "CA")       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

