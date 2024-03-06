#   Setup for Chatbot OPHELIA to talk to Chatbot CHELSEA
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

import random
import re
import os
from datetime import datetime
import time

emotionDictionary = {}
messageDict = {"happy": {}, "angry": {}, "sad": {}, "afraid": {}}
nEmotions = ["happy", "angry", "sad", "afraid"]
currentMood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
pitches = {"happy": 90, "angry": 80, "sad": 80, "afraid": 95}
speeds = {"happy": 150, "angry": 155, "sad": 135, "afraid": 155}
userMessage = " "
chatlog = []
Xchatlog = []
chatlogFile = {"regular": "OPHELIandCHELSEA_chatlog.txt", "extended": "OPHELIandCHELSEA_Xchatlog.txt" }
user_emotions = { "happy": 0, "angry": 0, "sad": 0, "afraid": 0 }

dictionary = {}
dictionary_keys_list = ['happy', 'angry', 'sad', 'afraid', 'emotion', 'seen', 'associated']
messageDict_CHELSEA = {"happy": {}, "angry": {}, "sad": {}, "afraid": {}}
currentMood_CHELSEA = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
pitches_CHELSEA = {"happy": 95, "angry": 80, "sad": 90, "afraid": 99}
speeds_CHELSEA = {"happy": 150, "angry": 155, "sad": 135, "afraid": 155}
userMessage_CHELSEA = " "
topics = {}

def addToMood():
	#Add the emotional values of the user reply to OPHELIA's emotional values
	for emotion in nEmotions:
		currentMood[emotion] += replyMood[emotion]

	#Change mood, pitch, and speaking speed according to OPHELIA's emotional values
	currentMood["mood"] = getMood(currentMood)
	currentMood["pitch"] = pitches[currentMood["mood"]]
	currentMood["speed"] = speeds[currentMood["mood"]]
	Xchatlog.append("OPHELIA (Thinking): I feel " + currentMood["mood"])
	
def getReplyMood():
	#Get the mood of the user reply by looking at the emotion counts gathered on it
	replyMood["mood"] = getMood(replyMood)

def getMood(moodDictionary):
	#Get the overall mood of either OPHELIA or the user's response
	if moodDictionary["angry"] > moodDictionary["happy"] and moodDictionary["angry"] > moodDictionary["sad"] and moodDictionary["angry"] > moodDictionary["afraid"]:
		return "angry"
	elif moodDictionary["sad"] > moodDictionary["angry"] and moodDictionary["sad"] > moodDictionary["happy"] and moodDictionary["sad"] > moodDictionary["afraid"]:
		return "sad"
	elif moodDictionary["afraid"] > moodDictionary["angry"] and moodDictionary["afraid"] > moodDictionary["sad"] and moodDictionary["afraid"] > moodDictionary["happy"]:
		return "afraid"
	else:
		return "happy"

def botReply(botResponse):
	#Do the various parts of OPHELIA's response, text output, text-to-speech with espeak, chatlogs
	print("OPHELIA: " + botResponse)
	os.system("espeak -v en+f4 -p {} -s {} \" {} \"".format(str(currentMood["pitch"]), str(currentMood["speed"]), botResponse))
	chatlog.append("OPHELIA: " + botResponse)
	Xchatlog.append("OPHELIA: " + botResponse)
	return botResponse
	
def addToMood_CHELSEA():
	#Add the emotional values of the user reply to CHELSEA's emotional values
	for emotion in nEmotions:
		currentMood_CHELSEA[emotion] += replyMood[emotion]

	#Change mood, pitch, and speaking speed according to CHELSEA's emotional values
	temp_dict = { 'happy': currentMood_CHELSEA['happy'], 'angry': currentMood_CHELSEA['angry'], 'sad': currentMood_CHELSEA['sad'], 'afraid': currentMood_CHELSEA['afraid'] }
	currentMood_CHELSEA["mood"] = getMood2(temp_dict, True)
	currentMood_CHELSEA["pitch"] = pitches_CHELSEA[currentMood_CHELSEA["mood"]]
	currentMood_CHELSEA["speed"] = speeds_CHELSEA[currentMood_CHELSEA["mood"]]
	Xchatlog.append("CHELSEA (Thinking): I feel " + currentMood_CHELSEA["mood"])

