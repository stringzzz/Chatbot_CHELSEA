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

# Chatbot CHELSEA: CHat Emotion Logic SEnse Automator (0.09) (BETA)
# Project Start Date: 02-20-2024
# Version 0.04 (Not fully tested): 02-27-2024
# Version 0.05 (All tested except Math Logic) 02-28-2024
# Version 0.06 (Added current topic logic) 03-02-2024
# Version 0.07 (Added WH-Question logic) 03-02-2024
# Version 0.08 (Added 'What do you mean' logic) 03-03-2024
# Version 0.09 (Added more question logic, some other small changes) 03-05-2024
# Version 0.10 (Added counts for all associated words) 03-10-2024

##############################################
## Chatbot CHELSEA message handling algorithm 
##############################################
# 1. User enters message
#
# 2. Detect if math question, use external script to handle
# and give solution to question (Highly experimental)
#
# 3. Detect if asking what she is or is not
#
# 4. Detect if asking what user is or is not
#
# 5. Detect if telling what she is or is not, learn accordingly
# Also detect if contradiction to what she already knows
#
# 6. Detect if current user describing what they are or are not
# Learn accordingly, detect if contradiction to what she already knows
#
# 7. Split message into words, remove punctuation
# Determine mood of reply, add counts to CHELSEA mood as well
#
# 8. Mark unkown words in message
#
# 9. Add to counts for each word, adjust the tied emotion to them accordingly
#
# 10. Take each word and associate all other (non-neutral) words in message 
# with them (Either start or add to count)
# Comes into play in matching single associated word with highest count, or select
# one randomly from list of highest
#
# 11. Add to running counts of all words in conversation
# Get topic(s) of conversation by the maximum value
#
# 12. Check if user is asking What Question, give possible answer response if so
#
# 13. Check if user asking for clarification on previous response,
# try to find matching message containing 2 or more words from
# previous response
#
# 14. Check if asking what CHELSEA feels about ___,
# respond according to the tied emotions with the words in ___
#
# 15. Check if asking 'do you like/dislike ___' question
# respond according to tied emotions to words in ___,
# agreement or disagreement depends on emotion and like/dislike
# word used
#
# 16. Check if asking 'which is better, _1_ or _2_'
# Used emotions tied to the words to decide which CHELSEA likes better,
# or indifferent if neither is tied to happy overall
# 12. Check for an exact match of message, give linked response if so
#
# 17. Check if asking 'why is' question, try to find match involving
# 'because' words a possible answer
# 
# 18. Check for 'most __emotion__' question, respond with biggest word(s) tied to emotion
#
# 19. Check for an exact match of message, give linked response if so
#
# 20. Check if message matches as part of a message in memory,
# give linked reponse if so
#
# 21. If certain # or greater messages and words in dictionary, PRNG to
# determine if attempting topic match. 
#
# 22. If certain # or greater messages and words in dictionary, PRNG to
# determine if doing single term match. If so, coin flip to determine whether
# trying to match single word from message as part of message in memory,
# or single word associated with word from message. Repond with linked 
# response if so
#
# 23. No match, overwrite old message in memory or learn brand new message/response pair
#
# 24. Respond with random response from memory to keep conversation going
#########################################   

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
pitches = {"happy": 95, "angry": 80, "sad": 90, "afraid": 99}
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
topics = {}

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
	replyMood["mood"] = getMood2(temp_dict, True)
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
	os.system("espeak -v en+f3 -p {} -s {} \" {} \"".format(str(currentMood["pitch"]), str(currentMood["speed"]), botResponse))
	chatlog.append("CHELSEA: " + botResponse)
	Xchatlog.append("CHELSEA: " + botResponse)
	return botResponse

