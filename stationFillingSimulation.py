import csv, datetime, time
import random as r

debug = True

#############
#Assumptions#
#############
#Starting Capacity = How many bikes are at the station to start every day
#Refill amount = How many bikes are added when capacity goes to -1
#Removal amount = How many bikes are removed when capacity goes to cap + 1
#Bikes (dis)appear from / to thin air.
#Every day starts with the same amount of bikes (no forecasting)
#Trying to reduce refill / removal occurrences

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

def runStationSimulation(station, curRunCapacity):
	print("Running simulation for %s @ %i bikes" % (station, curRunCapacity))
	fitness = 0
	maxCapacity = stationCapacityDict[station]

	reader = csv.reader(open("allTripData.csv", "rt"))

	header = next(reader)
	dateIdx = header.index("Start date")
	stIdx = header.index("Start terminal")
	endIdx = header.index("End terminal")

	currentFill = curRunCapacity
	curDate = "1/1/1900"
	i = 0
	for row in reader:
		i+=1
		if i%100000 == 0:
			print("%i/%i = %.2f%%" % (i, 2240000, (i/2240000)*100))
		if row[dateIdx] != curDate:
			currentFill = curRunCapacity
			curDate = row[dateIdx]

		if row[stIdx] == station:
			currentFill-=1
		elif row[endIdx] == station:
			currentFill+=1

		if currentFill < 0:
			fitness-=1
			currentFill = int(refillRate*maxCapacity)

		if currentFill > maxCapacity:
			fitness-=1
			currentFill = int((1 - reductionRate)*maxCapacity)


	return fitness

def main():
	buildCapacityDict()

	#Start out with filling each station with half it's capacity
	solution = {}

	curStationIdx = 0
	attemptsMade = 0
	stations = list(stationCapacityDict.keys())
	stations.sort()
	#Go through each station
	while curStationIdx < len(stations):
		station = list(stations)[curStationIdx]

		curBestCapacity = stationCapacityDict[station]//2
		curBestFitness = runStationSimulation(station, curBestCapacity)

		lastMin = -1
		lastMax = stationCapacityDict[station]+1
		sRunMin = 0
		sRunMax = stationCapacityDict[station]

		stillHaveAttempts = True
		if debug:
			print(station)
			print(stationCapacityDict[station])
			print(sRunMin)
			print(sRunMax)

		while stillHaveAttempts and curBestFitness != 0:
			mid = (sRunMax+sRunMin)//2
			#TODO: Change this
			#Example: Min-Mid-Max = 11-14-17
			#Change was 7 when it should be 3 (Maybe: incChange = (max-mid)//2)
			change = mid//2
			incCapacity = min(lastMax, mid+change)
			decCapacity = max(lastMin, mid-change)
			#Run an increase in capacity at that station
			incFitness = runStationSimulation(station, incCapacity)

			#Run a decrease in capacity at that station
			decFitness = runStationSimulation(station, decCapacity)


			if debug:
				print("---------")
				print(station)
				print("Min: "+str(sRunMin))
				print("Max: "+str(sRunMax))
				print("Mid: "+str(mid))
				print("Change: "+str(change))
				print("incCapacity: "+str(incCapacity))
				print("decCapacity: "+str(decCapacity))
				print("curBestCapacity: "+str(curBestCapacity))
				print("--")
				print("incFitness: "+str(incFitness))
				print("decFitness: "+str(decFitness))
				print("curBestFitness: "+str(curBestFitness))


			#If either were better than doing nothing, Update best solution & fitness
			if incFitness > curBestFitness:
				curBestCapacity = incCapacity
				curBestFitness = incFitness

			if decFitness > curBestFitness:
				curBestCapacity = decCapacity
				curBestFitness = decFitness

			#If increase was better than decrease
			if incFitness > decFitness:
				#Modify sRunMin
				#sRunMin = mid+change
				sRunMin = max(sRunMin, mid)

			#If decrease was better than increase
			elif decFitness > incFitness:
				#Modify sRunMax
				#sRunMax = mid-change
				sRunMax = min(sRunMax, mid)

			else:
				print("Fitnesses equaled! Flipping a coin.")
				if r.random() > .5:
					sRunMin = max(sRunMin, mid)
				else:
					sRunMax = min(sRunMax, mid)

			#If we're out of attempts, go to next station
			if sRunMax == sRunMin:
				stillHaveAttempts = False

			if lastMin == sRunMin and lastMax == sRunMax:
				stillHaveAttempts = False
			else:
				lastMin = sRunMin
				lastMax = sRunMax

		solution[station] = curBestCapacity
		print("Current Solution")
		print(solution)
		curStationIdx+=1



stationCapacityDict = {}
refillRate = .5
reductionRate = .3
main()
