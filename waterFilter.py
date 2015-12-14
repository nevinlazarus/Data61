#!/usr/bin/python

#takes in the water consumption dataset and filters out 'unnecesary' data.
#will create 2 CSV files. One with details, another with consumption data over time.

import csv
import os
import re
#first create the dict and read data from the general info csv
# obtain: propID, propType

if __name__ == '__main__':
	files = {'D3_MULTI_MIXED_PTBL.csv', 'D3_MULTI_NONRES_PTBL.csv', 'D3_MULTI_RES_PTBL_NEW.csv', 'D3_NONRES_PTBL.csv', 'D3_SD_PTBL.csv'}
	
	write =csv.writer(open("WaterDemand/WaterConsumption.csv", "wb"))

	i = 0;
	j = 0;
	for f in files:
		print "adding "+f+"..."
		name = "WaterDemand/"+f
		read = csv.reader(open(name,"rb"))
		for row in read:
			if(i == 0 and j == 0):
				head=[]
				for col in row:
					z = re.search(r'N_PROP', col)
					if(z):
						head.append('PROP_ID')
					m = re.search(r'PTBL_(.*)', col)
					if(m):
						head.append(m.group(1))
				write.writerow(head)

			else:
				write.writerow(row)
			j = j+1
		i=i+1
	print "Writing process complete!"

