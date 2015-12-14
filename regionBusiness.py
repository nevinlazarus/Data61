#!/usr/bin/python
import shapefile
from shapely.geometry import Point
from shapely.geometry import Polygon
import re
import csv
import json
import sys
import operator
from rtree import index

def main():
    
    area_type = "SA2"
    filename = "2011_" + area_type + "_shape/" + area_type + "_2011_AUST" #shapefile name
    state_code = '1'    #state code for NSW            
    stateIndex = 1;            
    if (area_type == "SA2"): #adjust the location of the field based on different file layouts
        stateIndex = 2    
    
    business_type = "establishment"
  
    reader = csv.reader(open("establishmentwithSA1.csv"))
    writer = csv.writer(open("establishmentwithSA2.csv", "wb"));
    myfile = sorted(reader, key=operator.itemgetter(1)) #sort by coordinates so that the points are somewhat localised
    
    foundregions = [] #acts as a cache
    locations = {} #dict of the regions business distribution
    errorfile = open("err.txt", "w+")        
    sf = shapefile.Reader(filename) #open the shapefile
    shapes = sf.shapeRecords() #list of shapes and their records
    fields = sf.fields    
    idx = index.Index()
    
    for i, shape in enumerate(shapes): #creates an index of the shapes
        if len(shape.shape.points) == 0: #malformed shape, just skip over it
            idx.insert(i, [0, 0, 0, 0])
        else:
            idx.insert(i, shape.shape.bbox)
        if shape.record[stateIndex] != state_code: break #since NSW are the first regions in the file
        
    coordIndex = 1    
    typeIndex = 3
    addressIndex = 2
    
    count = 0
    for line in myfile:        #for each record in the csv file
        coord = line[coordIndex].split(",")        
        if len(coord) < 2: break; #cannot read valid a coord pair
        
        
        point = Point(float(coord[1]), float(coord[0])) #creates a latitude, longitude pair             
        locationID = findRecord(idx, shapes, point, stateIndex, state_code)            
        types = line[typeIndex].split('/')
        if not locations.has_key(locationID): #key missing
            locations[locationID] = {} 
        for place_type in types: #for each type of business maintains a counter
            if not locations[locationID].has_key(place_type): # key missing
                locations[locationID][place_type] = 0
            locations[locationID][place_type] += 1        
        tmp = line;
        tmp.append(locationID)
        writer.writerow(tmp);
        count += 1
        print count, ":", locationID
        if (locationID == 0): #cannot assign point to one of the regions
            errorfile.write(line[addressIndex] + "\n");                           
            print line[addressIndex]
            exit() #we don't want there to be any misses!


            
    out = json.dumps(locations) #dump dict to a json file
    outfile = open(business_type + "_count" + area_type + ".txt", "w+") #writes json to output file
    outfile.write(out)
    outfile.close();
    errorfile.close()

#takes in a point        
#returns the id / name of the region which contains the point
def findRecord(idx, shapes, point, stateIndex, state_code):
    
    intersection_list = list(idx.intersection((point.bounds))) #gets list of possible intersections using the index
    
    #margin of error
    #start with no error margin, then slowly expands error radius until a suitable region is found
    for buffer_distance in range(1, 100): #it should never get to more than 20, but it its best to be safe
        bd = float(buffer_distance / 5000.0); #makes it into a float
        for s in intersection_list:  #for each possible intersection
            if point.buffer(bd).intersects(Polygon(shapes[s].shape.points)): #finds the region the point is actually in                                
                return shapes[s].record[stateIndex-1] #returns the location name
        
        intersection_list = list(idx.intersection((point.buffer(bd).bounds))) #gets list of possible intersections using the index
        print buffer_distance
        
    print intersection_list
    return 0 #if we can't figure out which region its in

main()  
