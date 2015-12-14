#!/usr/bin/python
from lxml import html
import requests
import re
import sys
import urllib
import csv
import shapefile


def main():

    w = shapefile.Writer(shapefile.POINT)
    #coord_file = open("sydney_final"); #my input coordinate file
    
    fields = ["Name", "Address", "Type", "Rating", "Cost"]
    
    w.field("Name", "C", "50")
    w.field("Address", "C", "50")
    w.field("Type", "C", "40")
    w.field("Rating", "C", "5")
    w.field("Cost", "C", "20")
    csv_name = "combinedestablishment.csv"
    
    count = 0
    with open(csv_name) as p:
        reader = csv.DictReader(p)
        #create fields in the shapefile
        
                
        #for each row in the csv, makes an entry in the shapefile
        for row in reader:                     
            #reads the coordinate pair from my input
            #coord = coord_file.readline().rstrip().split(',')
            coord = row["Coordinates"].split(",");
            if len(coord) < 2:  
                continue
            #copies the fields from the csv to the shapefile
            w.record(row["Name"], row["Address"], row["Type"], row["Rating"], row["Cost"])
            #writes the coordinates to the shapefile
            w.point(float(coord[1]), float(coord[0]))
            count += 1
            print count

    w.save("establishment.shp")


main()
