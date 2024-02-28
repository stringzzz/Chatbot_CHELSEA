#   chatbotCHELSEA, an AI chatbot with simulated emotions, math logic, and some self identity
#   Copyright (C) 2024 stringzzz, Ghostwarez Co.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Chatbot CHELSEA: CHat Emotion Logic SEnse Automator (0.04) (BETA)
# Project Start Date: 02-20-2024
# Version 0.04 (Not fully tested): 02-27-2024

import random
import re
import os
from datetime import datetime
from CHELSEA_MATH_LOGIC import CHELSEA_Math_Logic

dictionary = {}
dictionary_keys_list = ['happy', 'angry', 'sad', 'afraid', 'emotion', 'seen', 'associated']
messageDict = {"happy": {}, "angry": {}, "sad": {}, "afraid": {}}
nEmotions = ["happy", "angry", "sad", "afraid"]
currentMood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
pitches = {"happy": 90, "angry": 80, "sad": 80, "afraid": 95}
speeds = {"happy": 150, "angry": 155, "sad": 135, "afraid": 155}
userMessage = " "
user_self = {'uam': [], 'uamnot': []}
chatlog = []
Xchatlog = []
chatlogFile = {"regular": "CHELSEAchatlog.txt", "extended": "CHELSEAXchatlog.txt" }
user_emotions = { "happy": 0, "angry": 0, "sad": 0, "afraid": 0 }
self = { 'iam': [], 'iamnot': [] }
agree = ['Agreed, ', 'True ', 'Yes ', 'I know ', 'True that, ', 'Okay ', 'For sure, ', 'Oh yeah, ', 'Indeed, ', 'Yep, ', 'You know it, ', 'Correct, ']
disagree = ['No, ', 'Disagree, ', 'Wrong, ', 'Not true, ', 'False, ', 'Nope, ', 'Incorrect, ', 'I know otherwise, ', 'Oh no, ', 'Not valid, ', 'Negative, ']

def addToMood():
	#Add the emotional values of the user reply to CHELSEA's emotional values
	for emotion in nEmotions:
		currentMood[emotion] += replyMood[emotion]

	#Change mood, pitch, and speaking speed according to CHELSEA's emotional values
	temp_dict = { 'happy': currentMood['happy'], 'angry': currentMood['angry'], 'sad': currentMood['sad'], 'afraid': currentMood['afraid'] }
	currentMood["mood"] = getMood2(temp_dict, True)
	currentMood["pitch"] = pitches[currentMood["mood"]]
	currentMood["speed"] = speeds[currentMood["mood"]]
	Xchatlog.append("CHELSEA (Thinking): I feel " + currentMood["mood"])

def getReplyMood():
	#Get the mood of the user reply by looking at the emotion counts gathered on it
	temp_dict = { 'happy': replyMood['happy'], 'angry': replyMood['angry'], 'sad': replyMood['sad'], 'afraid': replyMood['afraid'] }
	replyMood["mood"] = getMood2(temp_dict, False)
	Xchatlog.append("CHELSEA (Thinking): " + username + " seems to be " + replyMood["mood"])

def getMood2(moodDictionary, botTF):
	#Get the overall mood of either CHELSEA or the user's response
	highest = max(moodDictionary.values())
	max1 = [k for k, v in moodDictionary.items() if v == highest]
	if (len(max1) == 1):	
		return max1[0]
	if (botTF):
		return 'happy'
	else:
		return 'temp neutral'

def botReply(botResponse):
	#Do the various parts of CHELSEA's response, text output, text-to-speech with espeak, chatlogs
	print("CHELSEA: " + botResponse)
	os.system("espeak -v en+f4 -p {} -s {} \" {} \"".format(str(currentMood["pitch"]), str(currentMood["speed"]), botResponse))
	chatlog.append("CHELSEA: " + botResponse)
	Xchatlog.append("CHELSEA: " + botResponse)
	return botResponse

