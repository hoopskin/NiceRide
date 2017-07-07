import csv, datetime

def buildCapacityDict():
	global stationCapacityDict

	#Go through station data and build an ID:Capacity dictionary

	reader = csv.reader(open("allStationData.csv", "rt"))

	header = next(reader)
	terminalIdx = header.index("Terminal")
	capacityIdx = header.index("Nb docks")

	for row in reader:
		try:
			val = int(row[capacityIdx])
		except(ValueError):
			continue

		try:
			stationCapacityDict[row[terminalIdx].strip()] = max(stationCapacityDict[row[terminalIdx].strip()], val)
		except(KeyError):
			stationCapacityDict[row[terminalIdx].strip()] = val

def detCapacityMinMax():
	#Initialize variables
	curStationCapacity = {k: 0 for k, v in stationCapacityDict.items()}
	minMaxCapacity = {k: [0,0] for k, v in stationCapacityDict.items()}

	#Start reading trip data
	reader = csv.reader(open("allTripData.csv", "rt"))
	#Capture header
	header = next(reader)

	#Capture Indexes
	dateIdx = header.index("Start date")
	stTerminal = header.index("Start terminal")
	endTerminal = header.index("End terminal")

	lastDate = "1/1/1900"
	i = 0
	#For row in data
	for row in reader:
		i+=1
		if i % 100000 == 0:
			print("%i/%i = %.2f%%" % (i, tripDataRowSize, ((i/tripDataRowSize)*100)))
		
		#if row[dateIdx][:row[dateIdx].index(" ")] == "9/10/2011":
		#	print("%s\t->\t%s" % (row[stTerminal], row[endTerminal]))

		#If new day, reset curStationCapacity
		if row[dateIdx][:row[dateIdx].index(" ")] != lastDate:
			curStationCapacity = {k: 0 for k, v in stationCapacityDict.items()}
			lastDate = row[dateIdx][:row[dateIdx].index(" ")]

		#Add and reduce capacities for this ride
		try:
			curStationCapacity[row[stTerminal]] -= 1
			#If min/max modifications needed, make them
			if curStationCapacity[row[stTerminal]] < minMaxCapacity[row[stTerminal]][0]:
				minMaxCapacity[row[stTerminal]][0] = curStationCapacity[row[stTerminal]]
		except(KeyError):
			#print(row)
			pass

		try:
			curStationCapacity[row[endTerminal]] += 1
			if curStationCapacity[row[endTerminal]] > minMaxCapacity[row[endTerminal]][1]:
				minMaxCapacity[row[endTerminal]][1] = curStationCapacity[row[endTerminal]]
				#if row[endTerminal] == "30158":
				#	print("30158 moving up!")
				#	print(curStationCapacity[row[endTerminal]])
				#	print(row[dateIdx][:row[dateIdx].index(" ")])
		except(KeyError):
			#print(row)
			pass

	#For key, value in minMaxCapacity
	for k, v in minMaxCapacity.items():
		#Output results
		print("Station %s:\tMin: %i\tMax: %i" % (k, v[0], v[1]))

def main():
	buildCapacityDict()

	#First curiousity, what's the minimum / maximum the stations got to?
	detCapacityMinMax()
	#Results saved at 'minMaxStationCapacity.txt'

dtFormat = "%m/%d/%Y %H:%M"
stationCapacityDict = {}
tripDataRowSize = 2240726
main()