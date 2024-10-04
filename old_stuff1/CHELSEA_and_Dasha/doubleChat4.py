#   Setup for Chatbot CHELSEA to talk to a copy of herself named 'Dasha'
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

messageDict = {"happy": {}, "angry": {}, "sad": {}, "afraid": {}}
nEmotions = ["happy", "angry", "sad", "afraid"]
userMessage = " "
chatlog = []
Xchatlog = []
chatlogFile = {"regular": "CHELSEA_and_Dasha_chatlog.txt", "extended": "CHELSEA_and_Dasha_Xchatlog.txt" }
user_emotions = { "happy": 0, "angry": 0, "sad": 0, "afraid": 0 }

dictionary = {}
dictionary_keys_list = ['happy', 'angry', 'sad', 'afraid', 'emotion', 'seen', 'associated']
messageDict_CHELSEA = {"happy": {}, "angry": {}, "sad": {}, "afraid": {}}
currentMood_CHELSEA = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
pitches_CHELSEA = {"happy": 95, "angry": 80, "sad": 90, "afraid": 99}
speeds_CHELSEA = {"happy": 150, "angry": 155, "sad": 135, "afraid": 155}
userMessage_CHELSEA = " "
topics = {}

dictionary_Dasha = {}
messageDict_Dasha = {"happy": {}, "angry": {}, "sad": {}, "afraid": {}}
currentMood_Dasha = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
pitches_Dasha = {"happy": 95, "angry": 80, "sad": 90, "afraid": 99}
speeds_Dasha = {"happy": 150, "angry": 155, "sad": 135, "afraid": 155}
userMessage_Dasha = " "
topics_Dasha = {}

def addToMood_Dasha():
	#Add the emotional values of the user reply to Dasha's emotional values
	for emotion in nEmotions:
		currentMood_Dasha[emotion] += replyMood[emotion]

	#Change mood, pitch, and speaking speed according to Dasha's emotional values
	temp_dict = { 'happy': currentMood_Dasha['happy'], 'angry': currentMood_Dasha['angry'], 'sad': currentMood_Dasha['sad'], 'afraid': currentMood_Dasha['afraid'] }
	currentMood_Dasha["mood"] = getMood2(temp_dict, True)
	currentMood_Dasha["pitch"] = pitches_Dasha[currentMood_Dasha["mood"]]
	currentMood_Dasha["speed"] = speeds_Dasha[currentMood_Dasha["mood"]]
	Xchatlog.append("Dasha (Thinking): I feel " + currentMood_Dasha["mood"])

def getReplyMood_Dasha():
	#Get the mood of the user reply by looking at the emotion counts gathered on it
	temp_dict = { 'happy': replyMood['happy'], 'angry': replyMood['angry'], 'sad': replyMood['sad'], 'afraid': replyMood['afraid'] }
	replyMood["mood"] = getMood2(temp_dict, True)
	Xchatlog.append("Dasha (Thinking): OPHELIA seems to be " + replyMood["mood"])

def botReply_Dasha(botResponse):
	#Do the various parts of Dasha's response, text output, text-to-speech with espeak, chatlogs
	print("Dasha: " + botResponse)
	os.system("espeak -v en+f3 -p {} -s {} \" {} \"".format(str(currentMood_Dasha["pitch"]), str(currentMood_Dasha["speed"]), botResponse))
	chatlog.append("Dasha: " + botResponse)
	Xchatlog.append("Dasha: " + botResponse)
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

