import csv, datetime

tripData = csv.reader(open("allTripData.csv", "rt"))
header = next(tripData)
seasonIdx = header.index("Season")
dateIdx = header.index("Start date")
hours = ["0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", \
"7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", \
"15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
seasonDateDict = {}

i = 0
for row in tripData:
	i += 1
	if i % 10000 == 0:
		print("Row: %i" % (i))
	startDate = datetime.datetime.strptime(row[dateIdx], "%m/%d/%Y %H:%M")
	hourOfDay = datetime.datetime.strftime(startDate, "%H")

	try:
		seasonDateDict[row[seasonIdx]][hourOfDay]+=1
	except(KeyError):
		try:
			seasonDateDict[row[seasonIdx]][hourOfDay] = 1
		except(KeyError):
			seasonDateDict[row[seasonIdx]] = {hourOfDay : 1}

seasons = list(seasonDateDict.keys())
seasons.sort()

print("""
Hour |  2010  |  2011  |  2012  |  2013  |  2014  |  2015  |  2016  |
-----+--------+--------+--------+--------+--------+--------+--------+""")

row = "%s | %s | %s | %s | %s | %s | %s | %s |"

print(seasonDateDict)
printDict = {}
for season in seasons:
	hourVals = []
	for hour in range(24):
		hourVals.append(seasonDateDict[season][str(hour).zfill(2)])

	total = sum([int(i) for i in hourVals])

	printVals = []
	for val in hourVals:
		printVals.append("{:.2%}".format(val/total).zfill(6))

	printDict[season] = printVals

for hr in hours:
	vals = []
	for season in ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]:
		vals.append(printDict[season][hours.index(hr)])
	print(row % (hr, vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6]))


