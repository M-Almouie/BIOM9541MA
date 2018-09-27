#!/usr/bin/env python
# to calculate stance for forward: from (heel contact->toe off)
# to calculate stance for backwards: from (toe contact->heel off)

# for toe, if less than 45 mm and difference is less than 1 => beginning of back stance
# for heel, if less than 35 mm and difference is more than 1 => end of back stance

# for heel, if less than 35 mm and difference is less than 1 => beginning of forward stance
# for toe, if less than 45 mm and difference is more than 1 => end of forward stance

import sys,csv,re,math

list = []
# Gait times
gStart = 0
gFinish = 0

#Stance times
sStart = 0
sFinish = 0

#experiment total time
eStart = 0
eFinish = 0

#participant's weight 
weight = 76

def openCSV():
	csvfile = open(filename, 'rt')
	readCSV = csv.reader(csvfile, delimiter=',', quotechar='|')
	return readCSV
	
def findPara(type):
	if type == "time":
		index = 0
	elif type == "distance":
		index = 2
	elif type == "rHeel":
		index = 3	
	elif type == "rToe":
		index = 6	
	elif type == "hipFlex" or type == "hipExt":
		index = 8
	elif type == "kneeFlex" or type == "kneeExt":
		index = 11
	elif type == "ankDorsi" or type == "ankPlant":
		index = 14
	# moments are calculated for the z-axis for now maybe be wrong
	elif type == "ankMom":
		index = 28
	elif type == "kneeMom":
		index = 30
	elif type == "hipMom":
		index = 33
	elif type == "hipPower":
		index = 36
	elif type == "kneePower":
		index = 39
	elif type == "ankPower":
		index = 42
	return index

def res(index):
	readCSV = openCSV()
	i = 0
	
	for row in readCSV:
		if i <= 10:
			i = i+1
			continue
		if row == []:
			break
		else:
			list.append(row[index])
			i = i+1

def stanceF():
	readCSV = openCSV()
	i = 0
	bool = 0
	sStart = 0
	sFinish = 0
	gFinish = 0
	tick = 0
	for row in readCSV:
		if i <= 10 or bool > 0:
			i = i+1
			bool -= 1
			continue
		if row == []:
			break
		else:
			if float(row[3]) < 45.00 and tick == 0:
				sStart = row[0]
				bool = 50
				tick = 1
			elif float(row[6]) < 55.00 and tick == 1:
				sFinish = row[0]
				tick = 2
			elif float(row[3]) < 45.00 and tick == 2:
				gFinish = row[0]
				break
	gStart = sStart
	return [sStart,sFinish,gFinish]

def stanceB():
	readCSV = openCSV()
	i = 0
	bool = 0
	sStart = 0
	sFinish = 0
	gFinish = 0
	tick = 0
	for row in readCSV:
		if i <= 10 or bool > 0:
			i = i+1
			bool -= 1
			continue
		if row == []:
			break
		else:
			if float(row[6]) < 45.00 and tick == 0:
				sStart = row[0]
				bool = 50
				tick = 1
			elif float(row[3]) < 50.00 and tick == 1:
				sFinish = row[0]
				tick = 2
			elif float(row[6]) < 45.00 and tick == 2:
				gFinish = row[0]
				break
	gStart = sStart
	return [sStart,sFinish,gFinish]

def strideLen(gSta,gFin):
	readCSV = openCSV()
	i = 0
	temp1 = 0
	temp2 = 0
	for row in readCSV:
		if i <= 10:
			i = i+1
			continue
		if row == []:
			break
		else:
			if float(row[0]) == gSta:
				temp1 = float(row[2])
			if float(row[0]) == gFin:
				temp2 = float(row[2])
	return (temp2-temp1)

def maxExtension(sStart,sFinish,index):
	readCSV = openCSV()
	i = 0
	max = 10
	for row in readCSV:
		if i <= 10:
			i = i+1
			continue
		if row == []:
			break
		if float(row[0]) < sStart:
			continue
		else:
			if float(row[0]) > sFinish:
				break
			if max > float(row[index]):
				max = float(row[index])
	return max

def maxFlexion(sStart,sFinish,index):
	readCSV = openCSV()
	i = 0
	max = -9
	for row in readCSV:
		if i <= 10:
			i = i+1
			continue
		if row == []:
			break
		if float(row[0]) < sStart:
			continue
		else:
			if float(row[0]) > sFinish:
				break
			if max < float(row[index]):
				max = float(row[index])
	return max

def maxHipFlex(sStart):
	readCSV = openCSV()
	i = 0
	flex = 0
	for row in readCSV:
		if i <= 10 or float(row[0]) < sStart:
			i = i+1
			
			continue
		if row == []:
			break
		else:
			flex = row[7]
			break
	return float(flex)
	
def extensorMoment(sStart,sFinish,index):
	readCSV = openCSV()
	i = 0
	max = 2
	for row in readCSV:
		if i <= 10 or float(row[0]) < sStart:
			i = i+1
			continue
		if row == []:
			break
		else:
			if float(row[0]) > sFinish:
				break
			if max > float(row[index]) and abs(float(row[index])) < 1:
				max = float(row[index])
	return max

def flexorMoment(sStart,sFinish,index):
	readCSV = openCSV()
	i = 0
	max = -2
	for row in readCSV:
		if i <= 10 or float(row[0]) < sStart:
			i = i+1
			continue
		if row == []:
			break
		else:
			if float(row[0]) > sFinish:
				break
			if max < float(row[index]) and abs(float(row[index])) < 1:
				max = float(row[index])
	return max
#Main

filename = sys.argv[1]

