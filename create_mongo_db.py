import csv
from pymongo import MongoClient

mongo_db = "MyDB"
mongo_coll = "FirstCollection"

global_mongo = MongoClient()
global_db = global_mongo[mongo_db]
global_coll = global_db[mongo_coll]

def string_to_float(s):
	try:
		return float(s)
	except ValueError:
		return -1.0

def string_to_int(s):
	try:
		return int(s)
	except ValueError:
		return -1

csvfile = open('C://Users//Chris//Desktop//Case2nd.csv', 'rt')

reader = csv.reader(csvfile, delimiter= '\t')

counter = 0

for row in reader:

	if counter != 0:
		#each row will be a document in the DB
		#for each row start with an empty doc
		doc = {}
		doc["MyCounter"] = counter - 1

		#if counter <5:
		#		print(row)
		
		#row is of the form: row = ['scenarioID','MOid',...]
		#use a counter so that we can manipulate easier the row
		#e.g. if i == 0 skip that since this will be the scenarioID and we may
		#not need this...anyways below
		realX = None
		realY = None
		for i in range(len(row)):

			if ';' not in row[i]:

				if i == 0:
					doc["scenarioID"] = string_to_int(row[i])
				elif i==1:
					doc["MOid"] = string_to_int(row[i])
				elif i==2: 
					doc["MPid"] = string_to_int(row[i]) 
				elif i==3:
					doc["edgeID"] = string_to_int(row[i])
				elif i==4:
					#doc['realX'] = string_to_float(row[i])
					realX = string_to_float(row[i])
				elif i==5:
					#we may need to split the y cooridnate
					vals = row[i].split(' ')
					if len(vals) == 1:
						#doc['realY'] = string_to_float(vals[0])
						realY = string_to_float(vals[0])
					elif len(vals) >= 2:
						#doc['realY'] = string_to_float(vals[0])
						realY = string_to_float(vals[0])
			else:
				#the character ; is in the string
				vals = row[i].split(';')

				#the second string is the date and the time
				date_time_string = vals[1].split(' ')
				
				#put the date in the doc
				doc['date'] = date_time_string[0]

				#the time is the second entry
				time_str = date_time_string[1].split(':')
				doc['time'] = [{'hours':string_to_int(time_str[0])},
											 {'mins':string_to_int(time_str[1])},{'secs':string_to_float(time_str[2])}]
				doc['duration'] = string_to_int(time_str[0])*3600+string_to_int(time_str[1])*60+string_to_float(time_str[2])

				#the remaining entries of the row are the episodes
				episodes = vals[2:]
				doc['episodes'] = episodes
				if counter == 40:
					#print(row)
					print(vals)
					print(episodes)
					#print(date_time_string)
					#print(time_str)
					
		#insert in the collection the document
		if realX == None or realY == None:
			raise ValueError("realX or realY is None")
		doc['loc'] = {"x":realX,"y":realY}
		global_coll.insert(doc)
		if counter == 40:
			print(doc)      

	counter += 1
#    global_coll.insert(row)
