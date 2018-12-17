## @package FeatureExtraction
# This module is used to extract the features from the mouse logger data.
#
# Once features are extrcted they are used to classify the authentic user based on some predictive models.
# Numbering convention used for the various features extracted from the data. Feature details mentioned
# in the report.
# *	1: Click Time
# *	2: Horizontal Velocity
# *	3: Vertical Velocity
# *	4: Pause Time
# *	5: Straightness
##

import math
import os, os.path

##
# @var outFileName The name of the output file where the features are written after extraction
##
# File name where the output features are written
outFileName = open('features/ProcessedFeatures.csv', 'w')
outFileName.write('User, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10\n')
## 
# @var testClass The test user for which classification is ot be done
##
testClass = 'arvind' 	#the class which is to be predicted

#STANDARD FUNCTIONS*********************************************************************************************

## @fn getNthVal Documentation for a function.
# Returns the nth term after splitting a line from the logger based on comma. This is used to find the timestamp
# or the coordinate values for the line.
def getNthVal(line, n):
	return int(line.split(", ")[n])

#finds the distance between the two given points
def dist(x0, y0, x1, y1):
	return math.sqrt((x1 - x0)**2 + (y1 - y0)**2)

## This class is used to create a user object corresponding to each user whose data is being analyzed. Then this
# object is used to extract the features from the user's data.
class UserSession(object):
	
	#GLOBAL CONSTANTS*********************************************************************************************
	## After this time it is assumed that the next logged line was not part of a continuous process (stroke)
	MIN_RESONSE_TIME = 400
	## After this time it is assumed that a session was over for a user. That is, after this time a new session is
	# started for the user
	MAX_SESSION_BREAK_TIME = 1800000
	## This indicates the minimum number of actions that needs to be logged for a session to be used for data extraction
	# This is done because otherwise the session might not reflect the proper behavioral characteristics of the user
	MIN_ACTION_PER_SESSION = 1000

	## The constructor for the class
	# @param self The object pointer
	# @param folderName The name of the folder whose data needs to be analyzed
	def __init__(self, folderName):
		#FEATURE RELATED VARIABLES************************************************************************************
		## The name of the folder to be analyzed
		self.folderName = folderName
		## Temporary flag variable to check if mouse click has actually occured
		self.flag = 0
		## The average value of the mouse click feature
		self.offtimeAvg = 0
		## The standard deviation value of the mouse click feature
		self.offtimeStd = 0
		## The count of the number of mouse clicks
		self.offtimeCnt = 0
		## Total time from mouse move to mouse click
		self.time = 0
		## The starting X coordinate of the mouse stroke
		self.startX = 0
		## The starting Y coordinate of the mouse stroke
		self.startY = 0	#starting Y coordinate
		## The ending X coordinate of the mouse stroke
		self.endX = 0	#ending X coordinate
		## The ending Y coordinate of the mouse stroke
		self.endY = 0	#ending Y coordinate
		## Total number of mouse moves logged for one such gesture/stroke
		self.cnt = 0		#total number of mouse moves logged for one such gesture
		## The original distance covered by the user (for straightness calculation)
		self.originalDist = 0	#the original distance covered by the user (for straightness calculation)
		## Stores the last logged X coordinate for MM
		self.tempX = 0	#stores the last logged X coordinate for MM
		## Stores the last logged Y coordinate for MM
		self.tempY = 0	#stores the last logged Y coordinate for MM

		## The average value of horzontal velocity
		self.horVeloAvg = 0
		## The average value of vertical velocity
		self.verVeloAvg = 0
		## The average value of pause time
		self.delayAvg = 0
		## The average value of straightness
		self.straightnessAvg = 0
		## The total count of all the actions (used to find average)
		self.allCnt = 0
		## The standard deviation value of horzontal velocity
		self.horVeloStd = 0
		## The standard deviation value of vertical velocity
		self.verVeloStd = 0
		## The standard deviation value of pause time
		self.delayStd = 0
		## The standard deviation value of straightness
		self.straightnessStd = 0

		## keeps count of the number of actions per session
		self.sessonActionCount = 0	#keeps count of the number of actions per session

	## Returns true if the time for a particular line based on the line format is exceeding the
	# max log-out time (session break)
	# @param self The object pointer
	# @param line The line of the log to be analyzed
	def isSessonTimeOver(self, line):
		if (line[:2] == "MP" or line[:2] == "MR"):
			if getNthVal(line, 2) > UserSession.MAX_SESSION_BREAK_TIME:
				return True
		elif (line[:2] == "MM" or line[:2] == "MD"):
			if getNthVal(line, 3) > UserSession.MAX_SESSION_BREAK_TIME:
				return True
		elif(line[:3] == "MWM"):
			if getNthVal(line, 6) > UserSession.MAX_SESSION_BREAK_TIME:
				return True

		return False

	## Resets the feature realted variables
	# @param self The object pointer
	def resetVariables(self):
		self.flag = 0
		self.offtimeAvg = self.offtimeStd = 0
		self.offtimeCnt = 0
		self.time = 0	#total time from mouse move to mouse click
		self.startX = 0	#starting X coordinate
		self.startY = 0	#starting Y coordinate
		self.endX = 0	#ending X coordinate
		self.endY = 0	#ending Y coordinate
		self.cnt = 0		#total number of mouse moves logged for one such gesture
		self.originalDist = 0	#the original distance covered by the user (for straightness calculation)
		self.tempX = 0	#stores the last logged X coordinate for MM
		self.tempY = 0	#stores the last logged Y coordinate for MM

		self.horVeloAvg = self.verVeloAvg = self.delayAvg = self.straightnessAvg = self.allCnt = 0
		self.horVeloStd = self.verVeloStd = self.delayStd = self.straightnessStd = 0

		self.sessonActionCount = 0

	## Writes the feature variables to file as mentioned in folderName
	# @param self The object pointer
	def writeToFile(self):
		#write to the output file -> username is either vikrant or others
		if(self.folderName == testClass):
			className = 2
		else:
			className = 1
		outFileName.write("%d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (className, self.offtimeAvg, self.offtimeStd,
						self.horVeloAvg, self.horVeloStd, self.verVeloAvg, self.verVeloStd, self.delayAvg, self.delayStd,
							self.straightnessAvg, self.straightnessStd))

	## Calculate the mean and standard deviation of features
	# @param self The object pointer
	def calculateValues(self):
		#calculation of mean and standard deviation
		self.offtimeAvg = float(self.offtimeAvg) / (self.offtimeCnt * self.sessonActionCount)	#normalize with session length
		self.offtimeStd = float(self.offtimeStd) / self.offtimeCnt
		self.offtimeStd -= self.offtimeAvg * self.offtimeAvg
		self.offtimeStd = math.sqrt(self.offtimeStd)

		self.horVeloAvg = float(self.horVeloAvg) / self.allCnt
		self.horVeloStd = float(self.horVeloStd) / self.allCnt
		self.horVeloStd -= self.horVeloAvg * self.horVeloAvg
		self.horVeloStd = math.sqrt(self.horVeloStd)

		self.verVeloAvg = float(self.verVeloAvg) / self.allCnt
		self.verVeloStd = float(self.verVeloStd) / self.allCnt
		self.verVeloStd -= self.verVeloAvg * self.verVeloAvg
		self.verVeloStd = math.sqrt(self.verVeloStd)

		self.delayAvg = float(self.delayAvg) / self.allCnt
		self.delayStd = float(self.delayStd) / self.allCnt
		self.delayStd -= self.delayAvg * self.delayAvg
		self.delayStd = math.sqrt(self.delayStd)

		self.straightnessAvg = float(self.straightnessAvg) / self.allCnt
		self.straightnessStd = float(self.straightnessStd) / self.allCnt
		self.straightnessStd -= self.straightnessAvg * self.straightnessAvg
		self.straightnessStd = math.sqrt(self.straightnessStd)