def chatlogOutput(chatlogFile, chatList):
	chatlog_file = open(chatlogFile, 'a')
	chatlog_file.write("\n\n\n" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
	for line in chatList:
		chatlog_file.write("\n" + line)
	chatlog_file.close()

#Input memory
print("Inputting memory...")

#Input dictionary of known words
flip = 0
temp_line = ""
dictionary_file = open("dictionary.txt", 'r')
for line in dictionary_file.readlines():
	if (not(flip)):
		dictionary[line.strip()] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 0, 'associated': []}
		flip = 1
		temp_line = line.strip()
		continue
	else:
		temp_list = line.strip().split("&!&!&!")
		for n in range(0, 6):
			if (dictionary_keys_list[n] == 'happy' or dictionary_keys_list[n] == 'angry' or dictionary_keys_list[n] == 'sad' or dictionary_keys_list[n] == 'afraid' or dictionary_keys_list[n] == 'seen'):
				dictionary[temp_line][dictionary_keys_list[n]] = int(temp_list[n])
			else:
				dictionary[temp_line][dictionary_keys_list[n]] = temp_list[n]
		flip = 0
		dictionary[temp_line]['associated'] = temp_list[6].split("%$%$%$")

#Input dictionary of message/response pairs
gotPair = 0
tempValues = []
message_dictionary_file = open("messageDictionary.txt", 'r')
for emotion in nEmotions:
	messagesNo = int(message_dictionary_file.readline())
	for messages in range(0, messagesNo):
		if gotPair < 2:
			tempValues.append(message_dictionary_file.readline().strip())
			gotPair += 1
		if gotPair == 2:
			messageDict[emotion][tempValues[0]] = tempValues[1]
			tempValues.clear()
			gotPair = 0
message_dictionary_file.close()

#Get counts for use in activating certain types of message detection
dictionaryCount = len(dictionary.keys())
responseCount = 0
for emotion in nEmotions:
	responseCount += len(messageDict[emotion])
	
#Input CHELSEA self file
self_file = open("CHELSEAself.txt", 'r')
lines = self_file.readlines()
self_file.close()

if lines[0].strip() != 'none':
	self['iam'] = lines[0].strip().split("&%&%")
if lines[1].strip() != 'none':
	self['iamnot'] = lines[1].strip().split("&%&%")
			
print("Memory input complete!\n")

#Get username
botReply("What is your name? ")
username = input("")
username = re.sub(r"( )", "_", username)

#Input the user file for the current user, if it exists
try: 
	user_file = open(username + ".txt", 'r')
	for emotion in nEmotions:
		user_emotions[emotion] = int(user_file.readline())
	user_file.readline() #Skip to next line
	line = user_file.readline()
	if line != 'none':
		user_self['uam'] = line.strip().split("&%&%")
	line = user_file.readline()
	if line != 'none':
		user_self['uamnot'] = line.strip().split("&%&%")
	user_file.close()
except(FileNotFoundError):
	pass

#Initial message
CHELSEAPreviousResponse = "hello"
botReply("hello, " + username)