def chatlogOutput(chatlogFile, chatList):
	chatlog_file = open("" + chatlogFile, 'a')
	chatlog_file.write("\n\n\n" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
	for line in chatList:
		chatlog_file.write("\n" + line)
	chatlog_file.close()

def getMost(dictio, emotion):
	temp_dict = {}
	for key in dictio.keys():
		if (dictio[key]['emotion'] == emotion):
			temp_dict[key] = dictio[key][emotion]
	highest = max(temp_dict.values())
	max1 = [k for k, v in temp_dict.items() if v == highest]
	return max1

#Input memory
print("Inputting memory...")

#Input dictionary of known words (NEW)
flip = 0
temp_line2 = ""
dictionary_file = open("dictionary2.txt", 'r')
for line in dictionary_file.readlines():
	if (not(flip)):
		dictionary[line.strip()] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 0, 'associated': {}}
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
		temp_associated = temp_list[6].split("%$%$%$")
		for associated_pair in temp_associated:
			temp_pair = associated_pair.split(':')
			if (temp_pair[0] == ''):
				continue
			dictionary[temp_line]['associated'][temp_pair[0]] = int(temp_pair[1])
dictionary_file.close()

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
	user_file = open("" + username + ".txt", 'r')
	for emotion in nEmotions:
		user_emotions[emotion] = int(user_file.readline())
	user_file.readline() #Skip to next line
	line = user_file.readline()
	if line.strip() != 'none':
		user_self['uam'] = line.strip().split("&%&%")
	line = user_file.readline()
	if line.strip() != 'none':
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
			
	#Ask CHELSEA what user is or is not
	match1 = re.search(r"what am i( not)?\?*$", userMessage)
	if (match1):
		if (not(match1.group(1)) and len(user_self['uam']) != 0):
			Xchatlog.append("CHELSEA (Thinking): Was asked what user is, have an answer.")
			botReply("You are " + re.sub(r"(your)", "my", random.choice(user_self['uam'])))
			continue
		elif (match1.group(1) and len(user_self['uamnot']) != 0):
			Xchatlog.append("CHELSEA (Thinking): Was asked what user is not, have an answer.")
			botReply("You are not " + re.sub(r"(your)", "my", random.choice(user_self['uamnot'])))
			continue
			
	#Tell CHELSEA what she is or is not and see if there's agreement according to her self memory
	match1 = re.search(r"(?:are you|you are|you're) (not )?([a-z '\-]*)\?*", userMessage)
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
			if (not(re.search(r"are you[a-z ]*\?*", userMessage))):
				self['iam'].append(match1.group(2))		
				Xchatlog.append("CHELSEA (Thinking): Learned new 'I am'.")
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
			if (not(re.search(r"are you[a-z '\-]*\?*", userMessage))):
				self['iamnot'].append(match1.group(2))		
				Xchatlog.append("CHELSEA (Thinking): Learned new 'I am not'.")
		
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
			Xchatlog.append("CHELSEA (Thinking): Learned new 'User am'.")
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
			Xchatlog.append("CHELSEA (Thinking): Learned new 'User am not'.")
				
	#Filter out punctuation from user message and split to list of words
	messageWords = (re.sub(r"([^a-z0-9 '\-])", '', userMessage)).split(" ")

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
			dictionary[word] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 0, 'associated': {}}
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
			try:
				dictionary[word]['associated'][word2] += 1
				Xchatlog.append("CHELSEA (Thinking): Added to count of association of " + word + " and " + word2)
				continue
			except(KeyError):
				dictionary[word]['associated'][word2] = 1
				Xchatlog.append("CHELSEA (Thinking): Learned association of " + word + " and " + word2)
				continue
		
	#Get counts for words in current conversation				
	for word in messageWords:
		if (dictionary[word]['emotion'] == 'permanent neutral' or dictionary[word]['emotion'] == 'temp neutral'):
			continue
		try:
			topics[word] += 1
		except(KeyError):
			topics[word] = 1
	
	#Get current topics of the conversation by the highest counts
	if (not(len(topics.keys()) == 0)):
		temp_highest = max(topics.values())
		current_topics = [k for k, v in topics.items() if v == temp_highest]
		Xchatlog.append("CHELSEA (Thinking): Current topic(s) is/are " + " & ".join(current_topics))
	
	#Check for possible matching answer to What Question in both keys and values under current mood
	responseMade = False
	whq_match_object = re.search(r"what (is|are) ([a-z '\-]+)\?*$", userMessage)

	temp_message_keys = list(messageDict[currentMood["mood"]].keys())
	random.shuffle(temp_message_keys) #Note, this shuffled list is potentially re-used in other parts of the script
	
	if (whq_match_object):
		temp_message_values = list(messageDict[currentMood["mood"]].values())
		random.shuffle(temp_message_values)
		partial_message = whq_match_object.group(2) + ' ' + whq_match_object.group(1)
		
		#Check values
		for message in temp_message_values:
			if (message == CHELSEAPreviousResponse):
				continue
			if message.find(partial_message) != -1:
				Xchatlog.append("CHELSEA (Thinking): WH-Q question match found in values.")
				CHELSEAPreviousResponse = botReply(message)
				responseMade = True
				break
		if responseMade:
			continue
		#Check keys
		for message in temp_message_keys:
			if (message == CHELSEAPreviousResponse):
				continue
			if message.find(partial_message) != -1:
				Xchatlog.append("CHELSEA (Thinking): WH-Q question match found in keys.")
				CHELSEAPreviousResponse = botReply(message)
				responseMade = True
				break
		if responseMade:
			continue
	
	#Check for question about previous message meaning
	meaning_match = re.search(r"(what (do you|does that) mean|(can you|(do you|can you) care to) clarify|I('m| am) confused|I do( not|n't) (understand|get( it)?)( what you mean| what (that|this) means)?|why (do|did) you (say|think) (that|this))\?*$", userMessage)
	if (meaning_match):
		previous_words = (re.sub(r"([^a-z0-9 '\-])", '', CHELSEAPreviousResponse)).split(" ")
		random.shuffle(previous_words)
		for message in temp_message_keys:
			if (message == CHELSEAPreviousResponse):
				continue
			match_count = 0
			match_words = []
			for word in previous_words:
				if (dictionary[word]['emotion'] == "temp neutral" or dictionary[word]['emotion'] == "permanent neutral"):
					continue
				if (len(match_words) != 0):
					repeated_word = False
					for word2 in match_words:
						if (word == word2):
							repeated_word = True
					if (repeated_word):
						continue
				if (message.find(word) != -1):
					match_count += 1
					match_words.append(word)
				if (match_count < 2):
					continue		
				else:
					Xchatlog.append("CHELSEA (Thinking): Previous words meaning match found for: " + " & ".join(match_words))
					CHELSEAPreviousResponse = botReply(message)
					responseMade = True
					break
			if responseMade:
				break
		if responseMade:
			continue
			
	#Ask what CHELSEA feels about ___
	feel_about_match = re.search(r"(?:how|what) do you (?:feel|think) (?:about|toward(?:s)?) ([a-z0-9, '\-]+)\?*$", userMessage)
	if (feel_about_match):
		feel_words = (re.sub(r"([^a-z0-9 '\-])", '', feel_about_match.group(1))).split(" ")
		temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
		for word in feel_words:
			if (dictionary[word]['emotion'] == 'temp neutral' or dictionary[word]['emotion'] == 'permanent neutral'):
				continue
			temp_dict[dictionary[word]['emotion']] += 1
		feel_emotion = getMood2(temp_dict, False)
		if (feel_emotion == 'temp neutral'):
			Xchatlog.append("CHELSEA (Thinking): Feel nothing.")
			CHELSEAPreviousResponse = botReply("i feel nothing about " + feel_about_match.group(1))
			responseMade = True
			continue
		else:
			Xchatlog.append("CHELSEA (Thinking): Have emotion to answer question.")
			CHELSEAPreviousResponse = botReply("i feel " + feel_emotion + ' about ' + feel_about_match.group(1))
			responseMade = True
			continue
			
	#Ask do you like question
	like_match = re.search(r"^do you (like|love|enjoy|adore|appreciate|dislike|hate|loathe|detest|despise) ([a-z0-9, '\-]+)\?*$", userMessage)
	if (like_match):
		like_terms = ['like', 'love', 'enjoy', 'adore', 'appreciate']
		dislike_terms = ['dislike', 'hate', 'loathe', 'detest', 'despise']
		like_words = (re.sub(r"([^a-z0-9 '\-])", '', like_match.group(2))).split(" ")
		temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
		for word in like_words:
			if (dictionary[word]['emotion'] == 'temp neutral' or dictionary[word]['emotion'] == 'permanent neutral'):
				continue
			temp_dict[dictionary[word]['emotion']] += 1
		like_emotion = getMood2(temp_dict, False)
		if (like_emotion != 'temp neutral'):
			Xchatlog.append("CHELSEA (Thinking): Like or dislike match found.")
			like_dislike = ''
			found = False
			for term in like_terms:
				if (like_match.group(1) == term):
					like_dislike = 'like'
					found = True
					break
			if (not(found)):
				like_dislike = 'dislike' 
			if ((like_emotion == 'happy' and like_dislike == 'like') or (like_emotion != 'happy' and like_dislike == 'dislike')):
				CHELSEAPreviousResponse = botReply("yes, i " + like_match.group(1) + ' ' + like_match.group(2))
			elif ((like_emotion == 'happy' and like_dislike == 'dislike') or (like_emotion != 'happy' and like_dislike == 'like')):
				CHELSEAPreviousResponse = botReply("no, i don't " + like_match.group(1) + ' ' + like_match.group(2))
			responseMade = True
			continue
		else:
			Xchatlog.append("CHELSEA (Thinking): Neither like or dislike")
			CHELSEAPreviousResponse = botReply("i don't feel anything about " + like_match.group(2))
			responseMade = True
			continue
			
	#Ask which is better, 1 or 2?
	better_match = re.search(r"(?:which|what) (?:is (?:better,? ?|best,? ?)|do you (?:like (?:better,? ?|best,? ?|more,? ?))) ([a-z0-9, '\-]+) or ([a-z0-9, '\-]+)\?*$", userMessage)
	if (better_match):
		better_words1 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(1))).split(" ")
		temp_dict1 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
		for word in better_words1:
			if (dictionary[word]['emotion'] == 'temp neutral' or dictionary[word]['emotion'] == 'permanent neutral'):
				continue
			temp_dict1[dictionary[word]['emotion']] += 1
		better_emotion1 = getMood2(temp_dict1, False)

		better_words2 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(2))).split(" ")
		temp_dict2 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
		for word in better_words2:
			if (dictionary[word]['emotion'] == 'temp neutral' or dictionary[word]['emotion'] == 'permanent neutral'):
				continue
			temp_dict2[dictionary[word]['emotion']] += 1
		better_emotion2 = getMood2(temp_dict2, False)
		
		if (better_emotion1 == 'happy' and better_emotion2 == 'happy'):
			Xchatlog.append("CHELSEA (Thinking): Found like both, determining which more.")
			happy_count1 = 0
			happy_count2 = 0
			for word in better_words1:
				happy_count1 += dictionary[word]['happy']
			for word in better_words2:
				happy_count2 += dictionary[word]['happy']
			if (happy_count1 > happy_count2):
				Xchatlog.append("CHELSEA (Thinking): Determined I like first option better.")
				CHELSEAPreviousResponse = botReply("i like both, but " + better_match.group(1) + ' most')
				responseMade = True
				continue
			elif (happy_count2 > happy_count1):
				Xchatlog.append("CHELSEA (Thinking): Determined I like second option better.")
				CHELSEAPreviousResponse = botReply("i like both, but " + better_match.group(2) + ' most')
				responseMade = True
				continue
			else:	
				Xchatlog.append("CHELSEA (Thinking): Determined I like both equally.")
				CHELSEAPreviousResponse = botReply("i like both " + better_match.group(1) + ' & ' + better_match.group(2) + ' the same')
				responseMade = True
				continue
		elif (better_emotion1 == 'happy' and better_emotion2 != 'happy'):
			Xchatlog.append("CHELSEA (Thinking): Found like first.")
			CHELSEAPreviousResponse = botReply("i like " + better_match.group(1) + ' better ')
			responseMade = True
			continue
		elif (better_emotion1 != 'happy' and better_emotion2 == 'happy'):
			Xchatlog.append("CHELSEA (Thinking): Found like second.")
			CHELSEAPreviousResponse = botReply("i like " + better_match.group(2) + ' better ')
			responseMade = True
			continue
		elif (better_emotion1 != 'happy' and better_emotion2 != 'happy'):
			Xchatlog.append("CHELSEA (Thinking): Like neither.")
			CHELSEAPreviousResponse = botReply("i don't prefer either " + better_match.group(1) + ' or ' + better_match.group(2))
			responseMade = True
			continue
			
	#Check for 'why is' question match
	whyis_match = re.search(r"why (?:is|are) ([a-z0-9, '\-]+)\?*$", userMessage)
	if (whyis_match):
		whyis_words = (re.sub(r"([^a-z0-9 '\-])", '', whyis_match.group(1))).split(" ")
		temp_message_values = list(messageDict[currentMood["mood"]].values())
		random.shuffle(temp_message_values)

		#Check values
		for message in temp_message_values:
			because_match = re.search(r"([a-z0-9, '\-]+) (because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)", message)
			if (because_match):
				match_count = 0
				for word in whyis_words:
					if ((because_match.group(1)).find(word) != -1):
						match_count += 1
					else:
						break
					if (match_count == len(whyis_words)):
						Xchatlog.append("CHELSEA (Thinking): Possible answer to 'why is' question match found in values for: " + " ".join(whyis_words))
						CHELSEAPreviousResponse = botReply(message)
						responseMade = True
						break
				if responseMade:
					break
		if responseMade:
			continue

		#Check keys
		for message in temp_message_keys:
			because_match = re.search(r"([a-z0-9, '\-]+) (because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)", message)
			if (because_match):
				match_count = 0
				for word in whyis_words:
					if ((because_match.group(1)).find(word) != -1):
						match_count += 1
					else:
						break
					if (match_count == len(whyis_words)):
						Xchatlog.append("CHELSEA (Thinking): Possible answer to 'why is' question match found in keys for: " + " ".join(whyis_words))
						CHELSEAPreviousResponse = botReply(message)
						responseMade = True
						break
				if responseMade:
					break
		if responseMade:
			continue
	
	#FLAG Ask 'most' question		
	max1 = []
	temp_emotion = ''
	happy_words = ['happy', 'contented', 'content', 'cheerful', 'cheery', 'merry', 'joyful', 'jovial', 'jolly', 'gleeful', 'delighted', 'joyous', 'thrilled', 'exuberant', 'elated', 'exhilarated', 'ecstatic', 'blissful', 'overjoyed']
	m1 = re.search(re.compile("what makes you most (" + "|".join(happy_words) + ")\?*$"), userMessage)
	if (m1):
		max1 = getMost(dictionary, 'happy')
		temp_emotion = 'happy'
		
	angry_words = ['angry', 'frustrated', 'irate', 'vexed', 'irritated', 'exasperated', 'indignant', 'aggrieved', 'irked', 'piqued', 'displeased', 'provoked', 'galled', 'resentful', 'furious', 'enraged', 'infuriated', 'raging', 'incandescent', 'wrathful', 'fuming', 'ranting', 'raving', 'seething', 'frenzied', 'beside oneself', 'outraged', 'choleric', 'crabby', 'waspish', 'hostile', 'antagonistic', 'mad', 'livid', 'boiling', 'riled', 'aggravated', 'sore', 'ticked off', 'ill-tempered', 'acrimonious']
	m1 = re.search(re.compile("what makes you most (" + "|".join(angry_words) + ")\?*$"), userMessage)
	if (m1):
		max1 = getMost(dictionary, 'angry')
		temp_emotion = 'angry'
	sad_words = ['sad', 'unhappy', 'sorrowful', 'depressed', 'downcast', 'miserable', 'glum', 'gloomy', 'dismal', 'blue', 'melancholy']
	m1 = re.search(re.compile("what makes you most (" + "|".join(sad_words) + ")\?*$"), userMessage)
	if (m1):
		max1 = getMost(dictionary, 'sad')
		temp_emotion = 'sad'
	afraid_words = ['afraid', 'frightened', 'scared', 'terrified', 'fearful', 'petrified', 'nervous', 'worried', 'panicky', 'timid', 'spooked']
	m1 = re.search(re.compile("what makes you most (" + "|".join(afraid_words) + ")\?*$"), userMessage)
	if (m1):
		max1 = getMost(dictionary, 'afraid')
		temp_emotion = 'afraid'	
	
	#Get max(es) for emotional words, respond accordingly	
	if (len(max1) == 1):	
		Xchatlog.append("CHELSEA (Thinking): Most " + temp_emotion + " match found.")
		CHELSEAPreviousResponse = botReply(max1[0] + " makes me most " + temp_emotion)
		responseMade = True
		continue
	elif (len(max1) > 1):
		Xchatlog.append("CHELSEA (Thinking): Most " + temp_emotion + " matches found.")
		CHELSEAPreviousResponse = botReply(random.choice(max1) + " is one of many that makes me most " + temp_emotion)
		responseMade = True
		continue
	
	#Check for exact match under current mood
	try:
		messageDict[currentMood["mood"]][userMessage]
		Xchatlog.append("CHELSEA (Thinking): Exact message match found.")
		CHELSEAPreviousResponse = botReply(messageDict[currentMood["mood"]][userMessage])
		continue
	except(KeyError):
		pass #Exact match not found in message dictionary
			
	#Check for partial match under current mood
	for message in temp_message_keys:
		if message.find(userMessage) != -1:
			Xchatlog.append("CHELSEA (Thinking): Partial message match found.")
			CHELSEAPreviousResponse = botReply(messageDict[currentMood["mood"]][message])
			responseMade = True
			break
	if responseMade:
		continue
		
	#Check for match with current topic
	if (not(len(topics.keys()) == 0) and (dictionaryCount >= 600 and responseCount >= 350 and random.randint(1, 4) == 1) or (dictionaryCount >= 2500 and responseCount >= 1200 and random.randint(1, 3) == 1)):
		for message in temp_message_keys:
			topics_found = True
			for topic in current_topics:
				if message.find(topic) == -1:
					topics_found = False
					break
			if (not(topics_found)):
				continue
			else:
				Xchatlog.append("CHELSEA (Thinking): Topic match found.")
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
						for message in temp_message_keys:
							if message.find(word) != -1:
								Xchatlog.append("CHELSEA (Thinking): Single term match found for term: " + word)
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
			#Single term match for a word associated with highest association count from user message word
			for word in messageWords:
				temp_dictionary = {}
				try:
					temp_dictionary = dictionary[word]['associated']
					if (len(temp_dictionary.keys()) == 0):
						continue
				except(KeyError):
					continue
				temp_highest = max(temp_dictionary.values())
				highest_associated = [k for k, v in temp_dictionary.items() if v == temp_highest]
				highest_associated_chosen = ''
				if (len(highest_associated) == 1):
					highest_associated_chosen = highest_associated[0]
				else:
					highest_associated_chosen = random.choice(highest_associated)
				if (dictionary[highest_associated_chosen]['emotion'] == "temp neutral" or dictionary[highest_associated_chosen]['emotion'] == "permanent neutral"):
					continue
						
				for message in temp_message_keys:
					if message.find(highest_associated_chosen) != -1:
						Xchatlog.append("CHELSEA (Thinking): Single term associated match found for associated term: " + highest_associated_chosen)
						CHELSEAPreviousResponse = botReply(messageDict[currentMood["mood"]][message])
						responseMade = True
						break
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
	Xchatlog.append("CHELSEA (Thinking): Gave random response.")	
	CHELSEAPreviousResponse = botReply(random.choice(list(messageDict[currentMood["mood"]].values())))

#Output memory
print("\nOutputting memory...")

#Output word dictionary file (NEW)
dictionary_file = open("dictionary2.txt", 'w')
for key in dictionary.keys():
	dictionary_file.write(key + "\n")
	for key2 in dictionary_keys_list:
		if (key2 == 'associated'):
			#word: value
			temp_associated = []
			for associated in dictionary[key][key2].keys():
				temp_associated.append(associated + ":" + str(dictionary[key][key2][associated]))
			dictionary_file.write(str("%$%$%$".join(temp_associated)) + "&!&!&!")
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
message_count = 0
for emotion in nEmotions:
	message_count += len(messageDict[emotion])
	data_file.write("Number of " + emotion + " message/response pairs: " + str(len(messageDict[emotion])) + "\n")
data_file.write("Total message/response pairs: " + str(message_count))
data_file.close()

#Output user profile (With educated guess emotional state) and user self properties
user_file = open("" + username + ".txt", 'w')
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
