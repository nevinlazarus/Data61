#!/usr/bin/python
import requests
import re
import sys
import urllib
import csv
import shapefile


def main():
    #inputed address
    #address = sys.stdin.readline()

    #getLatLong(longitude, latitude, address)
    makeShapeFile()

def getLatLong(coord, address):
    
    #formats the string to make it a valid url
    address = urllib.quote(address, safe='') 
    #forms the http request
    httpRequest = "https://maps.googleapis.com/maps/api/geocode/json?address="  + address 
    
    #gets the page

    page = requests.get(httpRequest) 

    content = page.content.split('\n');
    
    latitude = 0
    longitude = 0
    for line in content:
        #find matches for latitude and longitude
        
        if re.search("lat", line):
            line = re.sub('.*: ', '', line)
            line = re.sub(',.*', '', line)
            latitude = line
        if re.search("lng", line):
            line = re.sub('.*: ', '', line)
            line = re.sub(',.*', '', line)
            longitude = line
            #longitude is after latitude in the file
            break

    coord.append(float(longitude))
    coord.append(float(latitude))
    
    
    
def makeShapeFile():
    w = shapefile.Writer(shapefile.POINT)
    #fields in the csv file
    
    fields = ["ADDRESS", "SALE PRICE", "SALE DATE", "AREA", "STRATA/NON STRATA", "MULTI-PROPERTY SALE (Y/N)", "PROPERTY NUMBER", "DEALING NUMBER"]
    
        
    
    with open("SYDNEY_2000.csv") as p:
        reader = csv.DictReader(p)
        i = 0
        for row in reader:
            for field in row.keys():
                w.field(field, "C", "40")
            break
        for row in reader:                    
            address = row["ADDRESS"]            
            coord = []
            myfield = []
            for field in row:
                
                myfield.append(row[field])
            
            
            #getLatLong(coord, address)            
            
            coord.append(150.0 + (i % 100)/10)
            coord.append(-32.0 + i / 1000)
            if coord[0] == 0:
                break;
            print i
            if i == 999:
                break
            w.record(*myfield)            
            w.point(*coord)
            
            #print i, ": ", coord[0], coord[1]
            i += 1
            
            #2503    
            

    w.save("test.shp")
    
main()
