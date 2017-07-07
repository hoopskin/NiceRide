import csv, datetime, time
import random as r

debug = False

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
	fitness = 0
	time.sleep(.5)
	fitness = r.randint(-1000,0)

	return fitness

def main():
	buildCapacityDict()

	#Start out with filling each station with half it's capacity
	solution = {}

	curStationIdx = 0
	attemptsMade = 0
	#Go through each station
	while curStationIdx < len(stationCapacityDict.keys()):
		station = list(stationCapacityDict.keys())[curStationIdx]

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

		while stillHaveAttempts:
			mid = (sRunMax+sRunMin)//2
			change = mid//2
			incCapacity = mid+change
			decCapacity = mid-change
			#Run an increase in capacity at that station
			incFitness = runStationSimulation(station, incCapacity)

			#Run a decrease in capacity at that station
			decFitness = runStationSimulation(station, decCapacity)


			if debug:
				print("---------")
				print(station)
				print("Min: "+str(sRunMin))
				print("Max: "+str(sRunMax))
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
				print("Fitnesses equaled!")

			#If we're out of attempts, go to next station
			if sRunMax == sRunMin:
				stillHaveAttempts = False

			if lastMin == sRunMin and lastMax == sRunMax:
				stillHaveAttempts = False
			else:
				lastMin = sRunMin
				lastMax = sRunMax

		solution[station] = curBestCapacity
		curStationIdx+=1



stationCapacityDict = {}
refillRate = .5
reductionRate = .3
main()