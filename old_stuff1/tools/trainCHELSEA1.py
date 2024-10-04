#   chatbotCHELSEA, Training 1
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


##########################################################
# Input text file, tab separated message/response pairs, 
# each pair on own line
#
# A sample training file is provided with this tool, called
# 'questions_and_answers1.txt'
##########################################################

import re
import json

dictionary = {}
message_dict2 = {}
nEmotions = ["happy", "angry", "sad", "afraid"]
current_mood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
user_message = " "

def addToMood():
	#Add the emotional values of the user reply to CHELSEA's emotional values
	for emotion in nEmotions:
		current_mood[emotion] += reply_mood[emotion]

	#Change mood, pitch, and speaking speed according to CHELSEA's emotional values
	temp_dict = { 'happy': current_mood['happy'], 'angry': current_mood['angry'], 'sad': current_mood['sad'], 'afraid': current_mood['afraid'] }
	current_mood["mood"] = getMood2(temp_dict, True)
	current_mood["pitch"] = pitches[current_mood["mood"]]
	current_mood["speed"] = speeds[current_mood["mood"]]

def getReplyMood():
	#Get the mood of the user reply by looking at the emotion counts gathered on it
	temp_dict = { 'happy': reply_mood['happy'], 'angry': reply_mood['angry'], 'sad': reply_mood['sad'], 'afraid': reply_mood['afraid'] }
	reply_mood["mood"] = getMood2(temp_dict, True)

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

#Input memory
print("Inputting memory...")

with open("dictionary.json", 'r') as dictionary_file:
	dictionary = json.load(dictionary_file)
	
with open("messageDictionary2.json", 'r') as message_dictionary_file:
	message_dict2 = json.load(message_dictionary_file)
	
#Input qa training file as qa_pairs
print("Inputting dataset file")
qa_pairs = []
train_file = open('questions_and_answers1.txt', 'r')
for line in train_file.readlines():
	temp_pair = (line.strip()).split("\t")
	if (len(temp_pair[0]) > 100 or len(temp_pair[1]) > 100):
		continue 
	qa_pairs.append(temp_pair)
train_file.close()
print("Dataset file input complete.")	
			
print("Memory input complete!\n")

#Train loop
train_count = 0
train_max = len(qa_pairs)
for qa_pair in qa_pairs:

	train_count += 1
	print("Training line " + str(train_count) + "/" + str(train_max))
	CHELSEA_previous_response = qa_pair[0].lower() + '?' #Question of pair
	user_message = qa_pair[1].lower() #Answer of pair					
				
	#Filter certain chars from userMessage
	user_message = re.sub(r"([^a-z0-9, \"'\-\?!])", '', user_message)
	
	#Filter certain chars from CHELSEA_previous_response
	CHELSEA_previous_response = re.sub(r"([^a-z0-9, \"'\-\?!])", '', CHELSEA_previous_response)
	
	#Detect exclamation points at end of user_message to add emotional emphasis (Multiply counts by (exclaim_count + 1))
	exclaim_count = 1
	exclaim_match = re.search(r"(!+)$", user_message)
	if (exclaim_match):
		exclaim_count = len(exclaim_match.group(1)) + 1
	
	#Filter out punctuation from user message and split to list of words
	message_words = (re.sub(r"([^a-z0-9 '\-])", '', user_message)).split(" ")

	#Detect emotion words, get reply mood, add user reply emotional values to CHELSEA's emotional values
	unknown_words = []
	reply_mood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0}

	word_emotions = ""
	for word in message_words:
		if word == '':
			continue
		try:
			if (dictionary[word]['emotion'] != "permanent neutral" and dictionary[word]['emotion'] != "temp neutral"):
				reply_mood[dictionary[word]['emotion']] += (1 * exclaim_count)
				word_emotions = word_emotions + dictionary[word]['emotion'] + " "
			else: 
				word_emotions = word_emotions + " neutral "
		except(KeyError):
			unknown_words.append(word)
			word_emotions = word_emotions + " unknown "
		
	getReplyMood()
	addToMood()

	#Mark unknown words in the emotion dictionary according to the overall mood of the user reply
	if len(unknown_words) > 0:
		for word in unknown_words:
			dictionary[word] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 0, 'associated': {}}
			dictionary[word]['emotion'] = reply_mood["mood"] 
		
	#Add to counts for each word
	for word in message_words:
		try:
			if (dictionary[word]['emotion'] == 'permanent neutral' or dictionary[word]['emotion'] == 'temp neutral'):
				continue
		except(KeyError):
			continue
		dictionary[word][reply_mood["mood"]] += 1  * exclaim_count
		temp_dict = { 'happy': dictionary[word]['happy'], 'angry': dictionary[word]['angry'], 'sad': dictionary[word]['sad'], 'afraid': dictionary[word]['afraid'] }
		word_emotion = getMood2(temp_dict, False)
		if (word_emotion != dictionary[word]['emotion']):
			dictionary[word]['emotion'] = word_emotion
		
	#Mark associated words in list
	for word in message_words:
		try:
			if (dictionary[word]['emotion'] == 'permanent neutral' or dictionary[word]['emotion'] == 'temp neutral'):
				continue
		except(KeyError):
			continue
		for word2 in message_words:
			if (word == word2):
				continue
			try:
				if (dictionary[word2]['emotion'] == 'permanent neutral' or dictionary[word2]['emotion'] == 'temp neutral'):
					continue
			except(KeyError):
				continue
			try:
				dictionary[word]['associated'][word2] += 1
				continue
			except(KeyError):
				dictionary[word]['associated'][word2] = 1
				continue
			
	#No match, either overwrite old response or learn new one based on reply mood
	try:
		message_dict2[reply_mood["mood"]][CHELSEA_previous_response]
	except(KeyError):
		message_dict2[reply_mood["mood"]][CHELSEA_previous_response] = []
	message_dict2[reply_mood["mood"]][CHELSEA_previous_response].append(user_message)


#Output memory
print("\nOutputting memory...")

#Output word dictionary
with open("dictionary.json", 'w') as dictionary_file:
	json.dump(dictionary, dictionary_file)
	
#Output message/response dictionary
with open("messageDictionary2.json", 'w') as message_dictionary_file:
	json.dump(message_dict2, message_dictionary_file)

data_file = open("CHELSEAdata.txt", 'w')
data_file.write("Words in emotion dictionary: " + str(len(dictionary.keys())) + "\n")
message_count = 0
for emotion in nEmotions:
	message_count += len(message_dict2[emotion])
	data_file.write("Number of " + emotion + " message/response pairs: " + str(len(message_dict2[emotion])) + "\n")
data_file.write("Total message/response pairs: " + str(message_count))
data_file.close()

print("Memory output complete.\n")