#Forward files only
forPat = re.compile('Forward.*')
m = forPat.match(filename)
if m:
	stance = stanceF()
else:
	stance = stanceB()
gFinish = float(stance.pop())
# error value of 0.08 when calculating stance
sFinish = float(stance.pop())+0.08
sStart = float(stance.pop())
gStart = sStart
#res(index)

res(0)
eStart = float(list.pop(0))
eFinish = float(list.pop())
totalTime = eFinish-eStart

forPat = re.compile('Backward.*')
m2 = forPat.match(filename)
if m2:
	res(1)
else:
	res(2)
x1 = float(list.pop(0))
x2 = float(list.pop())
totalDist = x2-x1

# Anthropometric parameters
strideLength = float(strideLen(gStart,gFinish))
stepTime = sFinish-sStart
strideTime = 2*stepTime
cadence = 60/stepTime

#Kinematics
#Half of stance => loading response
#pre-swing => heel off,toe off reference foot before swing 
# Ankle
maxPlantLoading = maxExtension(sStart,sStart+(sFinish-sStart)/2,15)
maxDorsiStance = maxFlexion(sStart,sFinish,15)
maxPlantSwing = maxExtension(sStart,sFinish,15)
totalROMAnk = abs(maxPlantSwing)+abs(maxDorsiStance)
# Knee
maxFlexKneeLoading = maxFlexion(sStart,sStart+(sFinish-sStart)/2,10)
maxFlexKneeSwing = maxFlexion(sStart,gFinish,10)
totalROMKnee = abs(maxFlexKneeSwing)+abs(maxFlexKneeLoading)
# Hip
flexHipHeelStrike = maxHipFlex(sStart)
maxExtHipStance = maxExtension(sStart,sFinish,7)
totalROMHip = abs(maxExtHipStance)+abs(flexHipHeelStrike)

#Kinetics
#dorsi,extensor -> -, flexor,plantar -> +
#Ankle
maxDorsiMoment = extensorMoment(sStart,sFinish,27)
maxPlantMoment = flexorMoment(sStart,sFinish,27)
maxAnkPowerGen = maxFlexion(eStart,eFinish,42)
maxAnkPowerAbs = maxExtension(eStart,eFinish,42)
#Knee
maxKneeExtMoment = extensorMoment(sStart,sFinish,30)
maxKneeFlexMoment = flexorMoment(sStart,sFinish,30)
maxKneePowerGen = maxFlexion(eStart,eFinish,39)
maxKneePowerAbs = maxExtension(sStart,sStart+(sFinish-sStart)/2,39)
#Hip
maxHipExtMoment = extensorMoment(sStart,sFinish,33)
maxHipFlexMoment = flexorMoment(sStart,sFinish,33)
maxHipPowerGen = maxFlexion(sStart,sStart+(sFinish-sStart)/2,36)
maxHipPowerGen2 = maxFlexion(sStart,gFinish,36)


#Results
print("\n---------------------------------------------------\n")
print("Calculating Anthropometric data for",filename,"\n")
print("---------------------------------------------------")
print("Walking speed (m/s):",abs(totalDist/(1000*totalTime)))
print("Cadence (steps/s):",abs(cadence))
print("Stance percentage (%):",abs((sFinish-sStart)/(gFinish-gStart)*100))
print("Stride time (s):",strideTime)
print("Stride length (m):",abs(strideLength/1000))
print("---------------------------------------------------")
print("\nCalculating Kinematics data for",filename,"\n")
print("---------------------------------------------------")
print("Ankle")
print("-------")
print("Max. plantarflexion in loading response (pre swing in BW) (o):",maxPlantLoading)
print("Max. dorsiflexion in stance (o):",maxDorsiStance)
print("Max. plantarflexion in swing (o):",maxPlantSwing)
print("Total range of motion (o):",abs(totalROMAnk))
print("-------")
print("Knee")
print("-------")
print("Max. flexion in loading response (pre swing in BW) (o):",maxFlexKneeLoading)
print("Max. flexion in swing (o):",maxFlexKneeSwing)
print("Total range of motion (o):",abs(totalROMKnee))
print("-------")
print("Hip")
print("-------")
print("Flexion at heel strike (heel off in BW) (0):",flexHipHeelStrike)
print("Max. extension in stance (o):",maxExtHipStance)
print("Total range of motion (o):",totalROMHip)
print("---------------------------------------------------")
print("\nCalculating Kinetics data for",filename,"\n")
print("---------------------------------------------------")
print("Ankle")
print("-------")
print("Max. dorsiflexor moment (N.m/kg):",maxDorsiMoment/weight)
print("Max. plantarflexor moment (N.m/kg)",maxPlantMoment/weight)
print("Max. power generation (W/kg)",maxAnkPowerGen/weight)
print("Max. power absorption in loading response (W/kg)",maxAnkPowerAbs/weight)
print("-------")
print("Knee")
print("-------")
print("Max. extensor moment (N.m/kg):",maxKneeExtMoment/weight)
print("Max. flexor moment in stance (N.m/kg):",maxKneeFlexMoment/weight)
print("Max. power generation (W/kg):",maxKneePowerGen/weight)
print("Max. power absorption in loading response (W/kg):",maxKneePowerAbs/weight)
print("-------")
print("Hip")
print("-------")
print("Max. extensor moment in stance(N.m/kg):",maxHipExtMoment/weight)
print("Max. flexor moment in stance (N.m/kg):",maxHipFlexMoment/weight)
print("Max. power generation in Loading Response(W/kg):",maxHipPowerGen/weight)
print("Max. power absorption in Swing(W/kg):",maxHipPowerGen2/weight)