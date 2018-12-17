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

from UserSession import UserSession

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


## Main function
def main():
	
	allUsers = ['arvind', 'vikrant', 'anil', 'bishal', 'vishnu', 'pawan', 'pandu']

	#create a new user session object for each user and calculate features
	for name in allUsers:
		newSession = UserSession(name)
		calculateFeatures(newSession)

if __name__ == "__main__":
	main()

