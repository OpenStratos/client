import re
import sys

#Checks if a string matches a regex. Returns 1 if it does match and 0 if it does not.
#
def checkRegex(regex,message):
	regex = re.compile(regex)
	if regex.match(message):
		#print("Matched")
		return 1
	else:
		#print("Not matched")
		return 0


#Checks if a string is a valid data frame by matching it to a regular expression. 
#Returns 1 if it does match and 0 if it does not.
#
def checkForValidMessage(messageToCheck):
	return checkRegex("[\$](SYN|ACK|ACKR|PWR|OFF|ERR|REPORT|CREPORT|GPGGA|GPGSA|GPRMC)"+
			  "([,][^\r\n\t\s]+)+[\*][0-9A-Fa-f][0-9A-Fa-f]",messageToCheck)

#Parses a SYN frame
#
def parseSYN(synToParse):
	if checkRegex("[\*][0-9a-fA-F][0-9a*49-fA-F]",synToParse)==1:
		#TODO: SYN accepted. Now do something	
		return

#Parses an ACK frame
#
def parseACK(ackToParse):
	if checkRegex("[\*][0-9a-fA-F][0-9a*49-fA-F]",ackToParse)==1:
		ackToParse = ackToParse.split(",")
		#TODO: ACK accepted. Now do something
	return

#Parses an ACKR frame
#
def parseACKR(ackrToParse):
	if checkRegex("[\*][0-9a-fA-F][0-9a*49-fA-F]",ackrToParse)==1:
		ackrToParse = ackrToParse.split(",")
		#TODO: ACKR accepted. Now do something with it
		
	return

#Parses an PWR frame
#See comments for details
def parsePWR(pwrToParse):
	if checkRegex("[0|1]",pwrToParse)==1:
		powerStatus = int(pwrToParse)				#The variable powerStatus now holds the value of PowerStatus as detailed in the protocol

	return

#Parses an OFF frame
#See comments for details
def parseOFF(offToParse):
	print("Received:")
	print(offToParse)
	if checkRegex("[0-9A-Fa-f]+",offToParse)==1:
		password = offToParse					#The variable password now holds the value of the Password field (256 bit hex) as detailed in the protocol
	return
	

#Parses an ERR frame
#See comments for details
def parseERR(errToParse):
	#[1|2|3]
	if checkRegex("[1|2|3]+",errToParse)==0:
		error = int(errToParse)					#The variable error now holds the value of the error code (1,2 or 3) as detailed in the protocol
	return
		
#Parses a REPORT frame
#See comments for details
def parseREPORT(reportToParse):
	#[0|1][,]([\d][\d]([\d]*))[,]([0-9]{9})[,]([0-9]{10})[,][0|1][,](([+|-|]?[\d]+[.][\d]+))[,]([+|-]?[\d]+[.][\d]+)[,][\d]{2}[,][\d]{2}[,][\d]{2}
	if checkRegex("[$]REPORT[,]"+
		      "[0|1][,]([\d][\d]([\d]*))[,]([0-9]{9})[,]([0-9]{10})[,][0|1][,]"+
		      "(([+|-|]?[\d]+[.][\d]+))[,]([+|-]?[\d]+[.][\d]+)[,][\d]{2}[,][\d"+
		      "]{2}[,][\d]{2}",reportToParse)==1:

		reportToParse = reportToParse.split(",")
		safemode = int(reportToParse[1])
		cpuLoad = int(reportToParse[2])
		freeRAM = int(reportToParse[3])
		RASPTime = int(reportToParse[4])
		gpsActive = int(reportToParse[5])
		gpsLat = float(reportToParse[6])
		gpsLon = float(reportToParse[7])
		batRasp = float(reportToParse[8])
		bat1 = float(reportToParse[9])
		bat2 = float(reportToParse[10])
		#TODO: Do something with that
	return

