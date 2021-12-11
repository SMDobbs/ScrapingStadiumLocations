## This is a python script to scrape NFL stadium locations and then use a library to convert the given city/state combination to
## to provide estimated lat long locations for each stadium. 

#This loads in all requested libraries for the script
import requests #library used for scraping
import lxml.html as lh
import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
from geopy.exc import GeocoderTimedOut #library for location coversion to lat & long
from geopy.geocoders import Nominatim #library for location coversion to lat & long
from opencage.geocoder import OpenCageGeocode #library for location coversion to lat & long

#scrape the tables from wikipedia site
nfl_stadium = "https://en.wikipedia.org/wiki/List_of_current_National_Football_League_stadiums"

def scrapetable(wikiurl):
    table_class="wikitable sortable jquery-tablesorter"
    response=requests.get(wikiurl)
    soup = BeautifulSoup(response.text, 'html.parser')
    table=soup.find('table',{'class':"wikitable"})
    df=pd.read_html(str(table))
    df=pd.DataFrame(df[0])
    return df

nfltable = scrapetable(nfl_stadium)

df = pd.DataFrame(nfltable)

def lat(location):
    key = '0670737b84384f99a437bc60eaa6dbde'
    geocoder = OpenCageGeocode(key)
    results = geocoder.geocode(location)
    lat = results[0]['geometry']['lat']
    return(lat)

def long(location):
    key = '0670737b84384f99a437bc60eaa6dbde'
    geocoder = OpenCageGeocode(key)
    results = geocoder.geocode(location)
    lng = results[0]['geometry']['lng']
    return(lng)
    

columns_wanted = df[["Name", "Location", "Surface", "Roof type", "Team(s)"]]

columns_wanted['Lat'] = df.apply(lambda columns_wanted: lat(columns_wanted['Location']), axis=1)
columns_wanted['Long'] = df.apply(lambda columns_wanted: long(columns_wanted['Location']), axis=1)

columns_wanted
