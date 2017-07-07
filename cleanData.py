import csv, os

folderList = [f for f in os.listdir(os.curdir) if os.path.isdir(f) and f != ".git"]
folderList.sort()
tripDataFile = open("allTripData.csv", "wt")
stationLocationDataFile = open("allStationData.csv", "wt")

tripDataWriter = csv.writer(tripDataFile)
stationLocationDataWriter = csv.writer(stationLocationDataFile)

stationHeader = ["Season"]
tripHeader = ["Season"]
tripData = []

for season in folderList:
	print("Working on %s" % (season))
	stationFileName = [f for f in os.listdir(os.curdir+"/"+season) if f.lower().endswith("station_locations.csv") or f.lower().endswith("station-locations.csv")][0]
	tripFileName = [f for f in os.listdir(os.curdir+"/"+season) if f.lower().endswith("season.csv")][0]

	stationReader = csv.reader(open(season+"/"+stationFileName, "rt"))
	tripReader = csv.reader(open(season+"/"+tripFileName, "rt"))

	curFileStationHeader = next(stationReader)
	curFileTripHeader = next(tripReader)

	if stationHeader == ["Season"]:
		stationHeader.extend(curFileStationHeader)
		tripHeader.extend(curFileTripHeader)

		stationLocationDataWriter.writerow(stationHeader)
		tripDataWriter.writerow(tripHeader)

	for row in stationReader:
		oRow = [season]
		oRow.extend(row)
		stationLocationDataWriter.writerow(oRow)

	for row in tripReader:
		if row != ["","","","","","","0",""]:
			oRow = [season]
			oRow.extend(row)
			tripData.append("|".join(oRow))

tripData.sort()
for trip in tripData:
	tripDataWriter.writerow(trip.split("|"))

tripDataFile.close()
stationLocationDataFile.close()