#Input dictionary_Dasha of known words
flip = 0
temp_line = ""
dictionary_Dasha_file = open("dictionary_Dasha.txt", 'r')
for line in dictionary_Dasha_file.readlines():
	if (not(flip)):
		dictionary_Dasha[line.strip()] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 0, 'associated': []}
		flip = 1
		temp_line = line.strip()
		continue
	else:
		temp_list = line.strip().split("&!&!&!")
		for n in range(0, 6):
			if (dictionary_keys_list[n] == 'happy' or dictionary_keys_list[n] == 'angry' or dictionary_keys_list[n] == 'sad' or dictionary_keys_list[n] == 'afraid' or dictionary_keys_list[n] == 'seen'):
				dictionary_Dasha[temp_line][dictionary_keys_list[n]] = int(temp_list[n])
			else:
				dictionary_Dasha[temp_line][dictionary_keys_list[n]] = temp_list[n]
		flip = 0
		dictionary_Dasha[temp_line]['associated'] = temp_list[6].split("%$%$%$")

#Input dictionary_Dasha of message/response pairs
gotPair = 0
tempValues = []
message_dictionary_Dasha_file = open("messageDictionary_Dasha.txt", 'r')
for emotion in nEmotions:
	messagesNo = int(message_dictionary_Dasha_file.readline())
	for messages in range(0, messagesNo):
		if gotPair < 2:
			tempValues.append(message_dictionary_Dasha_file.readline().strip())
			gotPair += 1
		if gotPair == 2:
			messageDict_Dasha[emotion][tempValues[0]] = tempValues[1]
			tempValues.clear()
			gotPair = 0
message_dictionary_Dasha_file.close()

#Get counts for use in activating certain types of message detection
dictionaryCount_Dasha = len(dictionary_Dasha.keys())
responseCount_Dasha = 0
for emotion in nEmotions:
	responseCount_Dasha += len(messageDict_Dasha[emotion])
	
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
DashaPreviousResponse = "hello"
botReply_Dasha("hello, CHELSEA")
userMessage_CHELSEA = "hello"

#Chat loop
chatCount = 0