#Chat loop
while userMessage != "//exit":

	#User reply
	print(username + ": ", end = '')
	userMessage = (input("")).lower()
	chatlog.append(username + ": " + userMessage)
	Xchatlog.append("\n" + username + ": " + userMessage)
	if userMessage == "//exit":
		break
		
	#Math comprehension logic
	m1 = re.search(r"what does ([a-zA-Z0-9\(\)\*/\^\-\+ ,]*) (equal|=)\??", userMessage)
	if (m1):
		Xchatlog.append("CHELSEA (Thinking): Was asked a math question.")
		math_output = CHELSEA_Math_Logic(m1)
		print("CHELSEA: " + math_output)
		if (math_output == "Invalid expression!"):
			Xchatlog.append("CHELSEA (Thinking): Incorrect syntax or error for math question.")
			os.system("espeak -v en+f4 -p {} -s {} \" {} \"".format(str(currentMood["pitch"]), str(currentMood["speed"]), math_output))
		else:
			Xchatlog.append("CHELSEA (Thinking): I have the solution to the math question.")
		chatlog.append("CHELSEA: " + math_output)
		Xchatlog.append("CHELSEA: " + math_output)
		continue
	
	#Ask CHELSEA what she is or is not
	match1 = re.search(r"what are you( not)?\?*$", userMessage)
	if (match1):
		if (not(match1.group(1)) and len(self['iam']) != 0):
			Xchatlog.append("CHELSEA (Thinking): Was asked what I am, have an answer.")
			botReply("I am " + random.choice(self['iam']))
			continue
		elif (match1.group(1) and len(self['iamnot']) != 0):
			Xchatlog.append("CHELSEA (Thinking): Was asked what I am not, have an answer.")
			botReply("I am not " + random.choice(self['iamnot']))
			continue
			
	#Tell CHELSEA what she is or is not and see if there's agreement according to her self memory
	match1 = re.search(r"(?:you are|you're) (not )?(.*)", userMessage)
	if (match1):
		if (not(match1.group(1))):
			breakout = False
			for iam in self['iam']:
				if (iam == match1.group(2)):
					Xchatlog.append("CHELSEA (Thinking): Found agreement with 'I am'.")
					botReply(random.choice(agree) + 'I am ' + match1.group(2))
					breakout = True
					break
			if (breakout):
				continue
			for iamnot in self['iamnot']:
				if (iamnot == match1.group(2)):
					Xchatlog.append("CHELSEA (Thinking): Found disagreement with 'I am'.")
					botReply(random.choice(disagree) + 'I am not ' + match1.group(2))
					breakout = True
					break
			if (breakout):
				continue
			self['iam'].append(match1.group(2))		
			Xchatlog.append("CHELSEA (Thinking): Learned new 'I am'.")
			botReply(random.choice(agree) + 'I am ' + match1.group(2))
			continue
		else:
			breakout = False
			for iamnot in self['iamnot']:
				if (iamnot == match1.group(2)):
					Xchatlog.append("CHELSEA (Thinking): Found agreement with 'I am not'.")
					botReply(random.choice(agree) + 'I am not ' + match1.group(2))
					breakout = True
					break
			if (breakout):
				continue
			for iam in self['iam']:
				if (iam == match1.group(2)):
					Xchatlog.append("CHELSEA (Thinking): Found disagreement with 'I am not'.")
					botReply(random.choice(disagree) + 'I am ' + match1.group(2))
					breakout = True
					break
			if (breakout):
				continue
			self['iamnot'].append(match1.group(2))		
			Xchatlog.append("CHELSEA (Thinking): Learned new 'I am not'.")
			botReply(random.choice(agree) + 'I am not ' + match1.group(2))
			continue
		
	#Deal with current user's identity properties	
	match1 = re.search(r"(?:i am|i'm) (not )?(.*)", userMessage)
	if (match1):
		if (not(match1.group(1))):
			breakout = False
			for uam in user_self['uam']:
				if (uam == match1.group(2)):
					uam = re.sub(r"(your)", "my", uam)
					Xchatlog.append("CHELSEA (Thinking): Found agreement with 'User am'.")
					botReply(random.choice(agree) + 'you are ' + uam)
					breakout = True
					break
			if (breakout):
				continue
			for uamnot in user_self['uamnot']:
				if (uamnot == match1.group(2)):
					uamnot = re.sub(r"(your)", "my", uamnot)
					Xchatlog.append("CHELSEA (Thinking): Found disagreement with 'User am'.")
					botReply(random.choice(disagree) + 'you are not ' + uamnot)
					breakout = True
					break
			if (breakout):
				continue
			user_self['uam'].append(match1.group(2))
			uam = re.sub(r"(your)", "my", match1.group(2))		
			Xchatlog.append("CHELSEA (Thinking): Learned new 'User am'.")
			botReply(random.choice(agree) + 'you are ' + uam)
			continue
		else:
			breakout = False
			for uamnot in user_self['uamnot']:
				if (uamnot == match1.group(2)):
					uamnot = re.sub(r"(your)", "my", uamnot)
					Xchatlog.append("CHELSEA (Thinking): Found agreement with 'User am not'.")
					botReply(random.choice(agree) + 'you are not ' + uamnot)
					breakout = True
					break
			if (breakout):
				continue
			for uam in user_self['uam']:
				if (uam == match1.group(2)):
					uam = re.sub(r"(your)", "my", uam)
					Xchatlog.append("CHELSEA (Thinking): Found disagreement with 'User am not'.")
					botReply(random.choice(disagree) + 'you are ' + uam)
					breakout = True
					break
			if (breakout):
				continue
			user_self['uamnot'].append(match1.group(2))		
			uamnot = re.sub(r"(your)", "my", match1.group(2))
			Xchatlog.append("CHELSEA (Thinking): Learned new 'User am not'.")
			botReply(random.choice(agree) + 'you are not ' + uamnot)
			continue
				
	#Filter out punctuation from user message and split to list of words
	messageWords = (re.sub(r"(\.|\?|\!|,)", "", userMessage)).split(" ")

	#Detect emotion words, get reply mood, add user reply emotional values to CHELSEA's emotional values
	unknownWords = []
	replyMood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0}

	wordEmotions = ""
	for word in messageWords:
		if word == '':
			continue
		try:
			if (dictionary[word]['emotion'] != "permanent neutral" and dictionary[word]['emotion'] != "temp neutral"):
				replyMood[dictionary[word]['emotion']] += 1
				user_emotions[dictionary[word]['emotion']] += 1
				wordEmotions = wordEmotions + dictionary[word]['emotion'] + " "
			else: 
				wordEmotions = wordEmotions + " neutral "
		except(KeyError):
			unknownWords.append(word)
			wordEmotions = wordEmotions + " unknown "
	Xchatlog.append("Word emotions in previous reply: " + wordEmotions)
		
	getReplyMood()
	addToMood()

	#Mark unknown words in the emotion dictionary according to the overall mood of the user reply
	if len(unknownWords) > 0:
		Xchatlog.append("CHELSEA (Thinking): Unknown words detected: " + str(unknownWords))
		for word in unknownWords:
			dictionary[word] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 0, 'associated': ()}
			dictionary[word]['emotion'] = replyMood["mood"] 
		Xchatlog.append("CHELSEA (Thinking): Learned unknown words as '" + replyMood["mood"] + "' words.")
		
	#Add to counts for each word
	for word in messageWords:
		if (dictionary[word]['emotion'] == 'permanent neutral' or dictionary[word]['emotion'] == 'temp neutral'):
			continue
		dictionary[word][replyMood["mood"]] += 1
		temp_dict = { 'happy': dictionary[word]['happy'], 'angry': dictionary[word]['angry'], 'sad': dictionary[word]['sad'], 'afraid': dictionary[word]['afraid'] }
		word_emotion = getMood2(temp_dict, False)
		if (word_emotion != dictionary[word]['emotion']):
			dictionary[word]['emotion'] = word_emotion
			Xchatlog.append("CHELSEA (Thinking): Switched emotion of word '" + word + "' to " + word_emotion)
		
	#Mark associated words in list
	for word in messageWords:
		try:
			if (dictionary[word]['emotion'] == 'permanent neutral' or dictionary[word]['emotion'] == 'temp neutral'):
				continue
		except(KeyError):
			continue
		for word2 in messageWords:
			if (word == word2):
				continue
			try:
				if (dictionary[word2]['emotion'] == 'permanent neutral' or dictionary[word2]['emotion'] == 'temp neutral'):
					continue
			except(KeyError):
				continue
			
			temp_list = dictionary[word]['associated'][:]
			for word3 in temp_list:
				if (word3 == ''):
					continue
				if (word2 == word3 or word == word3):
					continue
				else:
					dictionary[word]['associated'].append(word2)
					Xchatlog.append("CHELSEA (Thinking): Learned association of " + word + " and " + word2)
					break
	
	#Check for exact match under current mood
	try:
		messageDict[currentMood["mood"]][userMessage]
		Xchatlog.append("CHELSEA (Thinking): Exact message match found.")
		CHELSEAPreviousResponse = botReply(messageDict[currentMood["mood"]][userMessage])
		continue
	except(KeyError):
		pass #Exact match not found in message dictionary
	
	#Check for partial match under current mood
	responseMade = False
	for message in messageDict[currentMood["mood"]].keys():
		if message.find(userMessage) != -1:
			Xchatlog.append("CHELSEA (Thinking): Partial message match found.")
			CHELSEAPreviousResponse = botReply(messageDict[currentMood["mood"]][message])
			responseMade = True
			break
	if responseMade:
		continue
		
	#Check for single term match under current mood, ignore neutral words
	#Only activated when she has learned enough, though this can easily be adjusted
	if ((dictionaryCount >= 2000 and responseCount >= 500 and random.randint(1, 4) == 1) or (dictionaryCount >= 4500 and responseCount >= 2700 and random.randint(1, 3) == 1)):
		responseMade = False
		#Coin flip
		if (random.randint(1, 2) == 1):
			#single term match from user message words
			for word in messageWords:
				try:
					if (dictionary[word]['emotion'] == "temp neutral" or dictionary[word]['emotion'] == "permanent neutral"):
						continue
					else:
						for message in messageDict[currentMood["mood"]].keys():
							if message.find(word) != -1:
								Xchatlog.append("CHELSEA (Thinking): Single term match found.")
								CHELSEAPreviousResponse = botReply(messageDict[currentMood["mood"]][message])
								responseMade = True
								break
						if responseMade:
							break
				except(KeyError):
					continue
			if responseMade:
				continue
		else:
			#Single term match for a word associated with user message word
			for word in messageWords:
				temp_words = []
				try:
					temp_words = dictionary[word]['associated']
				except(KeyError):
					continue
				if (len(temp_words) == 1 and temp_words[0] == ''):
					continue
					
				for word2 in temp_words:
					try:
						if (dictionary[word2]['emotion'] == "temp neutral" or dictionary[word2]['emotion'] == "permanent neutral"):
							continue
						else:
							for message in messageDict[currentMood["mood"]].keys():
								if message.find(word2) != -1:
									Xchatlog.append("CHELSEA (Thinking): Single term associated match found.")
									CHELSEAPreviousResponse = botReply(messageDict[currentMood["mood"]][message])
									responseMade = True
									break
							if responseMade:
								break
					except(KeyError):
						continue
				if responseMade:
					break
			if responseMade:
				continue
				 	
			
	#No match, either overwrite old response or learn new one based on reply mood
	Xchatlog.append("CHELSEA (Thinking): Message not recognized.")
	try:
		messageDict[replyMood["mood"]][CHELSEAPreviousResponse]
		Xchatlog.append("CHELSEA (Thinking): Overwrote old '" + replyMood["mood"] + "' response.")
	except(KeyError):
		Xchatlog.append("CHELSEA (Thinking): Learned new '" + replyMood["mood"] + "' response.")
	messageDict[replyMood["mood"]][CHELSEAPreviousResponse] = userMessage

	#Give random response from current mood	
	CHELSEAPreviousResponse = botReply(random.choice(list(messageDict[currentMood["mood"]].values())))