## Reads all the log files and calculate the appropriate features based on the session
# @param newSession The new user for whom the feature extraction needs to be done
def calculateFeatures(newSession):
	fileCount = len([name for name in os.listdir('data/' + newSession.folderName) if (name.endswith('.txt') and name.startswith('log'))])

	print 'Number of files: ' + str(fileCount)

	#***********************************************************************************************************
	for fileNum in range(1, fileCount + 1):
		fileName = open('data/' + newSession.folderName + '/log' + str(fileNum) + '.txt', 'r');
		# print "Filename: " + 'data/' + folderName + '/log' + str(fileNum) + '.txt'
		print 'Processing ' + newSession.folderName + ' log file ' + str(fileNum) + ' of ' + str(fileCount)
		
		resetFlag = 0

		for line in fileName:
			if newSession.isSessonTimeOver(line):
				#if min actions are not performed then not valid session
				if newSession.sessonActionCount > UserSession.MIN_ACTION_PER_SESSION:
					# session over so write to file and reset the parameters
					newSession.calculateValues()
					newSession.writeToFile()
					newSession.resetVariables()
			
			else:	#session is same so continue with the calculation
				newSession.sessonActionCount += 1
				# mouse click time calculation
				if(line[:2] == "MP"):	#mouse is pressed
					newSession.flag = 1
					ontime = getNthVal(line, 2)
				if(line[:2] == "MD") and newSession.flag == 1:	#mouse press is not for click
					newSession.flag = 0
				if(line[:2] == "MR" and newSession.flag == 1):		#if flag is 1 then mouse press is for mouse click
					newSession.flag = 0
					offtime = getNthVal(line, 2)
					
					newSession.offtimeAvg += offtime
					newSession.offtimeStd += offtime * offtime
					newSession.offtimeCnt += 1

				# velocity, pause time, straightness calculation
				if line[:2] == "MM":	#mouse moved
					newSession.cnt += 1
					delay = getNthVal(line, 3)		#the delay from last value
					if delay > UserSession.MIN_RESONSE_TIME:
						time = newSession.startX = newSession.startY = newSession.endX = 0
						newSession.endY = newSession.cnt = newSession.originalDist = 0
					elif newSession.cnt == 1:
						newSession.startX = getNthVal(line, 1)
						newSession.startY = getNthVal(line, 2)
						newSession.tempX = newSession.startX
						newSession.tempY = newSession.startY
					else:
						newSession.time += delay
						newSession.endX = getNthVal(line, 1)
						newSession.endY = getNthVal(line, 2)
						newSession.originalDist += dist(newSession.tempX, newSession.tempY, newSession.endX, newSession.endY)
						newSession.tempX = newSession.endX
						newSession.tempY = newSession.endY
				elif line[:2] == "MP" and newSession.cnt > 15:	#mouse pressed/clicked  assuming atlest 15 MM's as mouse move
					delay = getNthVal(line, 2)
					if delay > UserSession.MIN_RESONSE_TIME:
						newSession.time = newSession.startX = newSession.startY = newSession.endX = 0
						newSession.endY = newSession.cnt = 0
					else:
						newSession.time += delay
						horVelo = abs((float)(newSession.endX - newSession.startX) / newSession.time)
						verVelo = abs((float)(newSession.endY - newSession.startY) / newSession.time)
						tempDist = dist(newSession.startX, newSession.startY, newSession.endX, newSession.endY)
						if tempDist == 0:
							straightness = 0
						else:
							straightness = newSession.originalDist / tempDist
						
						newSession.horVeloAvg += horVelo
						newSession.verVeloAvg += verVelo
						newSession.delayAvg += delay
						newSession.straightnessAvg += straightness
						newSession.horVeloStd += horVelo * horVelo
						newSession.verVeloStd += verVelo * verVelo
						newSession.delayStd += delay * delay
						newSession.straightnessStd += straightness * straightness
						newSession.allCnt += 1
				else:
					newSession.cnt = 0

		#calculate and write to file for final session
		newSession.calculateValues()
		newSession.writeToFile()
		newSession.resetVariables()


## Main function
def main():
	
	allUsers = ['arvind', 'vikrant', 'anil', 'bishal', 'vishnu', 'pawan', 'pandu']

	#create a new user session object for each user and calculate features
	for name in allUsers:
		newSession = UserSession(name)
		calculateFeatures(newSession)

if __name__ == "__main__":
	main()

