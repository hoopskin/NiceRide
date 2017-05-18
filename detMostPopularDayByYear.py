import csv, datetime

tripData = csv.reader(open("allTripData.csv", "rt"))
header = next(tripData)
seasonIdx = header.index("Season")
dateIdx = header.index("Start date")
seasonDateDict = {}

i = 0
for row in tripData:
	i += 1
	if i % 10000 == 0:
		print("Row: %i" % (i))

	startDate = datetime.datetime.strptime(row[dateIdx], "%m/%d/%Y %H:%M")
	dayOfWeek = datetime.datetime.strftime(startDate, "%A")

	try:
		seasonDateDict[row[seasonIdx]][dayOfWeek]+=1
	except(KeyError):
		try:
			seasonDateDict[row[seasonIdx]][dayOfWeek] = 1
		except(KeyError):
			seasonDateDict[row[seasonIdx]] = {dayOfWeek : 1}

seasons = list(seasonDateDict.keys())
seasons.sort()

print("""
Season | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday |
-------+--------+---------+-----------+----------+--------+----------+--------+""")

row = " %s  | %s | %s  |  %s   |  %s  | %s |  %s  | %s |"

for season in seasons:
	monVal = seasonDateDict[season]["Monday"]
	tueVal = seasonDateDict[season]["Tuesday"]
	wedVal = seasonDateDict[season]["Wednesday"]
	thuVal = seasonDateDict[season]["Thursday"]
	friVal = seasonDateDict[season]["Friday"]
	satVal = seasonDateDict[season]["Saturday"]
	sunVal = seasonDateDict[season]["Sunday"]

	total = sum([monVal, tueVal, wedVal, thuVal, friVal, satVal, sunVal])

	monVal = "{:.2%}".format(monVal/total).zfill(6)
	tueVal = "{:.2%}".format(tueVal/total).zfill(6)
	wedVal = "{:.2%}".format(wedVal/total).zfill(6)
	thuVal = "{:.2%}".format(thuVal/total).zfill(6)
	friVal = "{:.2%}".format(friVal/total).zfill(6)
	satVal = "{:.2%}".format(satVal/total).zfill(6)
	sunVal = "{:.2%}".format(sunVal/total).zfill(6)

	print(row % (season, monVal, tueVal, wedVal, thuVal, friVal, satVal, sunVal))