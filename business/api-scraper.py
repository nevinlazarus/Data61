#!/usr/bin/python

import math
import urllib
import re
import requests
import json
import unicodedata

#returns

#top[0] = y
#top[1] = x
#takes in a number of points, 2 strings (coordinates), returns a list of coordinates
#the coordinates are listed as two lists, x coordinates, y coordinates. It is up to the 
#user to iterate through them
#
#When an area is defined by two points, top left and top right, this function will return
#a list of coordinates to search. The area is divided as evenly as possible. The number 
#of points will not match the input request perfectly, but so long as it is above 100
# it will never produce more points.
def getPoints(pts, topL, bottomR):
	bottom = bottomR.split(',')
	top = topL.split(',')

	lx = float(bottom[1])-float(top[1])
	ly = float(top[0])-float(bottom[0])
	print lx
	print ly
	ptDensity = math.sqrt((lx*ly)/(pts-(3.5*math.sqrt(pts))))
	print ptDensity

	x = float(top[1])
	i = 0
	xpts=[] 
	ypts=[]
	print x, float(top[1]), lx, ptDensity
	while (x < (float(top[1]) + lx)):
		x = float(top[1])+(i*ptDensity)
		#print x
		xpts.append(x)
		i = i+1


	i=0
	y = float(top[0])
	while (y > (float(top[0]) - ly)):
		y = float(top[0])-(i*ptDensity)
		ypts.append(y)
		i = i+1

	return xpts, ypts



#main function to test
if __name__ == '__main__':

	#parameters
	topL = "-33.856722,151.202227" # input
	bottomR = "-33.870596,151.210573" #input
	radius = "300"
	numPoints = 20
	shopType = "establishment"
	fileName=shopType+".txt"

	i = 0
	xpts, ypts = getPoints(numPoints, topL, bottomR)
	target = open(fileName, 'w+') 
	all_places = {}
	key = "AIzaSyBN1Ool_TDiEiVq2XGXRs-XNVknSDhEtF0"
	for x in xpts:
		for y in ypts:
			nextPage = ""
			pages = 0
			#print str(x)+","+str(y)

			#checks if there is a 'nextpage' available, if so it loads it, if not, terminates the loop
			while(pages < 1 or nextPage != ""):
				print i
				i += 1
				if(nextPage != ""):
					link = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=" + key + "&pagetoken='+str(nextPage)
					#reset nextPage variable
					nextPage = ""
				#if no next page, that means that it must be the fist page, so load the first page.
				else:
					link = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(y)+","+str(x)+"&types="+str(shopType)+"&key=" + key + "&rankby=distance"
				
				mypage = requests.get(link)
				j = json.loads(mypage.content)
				if j.has_key("next_page_token"): #if there is another page of results
					nextPage = j["next_page_token"]
				for result in j["results"]: #for each business
					all_places[result["place_id"]] = result #adds the business to the dict

				pages = pages+1
	print len(all_places)
	for place in all_places: #for each place found
		#write all the details to a csv file
		target.write(unicodedata.normalize('NFKD', all_places[place]["name"]).encode('ascii','ignore') + ";")
		if all_places[place].has_key("rating"):
			target.write(str(all_places[place]["rating"]) + ";")
		else:
			target.write("NoRating;")
		if all_places[place].has_key("price_level"):	
			target.write(str(all_places[place]["price_level"]) + ";")
		else:
			target.write("NoPrice;")
		target.write(str(all_places[place]["geometry"]["location"]["lat"]) + ",")
		target.write(str(all_places[place]["geometry"]["location"]["lng"]) + ";")
		target.write(all_places[place]["vicinity"] + ";")
		target.write(all_places[place]["place_id"] + ";")
		for mtype in all_places[place]["types"]:
			target.write(mtype + "/") #adds each business type
		target.write("\n")
	
	target.close()

	counter1 = 0;
	counter2 = 0;
	for x in xpts:
		print x
		counter1 = counter1+1

	for y in ypts:
		print y
		counter2 = counter2+1

	counter = counter1*counter2
	print counter




