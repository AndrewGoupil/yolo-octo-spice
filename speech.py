import os
import datetime
import urllib.request
import imaplib
import pywapi
import wolframalpha
import time

#email credentials to check for unread messages
usr = "@gmail.com"
pas = ""

#weather station codes
mississauga = "CAXX0295"
toronto = "CAXX0504"

#WolframAlpha App ID (Max 200 Queries)
appid = ""


#reads aloud a string using AT&T natual language online tool
def toSpeech(text):
	os.system('bash getWav.sh '+'"'+text+'"'+' ')


#returns the hour (24hour format), minutes, and seconds 
def getTime():
	time = datetime.datetime.now().strftime("%H %M %S").split()
	currentTime = []
	for x in time:
		currentTime.append(str(int(x)))
	return currentTime


#returns the weekday, month, and time as an array
def getDate():
	date = datetime.datetime.now().strftime("%A %B %d").split()
	date[2] = str(int(date[2]))
	return date


#returns the html of a given site as a string
def getHTML(url):
	f = urllib.request.urlopen(url)
	htmlByte = f.read()
	html = "".join(map(chr, htmlByte))
	return html


#returns the number of unread emails 
def getUnreadCount(username, password):
	gmail = imaplib.IMAP4_SSL('imap.gmail.com', '993')
	gmail.login(username, password)
	gmail.select()
	count = gmail.search(None, 'Unseen')[1][0].decode("utf-8").split()
	return len(count)


#gets the current conditions from Yahoo.com
def getConditions(city):
	result = pywapi.get_weather_from_yahoo(city, 'metric')
	condition = result['condition']['text']
	temperature = result['condition']['temp']
	humidity = result['atmosphere']['humidity']
	return [condition, temperature, humidity]


#gets a five day forecast from Yahoo.com
#day 0 is the current date
def getForecast(city, day=0):
	result = pywapi.get_weather_from_yahoo(city, 'metric')
	forecast = result['forecasts'][day]
	
	day = forecast['day']
	high = forecast['high']
	low = forecast['low']
	text = forecast['text']

	return [day, high, low, text]


#queries wolframalpha
def getWolframAlpha(txt):
	client = wolframalpha.Client(appid)
	res = client.query(txt)
	
	if(len(res.pods) >0):
		texts = ""
		pod = res.pods[1]

		if(pod.text):
			texts = pod.text
		else:
			texts = "I have no answer for that."
		#to skip ascii character in case of an error
		texts = texts.encode("ascii", "ignore")
		returnString= texts.decode("utf-8")
		return returnString
	else:
		return "Sorry, I am not sure."
	

def playSong():
	import random
	song = random.randint(1,9)
	os.system("mplayer music/"+str(song)+".mp3")


def alarm():
	condition = getConditions(mississauga)
	forecast = getForecast(mississauga)
	unread = getUnreadCount(usr, pas)

	string = ("Good morning Albert. "
		"It is "+condition[0]+" outside. "+condition[1]+" degrees with"
		+condition[2]+" percent humidity. "
		"Today will reach an expected high of "+forecast[1]+" and a low of "+forecast[2]+". It is expected to be "+forecast[3]+" later today. "
		"You have "+str(unread)+" unread messages.")
	os.system("mplayer alarm.wav")
	toSpeech(string)




#-----------------------------------Main-----------------------------------
while(True):

	INPUT = input()

	if(len(INPUT) ==0):
		toSpeech("You cannot enter an empty query!")

	#set alarm format = "alarm hh:mm (24 hours)"
	elif('alarm' in INPUT):
		toSpeech("Your alarm has been set.")
		arg = INPUT.split()[1].split(":")
		
		while(True):
			currentTime = getTime()
			print(currentTime)
			if(arg[0] == currentTime[0]) and (arg[1] == currentTime[1]):
				os.system("mplayer alarm.wav")
				alarm()
				break
			time.sleep(10)

	elif(INPUT == 'w'):
		condition = getConditions(mississauga)
		toSpeech("It is "+condition[0]+" outside. "+condition[1]+" degrees with"+condition[2]+" percent humidity.")
		
	elif(INPUT == 'f'):
		forecast = getForecast(mississauga)
		toSpeech("Today will reach an expected high of "+forecast[1]+" and a low of "+forecast[2]+". It is expected to be "+forecast[3]+" later today. ")

	elif(INPUT == 'm'):
		unread = getUnreadCount(usr, pas)
		toSpeech("You have "+str(unread)+" unread messages.")

	elif(INPUT == "s"):
		playSong()

	elif(INPUT == "t"):
		currentTime = getTime()
		toSpeech("The current time is: "+currentTime[0]+" hours and "+currentTime[1]+" minutes.")

	elif(INPUT == "d"):
		currentDate = getDate()
		toSpeech("It is "+currentDate[0]+" "+currentDate[1]+" "+currentDate[2])
	else:
		toSpeech(getWolframAlpha(INPUT))