#Parses a CREPORT frame
#See comments for details
def parseCREPORT(creportToParse):
	#Warning: Due to discrepancies between specs and examples for the CREPORT frames, the specification has been assumed to be correct.
	if checkRegex("[$]CREPORT[,]"+
		      "[0|1][,](([\d][\d]([\d]*)[.][\d][\d]))[,]([\d][.][\d]{2}[,])"+
		      "([\d][.][\d]{2}[,])([\d][.][\d]{2}[,])([0-9]{9})[,]([0-9]{10}"+
		      ")[,]([0-9]{10})[,][0|1][,][\d][\d][,](([+|-|]?[\d]+[.][\d]+))"+
		      "[,]([+|-]?[\d]+[.][\d]+)[,]([\d]{5}[.][\d])[,]([\d][.][\d]{2}"+
		      ")[,]([\d][.][\d]{2})[,]([\d]+([.][\d]([\d]+)?)?)[,]([\d]([\d]"+
		      "+)?)[,][0|1][,][0|1][,][0|1][,]([+|-]?[\d][\d][.][\d][\d])[,]"+
		      "([+|-]?[\d][\d][.][\d][\d])[,]([\d]{2}[.][\d]{2})[,]([\d]{2}["+
		      ".][\d]{2})[,]([\d]{2}[.][\d]{2})",creportToParse)==1:
		creportToParse = creportToParse.split(",")
		safemode = int(creportToParse[1])		#The variable safemode now holds the value of the corresponding field as detailed in the protocol
		cpuLoad = float(creportToParse[2])		#The variable cpuload now holds the value of the corresponding field as detailed in the protocol		
		cpuLoad1m = float(creportToParse[3])		#The variable cpuload1m now holds the value of the corresponding field as detailed in the protocol
		cpuLoad5m = float(creportToParse[4])		#The variable cpuload5m now holds the value of the corresponding field as detailed in the protocol
		cpuLoad15m = float(creportToParse[5])		#The variable cpuload15m now holds the value of the corresponding field as detailed in the protocol
		freeRAM = int(creportToParse[6])		#The variable freeRAM now holds the value of the corresponding field as detailed in the protocol
		RASPTime = int(creportToParse[7])		#The variable RASPtime now holds the value of the corresponding field as detailed in the protocol
		GPSTime = int(creportToParse[8])		#The variable GPSTime now holds the value of the corresponding field as detailed in the protocol
		GPSActive = int(creportToParse[9])		#The variable GPSActive now holds the value of the corresponding field as detailed in the protocol
		GPSSat = int(creportToParse[10])		#The variable GPSsat now holds the value of the corresponding field as detailed in the protocol
		gpsLat = float(creportToParse[11])		#The variable gpsLat now holds the value of the corresponding field as detailed in the protocol
		gpsLon = float(creportToParse[12])		#The variable gpsLon now holds the value of the corresponding field as detailed in the protocol
		alt = float(creportToParse[13])			#The variable alt now holds the value of the corresponding field as detailed in the protocol
		hdop = float(creportToParse[14])		#The variable hdop now holds the value of the corresponding field as detailed in the protocol
		vdop = float(creportToParse[15])		#The variable vdop now holds the value of the corresponding field as detailed in the protocol
		speed = float(creportToParse[16])		#The variable speed now holds the value of the corresponding field as detailed in the protocol
		course = int(creportToParse[17])		#The variable course now holds the value of the corresponding field as detailed in the protocol
		cam = int(creportToParse[18])			#The variable cam now holds the value of the corresponding field as detailed in the protocol
		logs = int(creportToParse[19])			#The variable logs now holds the value of the corresponding field as detailed in the protocol
		gsm = int(creportToParse[20])			#The variable gsm now holds the value of the corresponding field as detailed in the protocol
		temp1 = float(creportToParse[21])		#The variable temp1 now holds the value of the corresponding field as detailed in the protocol
		temp2 = float(creportToParse[22])		#The variable temp2 now holds the value of the corresponding field as detailed in the protocol
		batRasp = float(creportToParse[23])		#The variable batRasp now holds the value of the corresponding field as detailed in the protocol
		bat1 = float(creportToParse[24])		#The variable bat1 now holds the value of the corresponding field as detailed in the protocol
		bat2 = float(creportToParse[25])		#The variable bat2 now holds the value of the corresponding field as detailed in the protocol
		#TODO: Do something with that
		
	return

#Checks that the checksum of a frame is correct.
#TODO: Implement
def performCheckSum(stringToCheck):
	return

#Validates that a frame is an actual accepted frame and parses it.
#
def parse(lineToParse):
	if checkForValidMessage(lineToParse)==0:
		return
	else:
		messageCheckSum = lineToParse.split("*")
		performCheckSum(messageCheckSum[1])
		lineSplit = messageCheckSum[0].split(",")
		msgType = lineSplit[0]
		value = lineSplit[1].join(lineSplit[2:])


		options = {"$SYN":parseSYN,
			"$ACK":parseACK,
			"$ACKR":parseACKR,
			"$PWR":parsePWR,
			"$OFF":parseOFF,
			"$ERR":parseERR,
			"$REPORT":parseREPORT,
			"$CREPORT":parseCREPORT}

		options[msgType](messageCheckSum[0])
	return

#TODO: Call parse from here

