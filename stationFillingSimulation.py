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

def runStationSimulation(capacityDict):
	fitness = 0
	time.sleep(.5)
	fitness = r.randint(-1000,0)
	#If we're going station at a time, can we skip all the unnecessary rows?

	return fitness

def main():
	buildCapacityDict()

	#Start out with filling each station with half it's capacity
	curBestSolution = {k: v//2 for k, v in stationCapacityDict.items()}
	curBestFitness = runStationSimulation(curBestSolution)


	curStationIdx = 0
	attemptsMade = 0
	#Go through each station
	while curStationIdx < len(stationCapacityDict.keys()):
		station = list(stationCapacityDict.keys())[curStationIdx]
		sRunMin = 0
		sRunMax = stationCapacityDict[station]
		curRunSolution = {k: v//2 for k, v in stationCapacityDict.items()}
		stillHaveAttempts = True
		if debug:
			print(station)
			print(stationCapacityDict[station])
			print(sRunMin)
			print(sRunMax)

		while stillHaveAttempts:
			#Run an increase in capacity at that station
			curRunSolution[station] = (sRunMin+sRunMax)//2
			curRunSolution[station] += (sRunMax-sRunMin)//2
			incFitness = runStationSimulation(curRunSolution)

			#Run a decrease in capacity at that station
			curRunSolution[station] = (sRunMin+sRunMax)//2			
			curRunSolution[station] -= (sRunMax-sRunMin)//2

			decFitness = runStationSimulation(curRunSolution)


			if debug:
				print("---------")
				print(station)
				print("Min: "+str(sRunMin))
				print("Max: "+str(sRunMax))
				print(sRunMax == sRunMin)
				print("curBestSolution[station]: "+str(curBestSolution[station]))
				print("--")
				print("incFitness: "+str(incFitness))
				print("decFitness: "+str(decFitness))
				print("curBestFitness: "+str(curBestFitness))


			#If either were better than doing nothing, Update best solution & fitness
			if incFitness > curBestFitness:
				curRunSolution[station] = (sRunMin+sRunMax)//2
				curRunSolution[station] += (sRunMax-sRunMin)//2

				curBestSolution = {k: v for k, v in curRunSolution.items()}
				curBestFitness = incFitness

			if decFitness > curBestFitness:
				curRunSolution[station] = (sRunMin+sRunMax)//2			
				curRunSolution[station] -= (sRunMax-sRunMin)//2
				
				curBestSolution = {k: v for k, v in curRunSolution.items()}
				curBestFitness = decFitness

			#If increase was better than decrease
			if incFitness > decFitness:
				#Modify sRunMin
				sRunMin = ((sRunMin+sRunMax)//2)+((sRunMax-sRunMin)//2)

			#If decrease was better than increase
			elif decFitness > incFitness:
				#Modify sRunMax
				sRunMax = ((sRunMin+sRunMax)//2)-((sRunMax-sRunMin)//2)

			else:
				print("Fitnesses equaled!")

			#If we're out of attempts, go to next station
			if sRunMax == sRunMin:
				stillHaveAttempts = False

		curStationIdx+=1


stationCapacityDict = {}
main()