def getReplyMood_CHELSEA():
	#Get the mood of the user reply by looking at the emotion counts gathered on it
	temp_dict = { 'happy': replyMood['happy'], 'angry': replyMood['angry'], 'sad': replyMood['sad'], 'afraid': replyMood['afraid'] }
	replyMood["mood"] = getMood2(temp_dict, True)
	Xchatlog.append("CHELSEA (Thinking): OPHELIA seems to be " + replyMood["mood"])

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

def botReply_CHELSEA(botResponse):
	#Do the various parts of CHELSEA's response, text output, text-to-speech with espeak, chatlogs
	print("CHELSEA: " + botResponse)
	os.system("espeak -v en+f3 -p {} -s {} \" {} \"".format(str(currentMood_CHELSEA["pitch"]), str(currentMood_CHELSEA["speed"]), botResponse))
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

tempValues = []
emotion_dictionary_file = open("emotionDictionary.txt", 'r')
for line in emotion_dictionary_file.readlines():
	if line == "":
		break
	tempValues = (line.strip()).split(' ')
	emotionDictionary[tempValues[0]] = tempValues[1]
emotion_dictionary_file.close()

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
dictionaryCount = len(emotionDictionary)
responseCount = 0
for emotion in nEmotions:
	responseCount += len(messageDict[emotion])
	
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
message_dictionary_file = open("messageDictionary_CHELSEA.txt", 'r')
for emotion in nEmotions:
	messagesNo = int(message_dictionary_file.readline())
	for messages in range(0, messagesNo):
		if gotPair < 2:
			tempValues.append(message_dictionary_file.readline().strip())
			gotPair += 1
		if gotPair == 2:
			messageDict_CHELSEA[emotion][tempValues[0]] = tempValues[1]
			tempValues.clear()
			gotPair = 0
message_dictionary_file.close()

#Get counts for use in activating certain types of message detection
dictionaryCount_CHELSEA = len(dictionary.keys())
responseCount_CHELSEA = 0
for emotion in nEmotions:
	responseCount_CHELSEA += len(messageDict_CHELSEA[emotion])

print("Memory input complete!\n")

#Initial message
OPHELIAPreviousResponse = "hello"
botReply("hello, CHELSEA")
userMessage_CHELSEA = "hello"

#Chat loop
chatCount = 0