#Output memory
print("\nOutputting memory...")

#Output word dictionary file
dictionary_file = open("dictionary.txt", 'w')
for key in dictionary.keys():
	dictionary_file.write(key + "\n")
	for key2 in dictionary_keys_list:
		if (key2 == 'associated'):
			dictionary_file.write(str("%$%$%$".join(dictionary[key][key2])) + "&!&!&!")
		else:
			dictionary_file.write(str(dictionary[key][key2]) + "&!&!&!")
	dictionary_file.write("\n")
dictionary_file.close()

#Output message/reponse pair file
message_dictionary_file = open("messageDictionary.txt", 'w')
for emotion in nEmotions:
	message_dictionary_file.write(str(len(messageDict[emotion]) * 2) + "\n")
	for key in messageDict[emotion].keys():
		message_dictionary_file.write(key + "\n" + messageDict[emotion][key] + "\n")
message_dictionary_file.close()

#Output regular and extended chatlogs
chatlogOutput(chatlogFile["regular"], chatlog)
chatlogOutput(chatlogFile["extended"], Xchatlog)

#Output CHELSEA data file
data_file = open("CHELSEAdata.txt", 'w')
data_file.write(username + "\nWords in emotion dictionary: " + str(len(dictionary.keys())) + "\n")
for emotion in nEmotions:
	data_file.write("Number of " + emotion + " message/response pairs: " + str(len(messageDict[emotion])) + "\n")
data_file.close()

#Output user profile (With educated guess emotional state) and user self properties
user_file = open(username + ".txt", 'w')
for emotion in nEmotions:
	user_file.write(str(user_emotions[emotion]) + "\n")
user_overall_mood = getMood2(user_emotions, False)
user_file.write(username + " seems to be a(n) " + user_overall_mood + " person.\n")
if (len(user_self['uam']) == 0):
	user_self['uam'].append("none")
if (len(user_self['uamnot']) == 0):
	user_self['uamnot'].append("none")
user_file.write("&%&%".join(user_self['uam']) + "\n" + "&%&%".join(user_self['uamnot']))
user_file.close()

#Output CHELSEA self file
self_file = open("CHELSEAself.txt", 'w')
if (len(self['iam']) == 0):
	self['iam'].append("none")
if (len(self['iamnot']) == 0):
	self['iamnot'].append("none")
self_file.write("&%&%".join(self['iam']) + "\n" + "&%&%".join(self['iamnot']))
self_file.close()

print("Memory output complete.\n")
