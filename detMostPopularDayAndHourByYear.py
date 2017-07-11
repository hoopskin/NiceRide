import csv, datetime

tripData = csv.reader(open("allTripData.csv", "rt"))
header = next(tripData)
seasonIdx = header.index("Season")
dateIdx = header.index("Start date")
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
hours = ["0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", \
"7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", \
"15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
seasonDateDict = {}

i = 0
for row in tripData:
	i += 1
	if i % 10000 == 0:
		print("%i/%i = %.2f%%" % (i, 2240000, (i/2240000)*100))
	startDate = datetime.datetime.strptime(row[dateIdx], "%m/%d/%Y %H:%M")
	dayOfWeek = datetime.datetime.strftime(startDate, "%a")
	hourOfDay = datetime.datetime.strftime(startDate, "%H")
	key = dayOfWeek+" @ "+hours[int(hourOfDay)]
	
	try:
		seasonDateDict[row[seasonIdx]][key]+=1
	except(KeyError):
		try:
			seasonDateDict[row[seasonIdx]][key] = 1
		except(KeyError):
			seasonDateDict[row[seasonIdx]] = {key : 1}

seasons = list(seasonDateDict.keys())
seasons.sort()

oFile = open("seasonDayHourResults.csv", "wt")
writer = csv.writer(oFile)
writer.writerow(["Season", "Day", "Hour", "Count"])

print("Writing Results to File")
for s in seasons:
	for d in days:
		for h in hours:
			writer.writerow([s, d, h, seasonDateDict[s][d+" @ "+h]])

oFile.close()