#Change to 100 after testing
while chatCount <= 100:

	chatCount += 1

	time.sleep(1)
	
	while(True):
	
		userMessage_CHELSEA = DashaPreviousResponse
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
		Xchatlog.append("\n\n")
		
		userMessage_Dasha = CHELSEAPreviousResponse
	
		#Start Dasha code
		#Filter out punctuation from user message and split to list of words
		messageWords = (re.sub(r"([^a-z0-9 '\-])", '', userMessage_Dasha)).split(" ")

		#Detect emotion words, get reply mood, add user reply emotional values to Dasha's emotional values
		unknownWords = []
		replyMood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0}

		wordEmotions = ""
		for word in messageWords:
			if word == '':
				continue
			try:
				if (dictionary_Dasha[word]['emotion'] != "permanent neutral" and dictionary_Dasha[word]['emotion'] != "temp neutral"):
					replyMood[dictionary_Dasha[word]['emotion']] += 1
					user_emotions[dictionary_Dasha[word]['emotion']] += 1
					wordEmotions = wordEmotions + dictionary_Dasha[word]['emotion'] + " "
				else: 
					wordEmotions = wordEmotions + " neutral "
			except(KeyError):
				unknownWords.append(word)
				wordEmotions = wordEmotions + " unknown "
		Xchatlog.append("Word emotions in previous reply: " + wordEmotions)
			
		getReplyMood_Dasha()
		addToMood_Dasha()

		#Mark unknown words in the emotion dictionary_Dasha according to the overall mood of the user reply
		if len(unknownWords) > 0:
			Xchatlog.append("Dasha (Thinking): Unknown words detected: " + str(unknownWords))
			for word in unknownWords:
				dictionary_Dasha[word] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 0, 'associated': ()}
				dictionary_Dasha[word]['emotion'] = replyMood["mood"] 
			Xchatlog.append("Dasha (Thinking): Learned unknown words as '" + replyMood["mood"] + "' words.")
			
		#Add to counts for each word
		for word in messageWords:
			if (dictionary_Dasha[word]['emotion'] == 'permanent neutral' or dictionary_Dasha[word]['emotion'] == 'temp neutral'):
				continue
			dictionary_Dasha[word][replyMood["mood"]] += 1
			temp_dict = { 'happy': dictionary_Dasha[word]['happy'], 'angry': dictionary_Dasha[word]['angry'], 'sad': dictionary_Dasha[word]['sad'], 'afraid': dictionary_Dasha[word]['afraid'] }
			word_emotion = getMood2(temp_dict, False)
			if (word_emotion != dictionary_Dasha[word]['emotion']):
				dictionary_Dasha[word]['emotion'] = word_emotion
				Xchatlog.append("Dasha (Thinking): Switched emotion of word '" + word + "' to " + word_emotion)
			
		#Mark associated words in list
		for word in messageWords:
			try:
				if (dictionary_Dasha[word]['emotion'] == 'permanent neutral' or dictionary_Dasha[word]['emotion'] == 'temp neutral'):
					continue
			except(KeyError):
				continue
			for word2 in messageWords:
				if (word == word2):
					continue
				try:
					if (dictionary_Dasha[word2]['emotion'] == 'permanent neutral' or dictionary_Dasha[word2]['emotion'] == 'temp neutral'):
						continue
				except(KeyError):
					continue
				
				temp_list = dictionary_Dasha[word]['associated'][:]
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
						dictionary_Dasha[word]['associated'].append(word2)
						Xchatlog.append("Dasha (Thinking): Learned association of " + word + " and " + word2)
						break
			
		#Get counts for words in current conversation				
		for word in messageWords:
			if (dictionary_Dasha[word]['emotion'] == 'permanent neutral' or dictionary_Dasha[word]['emotion'] == 'temp neutral'):
				continue
			try:
				topics_Dasha[word] += 1
			except(KeyError):
				topics_Dasha[word] = 1
		
		#Get current topics_Dasha of the conversation by the highest counts
		if (not(len(topics_Dasha.keys()) == 0)):
			temp_highest = max(topics_Dasha.values())
			current_topics_Dasha = [k for k, v in topics_Dasha.items() if v == temp_highest]
			Xchatlog.append("Dasha (Thinking): Current topic(s) is/are " + " & ".join(current_topics_Dasha))
		
		#Check for possible matching answer to What Question in both keys and values under current mood
		responseMade = False
		whq_match_object = re.search(r"what (is|are) ([a-z '\-]+)\?*$", userMessage_Dasha)

		temp_message_keys = list(messageDict_Dasha[currentMood_Dasha["mood"]].keys())
		random.shuffle(temp_message_keys) #Note, this shuffled list is potentially re-used in other parts of the script
		
		if (whq_match_object):
			temp_message_values = list(messageDict_Dasha[currentMood_Dasha["mood"]].values())
			random.shuffle(temp_message_values)
			partial_message = whq_match_object.group(2) + ' ' + whq_match_object.group(1)
			
			#Check values
			for message in temp_message_values:
				if (message == DashaPreviousResponse):
					continue
				if message.find(partial_message) != -1:
					Xchatlog.append("Dasha (Thinking): WH-Q question match found in values.")
					DashaPreviousResponse = botReply_Dasha(message)
					responseMade = True
					break
			if responseMade:
				break
			#Check keys
			for message in temp_message_keys:
				if (message == DashaPreviousResponse):
					continue
				if message.find(partial_message) != -1:
					Xchatlog.append("Dasha (Thinking): WH-Q question match found in keys.")
					DashaPreviousResponse = botReply_Dasha(message)
					responseMade = True
					break
			if responseMade:
				break
		
		#Check for question about previous message meaning
		meaning_match = re.search(r"(what (do you|does that) mean|(can you|(do you|can you) care to) clarify|I('m| am) confused|I do( not|n't) (understand|get( it)?)( what you mean| what (that|this) means)?|why (do|did) you (say|think) (that|this))\?*$", userMessage_Dasha)
		if (meaning_match):
			previous_words = (re.sub(r"([^a-z0-9 '\-])", '', DashaPreviousResponse)).split(" ")
			random.shuffle(previous_words)
			for message in temp_message_keys:
				if (message == DashaPreviousResponse):
					continue
				match_count = 0
				match_words = []
				for word in previous_words:
					if (dictionary_Dasha[word]['emotion'] == "temp neutral" or dictionary_Dasha[word]['emotion'] == "permanent neutral"):
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
						Xchatlog.append("Dasha (Thinking): Previous words meaning match found for: " + " & ".join(match_words))
						DashaPreviousResponse = botReply_Dasha(message)
						responseMade = True
						break
				if responseMade:
					break
			if responseMade:
				break
				
		#Ask what Dasha feels about ___
		feel_about_match = re.search(r"(?:how|what) do you (?:feel|think) (?:about|toward(?:s)?) ([a-z0-9, '\-]+)\?*$", userMessage_Dasha)
		if (feel_about_match):
			feel_words = (re.sub(r"([^a-z0-9 '\-])", '', feel_about_match.group(1))).split(" ")
			temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in feel_words:
				if (dictionary_Dasha[word]['emotion'] == 'temp neutral' or dictionary_Dasha[word]['emotion'] == 'permanent neutral'):
					continue
				temp_dict[dictionary_Dasha[word]['emotion']] += 1
			feel_emotion = getMood2(temp_dict, False)
			if (feel_emotion == 'temp neutral'):
				Xchatlog.append("Dasha (Thinking): Feel nothing.")
				DashaPreviousResponse = botReply_Dasha("i feel nothing about " + feel_about_match.group(1))
				responseMade = True
				continue
			else:
				Xchatlog.append("Dasha (Thinking): Have emotion to answer question.")
				DashaPreviousResponse = botReply_Dasha("i feel " + feel_emotion + ' about ' + feel_about_match.group(1))
				responseMade = True
				continue
				
		#Ask do you like question
		like_match = re.search(r"^do you (like|love|enjoy|adore|appreciate|dislike|hate|loathe|detest|despise) ([a-z0-9, '\-]+)\?*$", userMessage_Dasha)
		if (like_match):
			like_terms = ['like', 'love', 'enjoy', 'adore', 'appreciate']
			dislike_terms = ['dislike', 'hate', 'loathe', 'detest', 'despise']
			like_words = (re.sub(r"([^a-z0-9 '\-])", '', like_match.group(2))).split(" ")
			temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in like_words:
				if (dictionary_Dasha[word]['emotion'] == 'temp neutral' or dictionary_Dasha[word]['emotion'] == 'permanent neutral'):
					continue
				temp_dict[dictionary_Dasha[word]['emotion']] += 1
			like_emotion = getMood2(temp_dict, False)
			if (like_emotion != 'temp neutral'):
				Xchatlog.append("Dasha (Thinking): Like or dislike match found.")
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
					DashaPreviousResponse = botReply_Dasha("yes, i " + like_match.group(1) + ' ' + like_match.group(2))
				elif ((like_emotion == 'happy' and like_dislike == 'dislike') or (like_emotion != 'happy' and like_dislike == 'like')):
					DashaPreviousResponse = botReply_Dasha("no, i don't " + like_match.group(1) + ' ' + like_match.group(2))
				responseMade = True
				break
			else:
				Xchatlog.append("Dasha (Thinking): Neither like or dislike")
				DashaPreviousResponse = botReply_Dasha("i don't feel anything about " + like_match.group(2))
				responseMade = True
				break
				
		#Ask which is better, 1 or 2?
		better_match = re.search(r"(?:which|what) (?:is (?:better,? ?|best,? ?)|do you (?:like (?:better,? ?|best,? ?|more,? ?))) ([a-z0-9, '\-]+) or ([a-z0-9, '\-]+)\?*$", userMessage_Dasha)
		if (better_match):
			better_words1 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(1))).split(" ")
			temp_dict1 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in better_words1:
				if (dictionary_Dasha[word]['emotion'] == 'temp neutral' or dictionary_Dasha[word]['emotion'] == 'permanent neutral'):
					continue
				temp_dict1[dictionary_Dasha[word]['emotion']] += 1
			better_emotion1 = getMood2(temp_dict1, False)

			better_words2 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(2))).split(" ")
			temp_dict2 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in better_words2:
				if (dictionary_Dasha[word]['emotion'] == 'temp neutral' or dictionary_Dasha[word]['emotion'] == 'permanent neutral'):
					continue
				temp_dict2[dictionary_Dasha[word]['emotion']] += 1
			better_emotion2 = getMood2(temp_dict2, False)
			
			if (better_emotion1 == 'happy' and better_emotion2 == 'happy'):
				Xchatlog.append("Dasha (Thinking): Found like both, determining which more.")
				happy_count1 = 0
				happy_count2 = 0
				for word in better_words1:
					happy_count1 += dictionary_Dasha[word]['happy']
				for word in better_words2:
					happy_count2 += dictionary_Dasha[word]['happy']
				if (happy_count1 > happy_count2):
					Xchatlog.append("Dasha (Thinking): Determined I like first option better.")
					DashaPreviousResponse = botReply_Dasha("i like both, but " + better_match.group(1) + ' most')
					responseMade = True
					continue
				elif (happy_count2 > happy_count1):
					Xchatlog.append("Dasha (Thinking): Determined I like second option better.")
					DashaPreviousResponse = botReply_Dasha("i like both, but " + better_match.group(2) + ' most')
					responseMade = True
					continue
				else:	
					Xchatlog.append("Dasha (Thinking): Determined I like both equally.")
					DashaPreviousResponse = botReply_Dasha("i like both " + better_match.group(1) + ' & ' + better_match.group(2) + ' the same')
					responseMade = True
					continue
			elif (better_emotion1 == 'happy' and better_emotion2 != 'happy'):
				Xchatlog.append("Dasha (Thinking): Found like first.")
				DashaPreviousResponse = botReply_Dasha("i like " + better_match.group(1) + ' better ')
				responseMade = True
				continue
			elif (better_emotion1 != 'happy' and better_emotion2 == 'happy'):
				Xchatlog.append("Dasha (Thinking): Found like second.")
				DashaPreviousResponse = botReply_Dasha("i like " + better_match.group(2) + ' better ')
				responseMade = True
				continue
			elif (better_emotion1 != 'happy' and better_emotion2 != 'happy'):
				Xchatlog.append("Dasha (Thinking): Like neither.")
				DashaPreviousResponse = botReply_Dasha("i don't prefer either " + better_match.group(1) + ' or ' + better_match.group(2))
				responseMade = True
				continue
				
		#Check for 'why is' question match
		whyis_match = re.search(r"why (?:is|are) ([a-z0-9, '\-]+)\?*$", userMessage_Dasha)
		if (whyis_match):
			whyis_words = (re.sub(r"([^a-z0-9 '\-])", '', whyis_match.group(1))).split(" ")
			temp_message_values = list(messageDict_Dasha[currentMood_Dasha["mood"]].values())
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
							Xchatlog.append("Dasha (Thinking): Possible answer to 'why is' question match found in values for: " + " ".join(whyis_words))
							DashaPreviousResponse = botReply_Dasha(message)
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
							Xchatlog.append("Dasha (Thinking): Possible answer to 'why is' question match found in keys for: " + " ".join(whyis_words))
							DashaPreviousResponse = botReply_Dasha(message)
							responseMade = True
							break
					if responseMade:
						break
			if responseMade:
				break
		
		#Check for exact match under current mood
		try:
			messageDict_Dasha[currentMood_Dasha["mood"]][userMessage_Dasha]
			Xchatlog.append("Dasha (Thinking): Exact message match found.")
			DashaPreviousResponse = botReply_Dasha(messageDict_Dasha[currentMood_Dasha["mood"]][userMessage_Dasha])
			break
		except(KeyError):
			pass #Exact match not found in message dictionary_Dasha
				
		#Check for partial match under current mood
		for message in temp_message_keys:
			if message.find(userMessage_Dasha) != -1:
				Xchatlog.append("Dasha (Thinking): Partial message match found.")
				DashaPreviousResponse = botReply_Dasha(messageDict_Dasha[currentMood_Dasha["mood"]][message])
				responseMade = True
				break
		if responseMade:
			break
			
		#Check for match with current topic
		if (not(len(topics_Dasha.keys()) == 0) and (dictionaryCount_Dasha >= 600 and responseCount_Dasha >= 350 and random.randint(1, 4) == 1) or (dictionaryCount_Dasha >= 2500 and responseCount_Dasha >= 1200 and random.randint(1, 3) == 1)):
			for message in temp_message_keys:
				topics_Dasha_found = True
				for topic in current_topics_Dasha:
					if message.find(topic) == -1:
						topics_Dasha_found = False
						break
				if (not(topics_Dasha_found)):
					continue
				else:
					Xchatlog.append("Dasha (Thinking): Topic match found.")
					DashaPreviousResponse = botReply_Dasha(messageDict_Dasha[currentMood_Dasha["mood"]][message])
					responseMade = True
					break
			if responseMade:
				break
			
		#Check for single term match under current mood, ignore neutral words
		#Only activated when she has learned enough, though this can easily be adjusted
		if ((dictionaryCount_Dasha >= 2000 and responseCount_Dasha >= 500 and random.randint(1, 4) == 1) or (dictionaryCount_Dasha >= 4500 and responseCount_Dasha >= 2700 and random.randint(1, 3) == 1)):
			responseMade = False
			#Coin flip
			if (random.randint(1, 2) == 1):
				#single term match from user message words
				for word in messageWords:
					try:
						if (dictionary_Dasha[word]['emotion'] == "temp neutral" or dictionary_Dasha[word]['emotion'] == "permanent neutral"):
							continue
						else:
							for message in temp_message_keys:
								if message.find(word) != -1:
									Xchatlog.append("Dasha (Thinking): Single term match found for term: " + word)
									DashaPreviousResponse = botReply_Dasha(messageDict_Dasha[currentMood_Dasha["mood"]][message])
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
						temp_words = dictionary_Dasha[word]['associated'][:]
					except(KeyError):
						continue
					if (len(temp_words) == 1 and temp_words[0] == ''):
						continue
						
					random.shuffle(temp_words)
					for word2 in temp_words:
						if (word2 == ''):
							continue
						try:
							if (dictionary_Dasha[word2]['emotion'] == "temp neutral" or dictionary_Dasha[word2]['emotion'] == "permanent neutral"):
								continue
							else:
								for message in temp_message_keys:
									if message.find(word2) != -1:
										Xchatlog.append("Dasha (Thinking): Single term associated match found for associated term: " + word2)
										DashaPreviousResponse = botReply_Dasha(messageDict_Dasha[currentMood_Dasha["mood"]][message])
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
		Xchatlog.append("Dasha (Thinking): Message not recognized.")
		try:
			messageDict_Dasha[replyMood["mood"]][DashaPreviousResponse]
			Xchatlog.append("Dasha (Thinking): Overwrote old '" + replyMood["mood"] + "' response.")
		except(KeyError):
			Xchatlog.append("Dasha (Thinking): Learned new '" + replyMood["mood"] + "' response.")
		messageDict_Dasha[replyMood["mood"]][DashaPreviousResponse] = userMessage_Dasha

		#Give random response from current mood
		Xchatlog.append("Dasha (Thinking): Gave random response.")	
		DashaPreviousResponse = botReply_Dasha(random.choice(list(messageDict_Dasha[currentMood_Dasha["mood"]].values())))
		break

print("\nEND OF CHAT\n")

print("Outputting chatlogs...")
#Output regular and extended chatlogs
chatlogOutput(chatlogFile["regular"], chatlog)
chatlogOutput(chatlogFile["extended"], Xchatlog)
print("Chatlog output complete.")