#Change to 100 after testing
while chatCount <= 100:

	chatCount += 1

	time.sleep(1)
	
	while(True):
		#Start CHELSEA code
		#Filter out punctuation from user message and split to list of words
		messageWords = (re.sub(r"([^a-z0-9 '\-])", '', userMessage_CHELSEA)).split(" ")

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
			
		getReplyMood_CHELSEA()
		addToMood_CHELSEA()

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
					breakout = False
					for word4 in temp_list:
						if (word2 == word4):
							breakout = True
							break
					if (breakout):
						continue
					else:
						dictionary[word]['associated'].append(word2)
						Xchatlog.append("CHELSEA (Thinking): Learned association of " + word + " and " + word2)
						break
			
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
		whq_match_object = re.search(r"what (is|are) ([a-z '\-]+)\?*$", userMessage_CHELSEA)

		temp_message_keys = list(messageDict_CHELSEA[currentMood_CHELSEA["mood"]].keys())
		random.shuffle(temp_message_keys) #Note, this shuffled list is potentially re-used in other parts of the script
		
		if (whq_match_object):
			temp_message_values = list(messageDict_CHELSEA[currentMood_CHELSEA["mood"]].values())
			random.shuffle(temp_message_values)
			partial_message = whq_match_object.group(2) + ' ' + whq_match_object.group(1)
			
			#Check values
			for message in temp_message_values:
				if (message == CHELSEAPreviousResponse):
					continue
				if message.find(partial_message) != -1:
					Xchatlog.append("CHELSEA (Thinking): WH-Q question match found in values.")
					CHELSEAPreviousResponse = botReply_CHELSEA(message)
					responseMade = True
					break
			if responseMade:
				break
			#Check keys
			for message in temp_message_keys:
				if (message == CHELSEAPreviousResponse):
					continue
				if message.find(partial_message) != -1:
					Xchatlog.append("CHELSEA (Thinking): WH-Q question match found in keys.")
					CHELSEAPreviousResponse = botReply_CHELSEA(message)
					responseMade = True
					break
			if responseMade:
				break
		
		#Check for question about previous message meaning
		meaning_match = re.search(r"(what (do you|does that) mean|(can you|(do you|can you) care to) clarify|I('m| am) confused|I do( not|n't) (understand|get( it)?)( what you mean| what (that|this) means)?|why (do|did) you (say|think) (that|this))\?*$", userMessage_CHELSEA)
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
						CHELSEAPreviousResponse = botReply_CHELSEA(message)
						responseMade = True
						break
				if responseMade:
					break
			if responseMade:
				break
				
		#Ask what CHELSEA feels about ___
		feel_about_match = re.search(r"(?:how|what) do you (?:feel|think) (?:about|toward(?:s)?) ([a-z0-9, '\-]+)\?*$", userMessage_CHELSEA)
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
				CHELSEAPreviousResponse = botReply_CHELSEA("i feel nothing about " + feel_about_match.group(1))
				responseMade = True
				continue
			else:
				Xchatlog.append("CHELSEA (Thinking): Have emotion to answer question.")
				CHELSEAPreviousResponse = botReply_CHELSEA("i feel " + feel_emotion + ' about ' + feel_about_match.group(1))
				responseMade = True
				continue
				
		#Ask do you like question
		like_match = re.search(r"^do you (like|love|enjoy|adore|appreciate|dislike|hate|loathe|detest|despise) ([a-z0-9, '\-]+)\?*$", userMessage_CHELSEA)
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
					CHELSEAPreviousResponse = botReply_CHELSEA("yes, i " + like_match.group(1) + ' ' + like_match.group(2))
				elif ((like_emotion == 'happy' and like_dislike == 'dislike') or (like_emotion != 'happy' and like_dislike == 'like')):
					CHELSEAPreviousResponse = botReply_CHELSEA("no, i don't " + like_match.group(1) + ' ' + like_match.group(2))
				responseMade = True
				break
			else:
				Xchatlog.append("CHELSEA (Thinking): Neither like or dislike")
				CHELSEAPreviousResponse = botReply_CHELSEA("i don't feel anything about " + like_match.group(2))
				responseMade = True
				break
				
		#Ask which is better, 1 or 2?
		better_match = re.search(r"(?:which|what) (?:is (?:better,? ?|best,? ?)|do you (?:like (?:better,? ?|best,? ?|more,? ?))) ([a-z0-9, '\-]+) or ([a-z0-9, '\-]+)\?*$", userMessage_CHELSEA)
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
					CHELSEAPreviousResponse = botReply_CHELSEA("i like both, but " + better_match.group(1) + ' most')
					responseMade = True
					continue
				elif (happy_count2 > happy_count1):
					Xchatlog.append("CHELSEA (Thinking): Determined I like second option better.")
					CHELSEAPreviousResponse = botReply_CHELSEA("i like both, but " + better_match.group(2) + ' most')
					responseMade = True
					continue
				else:	
					Xchatlog.append("CHELSEA (Thinking): Determined I like both equally.")
					CHELSEAPreviousResponse = botReply_CHELSEA("i like both " + better_match.group(1) + ' & ' + better_match.group(2) + ' the same')
					responseMade = True
					continue
			elif (better_emotion1 == 'happy' and better_emotion2 != 'happy'):
				Xchatlog.append("CHELSEA (Thinking): Found like first.")
				CHELSEAPreviousResponse = botReply_CHELSEA("i like " + better_match.group(1) + ' better ')
				responseMade = True
				continue
			elif (better_emotion1 != 'happy' and better_emotion2 == 'happy'):
				Xchatlog.append("CHELSEA (Thinking): Found like second.")
				CHELSEAPreviousResponse = botReply_CHELSEA("i like " + better_match.group(2) + ' better ')
				responseMade = True
				continue
			elif (better_emotion1 != 'happy' and better_emotion2 != 'happy'):
				Xchatlog.append("CHELSEA (Thinking): Like neither.")
				CHELSEAPreviousResponse = botReply_CHELSEA("i don't prefer either " + better_match.group(1) + ' or ' + better_match.group(2))
				responseMade = True
				continue
				
		#Check for 'why is' question match
		whyis_match = re.search(r"why (?:is|are) ([a-z0-9, '\-]+)\?*$", userMessage_CHELSEA)
		if (whyis_match):
			whyis_words = (re.sub(r"([^a-z0-9 '\-])", '', whyis_match.group(1))).split(" ")
			temp_message_values = list(messageDict_CHELSEA[currentMood_CHELSEA["mood"]].values())
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
							CHELSEAPreviousResponse = botReply_CHELSEA(message)
							responseMade = True
							break
					if responseMade:
						break
			if responseMade:
				break

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
							CHELSEAPreviousResponse = botReply_CHELSEA(message)
							responseMade = True
							break
					if responseMade:
						break
			if responseMade:
				break
		
		#Check for exact match under current mood
		try:
			messageDict_CHELSEA[currentMood_CHELSEA["mood"]][userMessage_CHELSEA]
			Xchatlog.append("CHELSEA (Thinking): Exact message match found.")
			CHELSEAPreviousResponse = botReply_CHELSEA(messageDict_CHELSEA[currentMood_CHELSEA["mood"]][userMessage_CHELSEA])
			break
		except(KeyError):
			pass #Exact match not found in message dictionary
				
		#Check for partial match under current mood
		for message in temp_message_keys:
			if message.find(userMessage_CHELSEA) != -1:
				Xchatlog.append("CHELSEA (Thinking): Partial message match found.")
				CHELSEAPreviousResponse = botReply_CHELSEA(messageDict_CHELSEA[currentMood_CHELSEA["mood"]][message])
				responseMade = True
				break
		if responseMade:
			break
			
		#Check for match with current topic
		if (not(len(topics.keys()) == 0) and (dictionaryCount_CHELSEA >= 600 and responseCount_CHELSEA >= 350 and random.randint(1, 4) == 1) or (dictionaryCount_CHELSEA >= 2500 and responseCount_CHELSEA >= 1200 and random.randint(1, 3) == 1)):
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
					CHELSEAPreviousResponse = botReply_CHELSEA(messageDict_CHELSEA[currentMood_CHELSEA["mood"]][message])
					responseMade = True
					break
			if responseMade:
				break
			
		#Check for single term match under current mood, ignore neutral words
		#Only activated when she has learned enough, though this can easily be adjusted
		if ((dictionaryCount_CHELSEA >= 2000 and responseCount_CHELSEA >= 500 and random.randint(1, 4) == 1) or (dictionaryCount_CHELSEA >= 4500 and responseCount_CHELSEA >= 2700 and random.randint(1, 3) == 1)):
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
									CHELSEAPreviousResponse = botReply_CHELSEA(messageDict_CHELSEA[currentMood_CHELSEA["mood"]][message])
									responseMade = True
									break
							if responseMade:
								break
					except(KeyError):
						continue
				if responseMade:
					break
			else:
				#Single term match for a word associated with user message word
				for word in messageWords:
					temp_words = []
					try:
						temp_words = dictionary[word]['associated'][:]
					except(KeyError):
						continue
					if (len(temp_words) == 1 and temp_words[0] == ''):
						continue
						
					random.shuffle(temp_words)
					for word2 in temp_words:
						if (word2 == ''):
							continue
						try:
							if (dictionary[word2]['emotion'] == "temp neutral" or dictionary[word2]['emotion'] == "permanent neutral"):
								continue
							else:
								for message in temp_message_keys:
									if message.find(word2) != -1:
										Xchatlog.append("CHELSEA (Thinking): Single term associated match found for associated term: " + word2)
										CHELSEAPreviousResponse = botReply_CHELSEA(messageDict_CHELSEA[currentMood_CHELSEA["mood"]][message])
										responseMade = True
										break
								if responseMade:
									break
						except(KeyError):
							continue
					if responseMade:
						break
				if responseMade:
					break
					 	
				
		#No match, either overwrite old response or learn new one based on reply mood
		Xchatlog.append("CHELSEA (Thinking): Message not recognized.")
		try:
			messageDict_CHELSEA[replyMood["mood"]][CHELSEAPreviousResponse]
			Xchatlog.append("CHELSEA (Thinking): Overwrote old '" + replyMood["mood"] + "' response.")
		except(KeyError):
			Xchatlog.append("CHELSEA (Thinking): Learned new '" + replyMood["mood"] + "' response.")
		messageDict_CHELSEA[replyMood["mood"]][CHELSEAPreviousResponse] = userMessage_CHELSEA

		#Give random response from current mood
		Xchatlog.append("CHELSEA (Thinking): Gave random response.")	
		CHELSEAPreviousResponse = botReply_CHELSEA(random.choice(list(messageDict_CHELSEA[currentMood_CHELSEA["mood"]].values())))
		break
			
	time.sleep(1)

	while(True):
		userMessage = CHELSEAPreviousResponse
		#Filter out punctuation from user message and split to list of words
		messageWords = (re.sub(r"(\.|\?|\!|,)", "", userMessage)).split(" ")

		#Detect emotion words, get reply mood, add user reply emotional values to OPHELIA's emotional values
		unknownWords = []
		replyMood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0}

		wordEmotions = ""
		for word in messageWords:
			if word == '':
				continue
			try:
				if emotionDictionary[word] != "neutral":
					replyMood[emotionDictionary[word]] += 1
					user_emotions[emotionDictionary[word]] += 1
					wordEmotions = wordEmotions + emotionDictionary[word] + " "
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
			Xchatlog.append("OPHELIA (Thinking): Unknown words detected: " + str(unknownWords))
			for word in unknownWords:
				emotionDictionary[word] = replyMood["mood"] 
			Xchatlog.append("OPHELIA (Thinking): Learned unknown words as '" + replyMood["mood"] + "' words.") 
		
		#Check for exact match under current mood
		try:
			messageDict[currentMood["mood"]][userMessage]
			Xchatlog.append("OPHELIA (Thinking): Exact message match found.")
			OPHELIAPreviousResponse = botReply(messageDict[currentMood["mood"]][userMessage])
			userMessage_CHELSEA = OPHELIAPreviousResponse
			break
		except(KeyError):
			pass #Exact match not found in message dictionary
		
		#Check for partial match under current mood
		responseMade = False
		for message in messageDict[currentMood["mood"]].keys():
			if message.find(userMessage) != -1:
				Xchatlog.append("OPHELIA (Thinking): Partial message match found.")
				OPHELIAPreviousResponse = botReply(messageDict[currentMood["mood"]][message])
				userMessage_CHELSEA = OPHELIAPreviousResponse
				responseMade = True
				break
		if responseMade:
			break
			
		#Check for single term match under current mood, ignore neutral words
		#Only activated when she has learned enough, though this can easily be adjusted
		if ((dictionaryCount >= 2000 and responseCount >= 500 and random.randint(1, 4) == 1) or (dictionaryCount >= 3000 and responseCount >= 850 and random.randint(1, 3) == 1) or (dictionaryCount >= 3600 and responseCount >= 1100 and random.randint(1, 2) == 1)):
			responseMade = False
			for word in messageWords:
				try:
					if (emotionDictionary[word] == "neutral"):
						continue
					else:
						for message in messageDict[currentMood["mood"]].keys():
							if message.find(word) != -1:
								Xchatlog.append("OPHELIA (Thinking): Single term match found.")
								OPHELIAPreviousResponse = botReply(messageDict[currentMood["mood"]][message])
								userMessage_CHELSEA = OPHELIAPreviousResponse
								responseMade = True
								break
						if responseMade:
							break
				except(KeyError):
					continue
			if responseMade:
				break
					 	
				
		#No match, either overwrite old response or learn new one based on reply mood
		Xchatlog.append("OPHELIA (Thinking): Message not recognized.")
		try:
			messageDict[replyMood["mood"]][OPHELIAPreviousResponse]
			Xchatlog.append("OPHELIA (Thinking): Overwrote old '" + replyMood["mood"] + "' response.")
		except(KeyError):
			Xchatlog.append("OPHELIA (Thinking): Learned new '" + replyMood["mood"] + "' response.")
		messageDict[replyMood["mood"]][OPHELIAPreviousResponse] = userMessage

		#Give random response from current mood	
		OPHELIAPreviousResponse = botReply(random.choice(list(messageDict[currentMood["mood"]].values())))
		userMessage_CHELSEA = OPHELIAPreviousResponse
		break

print("\nEND OF CHAT\n")

print("Outputting chatlogs...")
#Output regular and extended chatlogs
chatlogOutput(chatlogFile["regular"], chatlog)
print("Chatlog output complete.")
chatlogOutput(chatlogFile["extended"], Xchatlog)
