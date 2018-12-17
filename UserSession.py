import math
import os, os.path

from EMD import EMD
from sequence import Point,dist,sequence

## @fn getNthVal Documentation for a function.
# Returns the nth term after splitting a line from the logger based on comma. This is used to find the timestamp
# or the coordinate values for the line.
def getNthVal(line, n):
	return int(line.split(", ")[n])

## This class is used to create a user object corresponding to each user whose data is being analyzed. Then this
# object is used to extract the features from the user's data.
class UserSession(object):
	
	#GLOBAL CONSTANTS*********************************************************************************************
	## After this time it is assumed that the next logged line was not part of a continuous process (stroke)
	MIN_RESPONSE_TIME = 400
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
		self.time = 0
		## The starting coordinates of the mouse stroke
		self.startP = Point()
		## The ending coordinates of the mouse stroke
		self.endP = Point()
		## Total number of mouse moves logged for one such gesture/stroke
		self.cnt = 0		#total number of mouse moves logged for one such gesture
		## The original distance covered by the user (for straightness calculation)
		self.originalDist = 0	#the original distance covered by the user (for straightness calculation)
		## Stores the last logged coordinate for MM
		self.tempP = Point()
		## keeps count of the number of actions per session
		self.sessonActionCount = 0	#keeps count of the number of actions per session
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
		self.time = 0	#total time from mouse move to mouse click
		self.startP = Point()	#starting coordinate
		self.endP = Point()	#ending coordinate
		self.cnt = 0		#total number of mouse moves logged for one such gesture	
		self.tempP = Point()	#stores the last logged coordinate for MM

		self.allCnt = 0

		self.sessonActionCount = 0

	## Writes the feature variables to file as mentioned in folderName
	# @param self The object pointer
	def writeToFile(self):
		#write to the output file -> username is either vikrant or others


	## Calculate the mean and standard deviation of features
	# @param self The object pointer

## Reads all the log files and calculate the appropriate features based on the session
# @param newSession The new user for whom the feature extraction needs to be done
def calculateFeatures(newSession):
	fileCount = len([name for name in os.listdir('data/' + newSession.folderName) if name.endswith('.txt') and name.startswith('log')])
	print ('Number of files: ' + str(fileCount))
	print (os.listdir('data/' + newSession.folderName))

	#***********************************************************************************************************
	for fileNum in range(1, fileCount + 1):
		fileName = open('data/' + newSession.folderName + '/log' + str(fileNum) + '.txt', 'r');
		# print "Filename: " + 'data/' + folderName + '/log' + str(fileNum) + '.txt'
		print ('Processing ' + newSession.folderName + ' log file ' + str(fileNum) + ' of ' + str(fileCount))
		
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

				if(line[:3] == "MM" and newSession.flag == 0):		#if flag is 1 then mouse press is for mouse click
					newSession.flag = 1
					offtime = getNthVal(line, 2)
					
					newSession.offtimeAvg += offtime
					newSession.offtimeStd += offtime * offtime
					newSession.offtimeCnt += 1

				# velocity, pause time, straightness calculation
				if line[:2] == "MM":	#mouse moved
					newSession.cnt += 1
					delay = getNthVal(line, 3)		#the delay from last value
					if delay > UserSession.MIN_RESPONSE_TIME:
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
					if delay > UserSession.MIN_RESPONSE_TIME:
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
