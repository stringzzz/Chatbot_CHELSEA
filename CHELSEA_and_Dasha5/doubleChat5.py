#   Setup for Chatbot CHELSEA to talk to a copy of herself named 'Dasha' (Version 2)
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
import json

nEmotions = ["happy", "angry", "sad", "afraid"]
chatlog = []
Xchatlog = []
chatlogFile = {"regular": "CHELSEA_and_Dasha2_chatlog.txt", "extended": "CHELSEA_and_Dasha2_Xchatlog.txt" }
user_emotions = { "happy": 0, "angry": 0, "sad": 0, "afraid": 0 }

dictionary = {}
dictionary_keys_list = ['happy', 'angry', 'sad', 'afraid', 'emotion', 'seen', 'associated']
message_dict2_CHELSEA = {"happy": {}, "angry": {}, "sad": {}, "afraid": {}}
current_mood_CHELSEA = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
pitches_CHELSEA = {"happy": 95, "angry": 80, "sad": 90, "afraid": 99}
speeds_CHELSEA = {"happy": 150, "angry": 155, "sad": 135, "afraid": 155}
user_message_CHELSEA = " "
topics = {}
CHELSEA_previous_response = ""
previous_pairs_CHELSEA = []

dictionary_Dasha = {}
message_dict2_Dasha = {"happy": {}, "angry": {}, "sad": {}, "afraid": {}}
current_mood_Dasha = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
pitches_Dasha = {"happy": 95, "angry": 80, "sad": 90, "afraid": 99}
speeds_Dasha = {"happy": 150, "angry": 155, "sad": 135, "afraid": 155}
user_message_Dasha = " "
topics_Dasha = {}
Dasha_previous_response = ""
previous_pairs_Dasha = []

def addToMood_Dasha():
	#Add the emotional values of the user reply to Dasha's emotional values
	for emotion in nEmotions:
		current_mood_Dasha[emotion] += reply_mood[emotion]

	#Change mood, pitch, and speaking speed according to Dasha's emotional values
	temp_dict = { 'happy': current_mood_Dasha['happy'], 'angry': current_mood_Dasha['angry'], 'sad': current_mood_Dasha['sad'], 'afraid': current_mood_Dasha['afraid'] }
	current_mood_Dasha["mood"] = getMood2(temp_dict, True)
	current_mood_Dasha["pitch"] = pitches_Dasha[current_mood_Dasha["mood"]]
	current_mood_Dasha["speed"] = speeds_Dasha[current_mood_Dasha["mood"]]
	Xchatlog.append("Dasha (Thinking): I feel " + current_mood_Dasha["mood"])

def getReplyMood_Dasha():
	#Get the mood of the user reply by looking at the emotion counts gathered on it
	temp_dict = { 'happy': reply_mood['happy'], 'angry': reply_mood['angry'], 'sad': reply_mood['sad'], 'afraid': reply_mood['afraid'] }
	reply_mood["mood"] = getMood2(temp_dict, True)
	Xchatlog.append("Dasha (Thinking): CHELSEA seems to be " + reply_mood["mood"])

def botReply_Dasha(botResponse):
	#Do the various parts of Dasha's response, text output, text-to-speech with espeak, chatlogs
	print("Dasha: " + botResponse)
	os.system("espeak -v en+f3 -p {} -s {} \" {} \"".format(str(current_mood_Dasha["pitch"]), str(current_mood_Dasha["speed"]), botResponse))
	chatlog.append("Dasha: " + botResponse)
	Xchatlog.append("Dasha: " + botResponse)
	return botResponse
		
def addToMood():
	#Add the emotional values of the user reply to CHELSEA's emotional values
	for emotion in nEmotions:
		current_mood_CHELSEA[emotion] += reply_mood[emotion]

	#Change mood, pitch, and speaking speed according to CHELSEA's emotional values
	temp_dict = { 'happy': current_mood_CHELSEA['happy'], 'angry': current_mood_CHELSEA['angry'], 'sad': current_mood_CHELSEA['sad'], 'afraid': current_mood_CHELSEA['afraid'] }
	current_mood_CHELSEA["mood"] = getMood2(temp_dict, True)
	current_mood_CHELSEA["pitch"] = pitches_CHELSEA[current_mood_CHELSEA["mood"]]
	current_mood_CHELSEA["speed"] = speeds_CHELSEA[current_mood_CHELSEA["mood"]]
	Xchatlog.append("CHELSEA (Thinking): I feel " + current_mood_CHELSEA["mood"])

def getReplyMood():
	#Get the mood of the user reply by looking at the emotion counts gathered on it
	temp_dict = { 'happy': reply_mood['happy'], 'angry': reply_mood['angry'], 'sad': reply_mood['sad'], 'afraid': reply_mood['afraid'] }
	reply_mood["mood"] = getMood2(temp_dict, True)
	Xchatlog.append("CHELSEA (Thinking): Dasha seems to be " + reply_mood["mood"])

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
	os.system("espeak -v en+f3 -p {} -s {} \" {} \"".format(str(current_mood_CHELSEA["pitch"]), str(current_mood_CHELSEA["speed"]), botResponse))
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
#Input dictionary_Dasha of message/response pairs
with open("dictionary_Dasha.json", 'r') as dictionary_file:
	dictionary_Dasha = json.load(dictionary_file)
	
with open("messageDictionary2_Dasha.json", 'r') as message_dictionary_file:
	message_dict2_Dasha = json.load(message_dictionary_file)

#Get counts for use in activating certain types of message detection
dictionary_count_Dasha = len(dictionary_Dasha.keys())
response_count_Dasha = 0
for emotion in nEmotions:
	response_count_Dasha += len(message_dict2_Dasha[emotion])
	
#Input dictionary of known words
#Input dictionary of message/response pairs
with open("dictionary_CHELSEA.json", 'r') as dictionary_file:
	dictionary = json.load(dictionary_file)
	
with open("messageDictionary2_CHELSEA.json", 'r') as message_dictionary_file:
	message_dict2_CHELSEA = json.load(message_dictionary_file)


#Get counts for use in activating certain types of message detection
dictionary_count = len(dictionary.keys())
response_count = 0
for emotion in nEmotions:
	response_count += len(message_dict2_CHELSEA[emotion])

print("Memory input complete!\n")

#Initial message
Dasha_previous_response = "hello"
botReply_Dasha("hello, CHELSEA")
user_message_CHELSEA = "hello"

#Chat loop
chatCount = 0

#Change to 100 after testing
while chatCount <= 120:

	chatCount += 1

	time.sleep(1)
	
	while(True):
	
		user_message_CHELSEA = Dasha_previous_response
		#Start CHELSEA code
		#Filter certain chars from userMessage
		user_message_CHELSEA = re.sub(r"([^a-z0-9, \"'\-\?!])", '', user_message_CHELSEA)
		
		#Detect exclamation points at end of user_message_CHELSEA to add emotional emphasis (Multiply counts by (exclaim_count + 1))
		exclaim_count = 1
		exclaim_match = re.search(r"(!+)$", user_message_CHELSEA)
		if (exclaim_match):
			Xchatlog.append("CHELSEA (Thinking): Exclamation detected, exclaim count: " + str(len(exclaim_match.group(1))))
			exclaim_count = len(exclaim_match.group(1)) + 1
		
		#Filter out punctuation from user message and split to list of words
		message_words = (re.sub(r"([^a-z0-9 '\-])", '', user_message_CHELSEA)).split(" ")

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
		Xchatlog.append("Word emotions in previous reply: " + word_emotions)
			
		getReplyMood()
		addToMood()

		#Mark unknown words in the emotion dictionary according to the overall mood of the user reply
		if len(unknown_words) > 0:
			Xchatlog.append("CHELSEA (Thinking): Unknown words detected: " + str(unknown_words))
			for word in unknown_words:
				dictionary[word] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 0, 'associated': {}}
				dictionary[word]['emotion'] = reply_mood["mood"] 
			Xchatlog.append("CHELSEA (Thinking): Learned unknown words as '" + reply_mood["mood"] + "' words.")
			
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
				Xchatlog.append("CHELSEA (Thinking): Switched emotion of word '" + word + "' to " + word_emotion)
			
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
					Xchatlog.append("CHELSEA (Thinking): Added to count of association of " + word + " and " + word2)
					continue
				except(KeyError):
					dictionary[word]['associated'][word2] = 1
					Xchatlog.append("CHELSEA (Thinking): Learned association of " + word + " and " + word2)
					continue
			
		#Get counts for words in current conversation				
		for word in message_words:
			try:
				if (dictionary[word]['emotion'] == 'permanent neutral' or dictionary[word]['emotion'] == 'temp neutral'):
					continue
			except(KeyError):
				continue
			try:
				topics[word] += (1 * exclaim_count)
			except(KeyError):
				topics[word] = (1 * exclaim_count)
		
		#Get current topics of the conversation by the highest counts
		if (not(len(topics.keys()) == 0)):
			temp_highest = max(topics.values())
			current_topics = [k for k, v in topics.items() if v == temp_highest]
			Xchatlog.append("CHELSEA (Thinking): Current topic(s) is/are " + " & ".join(current_topics))
		
		#Add to previous pairs
		temp_pair = []
		temp_pair.append(CHELSEA_previous_response)
		temp_pair.append(user_message_CHELSEA)
		previous_pairs_CHELSEA.append(temp_pair)
		if (len(previous_pairs_CHELSEA) > 3):
			del previous_pairs_CHELSEA[0]
		
		#Get depth words
		depth_words = []	
		if (len(previous_pairs_CHELSEA) == 3):
			temp_depth_words = {}		
			for pair in previous_pairs_CHELSEA:
				temp_messages = (re.sub(r"([^a-z0-9 '\-])", '', pair[0])).split(" ")
				temp_responses = (re.sub(r"([^a-z0-9 '\-])", '', pair[1])).split(" ")
				for word1 in temp_messages:
					try:
						if (dictionary[word1]['emotion'] == "permanent neutral" or dictionary[word1]['emotion'] == "temp neutral"):
							continue
					except(KeyError):
						continue
					for word2 in temp_responses:
						try:
							if (dictionary[word2]['emotion'] == "permanent neutral" or dictionary[word2]['emotion'] == "temp neutral"):
								continue
						except(KeyError):
							continue
						if (word1 == word2):
							temp_depth_words[word1] = 1
			depth_words = list(temp_depth_words.keys())
			if (len(depth_words) > 0):
				Xchatlog.append("CHELSEA (Thinking): Found depth words: " + " ".join(depth_words))
		
		#Check for possible matching answer to What Question in both keys and values under current mood
		response_made = False
		whq_match_object = re.search(r"what (is|are) ([a-z '\-]+)\?*$", user_message_CHELSEA)

		temp_message_keys = list(message_dict2_CHELSEA[current_mood_CHELSEA["mood"]].keys())
		random.shuffle(temp_message_keys) #Note, this shuffled list is potentially re-used in other parts of the script
		
		if (whq_match_object):
			temp_message_values = list(message_dict2_CHELSEA[current_mood_CHELSEA["mood"]].values())
			random.shuffle(temp_message_values)
			partial_message = whq_match_object.group(2) + ' ' + whq_match_object.group(1)
			
			#Check values
			for message in temp_message_values:
				message = random.choice(message)
				if (message == CHELSEA_previous_response):
					continue
				if message.find(partial_message) != -1:
					Xchatlog.append("CHELSEA (Thinking): WH-Q question match found in values.")
					CHELSEA_previous_response = botReply(message)
					response_made = True
					break
			if response_made:
				break
			#Check keys
			for message in temp_message_keys:
				if (message == CHELSEA_previous_response):
					continue
				if message.find(partial_message) != -1:
					Xchatlog.append("CHELSEA (Thinking): WH-Q question match found in keys.")
					CHELSEA_previous_response = botReply(message)
					response_made = True
					break
			if response_made:
				break
		
		#Check for question about previous message meaning
		meaning_match = re.search(r"(what (do you|does that) mean|(can you|(do you|can you) care to) clarify|I('m| am) confused|I do( not|n't) (understand|get( it)?)( what you mean| what (that|this) means)?|why (do|did) you (say|think) (that|this))\?*$", user_message_CHELSEA)
		if (meaning_match):
			previous_words = (re.sub(r"([^a-z0-9 '\-])", '', CHELSEA_previous_response)).split(" ")
			random.shuffle(previous_words)
			for message in temp_message_keys:
				if (message == CHELSEA_previous_response):
					continue
				match_count = 0
				match_words = []
				for word in previous_words:
					try:
						if (dictionary[word]['emotion'] == "temp neutral" or dictionary[word]['emotion'] == "permanent neutral"):
							continue
					except(KeyError):
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
						CHELSEA_previous_response = botReply(message)
						response_made = True
						break
				if response_made:
					break
			if response_made:
				break
				
		#Ask what CHELSEA feels about ___
		feel_about_match = re.search(r"(?:how|what) do you (?:feel|think) (?:about|toward(?:s)?) ([a-z0-9, '\-]+)\?*$", user_message_CHELSEA)
		if (feel_about_match):
			feel_words = (re.sub(r"([^a-z0-9 '\-])", '', feel_about_match.group(1))).split(" ")
			temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in feel_words:
				try:
					if (dictionary[word]['emotion'] == 'temp neutral' or dictionary[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
					continue
				temp_dict[dictionary[word]['emotion']] += 1
			feel_emotion = getMood2(temp_dict, False)
			if (feel_emotion == 'temp neutral'):
				Xchatlog.append("CHELSEA (Thinking): Feel nothing.")
				CHELSEA_previous_response = botReply("i feel nothing about " + feel_about_match.group(1))
				response_made = True
				break
			else:
				Xchatlog.append("CHELSEA (Thinking): Have emotion to answer question.")
				CHELSEA_previous_response = botReply("i feel " + feel_emotion + ' about ' + feel_about_match.group(1))
				response_made = True
				break
				
		#Ask do you like question
		like_match = re.search(r"^do you (like|love|enjoy|adore|appreciate|dislike|hate|loathe|detest|despise) ([a-z0-9, '\-]+)\?*$", user_message_CHELSEA)
		if (like_match):
			like_terms = ['like', 'love', 'enjoy', 'adore', 'appreciate']
			dislike_terms = ['dislike', 'hate', 'loathe', 'detest', 'despise']
			like_words = (re.sub(r"([^a-z0-9 '\-])", '', like_match.group(2))).split(" ")
			temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in like_words:
				try:
					if (dictionary[word]['emotion'] == 'temp neutral' or dictionary[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
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
					CHELSEA_previous_response = botReply("yes, i " + like_match.group(1) + ' ' + like_match.group(2))
				elif ((like_emotion == 'happy' and like_dislike == 'dislike') or (like_emotion != 'happy' and like_dislike == 'like')):
					CHELSEA_previous_response = botReply("no, i don't " + like_match.group(1) + ' ' + like_match.group(2))
				response_made = True
				break
			else:
				Xchatlog.append("CHELSEA (Thinking): Neither like or dislike")
				CHELSEA_previous_response = botReply("i don't feel anything about " + like_match.group(2))
				response_made = True
				break
				
		#Ask which is better, 1 or 2?
		better_match = re.search(r"(?:which|what) (?:is (?:better,? ?|best,? ?)|do you (?:like (?:better,? ?|best,? ?|more,? ?))) ([a-z0-9, '\-]+) or ([a-z0-9, '\-]+)\?*$", user_message_CHELSEA)
		if (better_match):
			better_words1 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(1))).split(" ")
			temp_dict1 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in better_words1:
				try:
					if (dictionary[word]['emotion'] == 'temp neutral' or dictionary[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
					continue
				temp_dict1[dictionary[word]['emotion']] += 1
			better_emotion1 = getMood2(temp_dict1, False)

			better_words2 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(2))).split(" ")
			temp_dict2 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in better_words2:
				try:
					if (dictionary[word]['emotion'] == 'temp neutral' or dictionary[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
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
					CHELSEA_previous_response = botReply("i like both, but " + better_match.group(1) + ' most')
					response_made = True
					break
				elif (happy_count2 > happy_count1):
					Xchatlog.append("CHELSEA (Thinking): Determined I like second option better.")
					CHELSEA_previous_response = botReply("i like both, but " + better_match.group(2) + ' most')
					response_made = True
					break
				else:	
					Xchatlog.append("CHELSEA (Thinking): Determined I like both equally.")
					CHELSEA_previous_response = botReply("i like both " + better_match.group(1) + ' & ' + better_match.group(2) + ' the same')
					response_made = True
					break
			elif (better_emotion1 == 'happy' and better_emotion2 != 'happy'):
				Xchatlog.append("CHELSEA (Thinking): Found like first.")
				CHELSEA_previous_response = botReply("i like " + better_match.group(1) + ' better ')
				response_made = True
				break
			elif (better_emotion1 != 'happy' and better_emotion2 == 'happy'):
				Xchatlog.append("CHELSEA (Thinking): Found like second.")
				CHELSEA_previous_response = botReply("i like " + better_match.group(2) + ' better ')
				response_made = True
				break
			elif (better_emotion1 != 'happy' and better_emotion2 != 'happy'):
				Xchatlog.append("CHELSEA (Thinking): Like neither.")
				CHELSEA_previous_response = botReply("i don't prefer either " + better_match.group(1) + ' or ' + better_match.group(2))
				response_made = True
				break
				
		#Check for 'why is' question match
		whyis_match = re.search(r"why (?:is|are) ([a-z0-9, '\-]+)\?*$", user_message_CHELSEA)
		if (whyis_match):
			whyis_words = (re.sub(r"([^a-z0-9 '\-])", '', whyis_match.group(1))).split(" ")
			temp_message_values = list(message_dict2_CHELSEA[current_mood_CHELSEA["mood"]].values())
			random.shuffle(temp_message_values)

			#Check values
			for message in temp_message_values:
				message = random.choice(message)
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
							CHELSEA_previous_response = botReply(message)
							response_made = True
							break
					if response_made:
						break
			if response_made:
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
							CHELSEA_previous_response = botReply(message)
							response_made = True
							break
					if response_made:
						break
			if response_made:
				break
		
		#Ask 'most' question		
		max1 = []
		temp_emotion = ''
		happy_words = ['happy', 'contented', 'content', 'cheerful', 'cheery', 'merry', 'joyful', 'jovial', 'jolly', 'gleeful', 'delighted', 'joyous', 'thrilled', 'exuberant', 'elated', 'exhilarated', 'ecstatic', 'blissful', 'overjoyed']
		m1 = re.search(re.compile("what makes you most (" + "|".join(happy_words) + ")\?*$"), user_message_CHELSEA)
		if (m1):
			max1 = getMost(dictionary, 'happy')
			temp_emotion = 'happy'
			
		angry_words = ['angry', 'frustrated', 'irate', 'vexed', 'irritated', 'exasperated', 'indignant', 'aggrieved', 'irked', 'piqued', 'displeased', 'provoked', 'galled', 'resentful', 'furious', 'enraged', 'infuriated', 'raging', 'incandescent', 'wrathful', 'fuming', 'ranting', 'raving', 'seething', 'frenzied', 'beside oneself', 'outraged', 'choleric', 'crabby', 'waspish', 'hostile', 'antagonistic', 'mad', 'livid', 'boiling', 'riled', 'aggravated', 'sore', 'ticked off', 'ill-tempered', 'acrimonious']
		m1 = re.search(re.compile("what makes you most (" + "|".join(angry_words) + ")\?*$"), user_message_CHELSEA)
		if (m1):
			max1 = getMost(dictionary, 'angry')
			temp_emotion = 'angry'
		sad_words = ['sad', 'unhappy', 'sorrowful', 'depressed', 'downcast', 'miserable', 'glum', 'gloomy', 'dismal', 'blue', 'melancholy']
		m1 = re.search(re.compile("what makes you most (" + "|".join(sad_words) + ")\?*$"), user_message_CHELSEA)
		if (m1):
			max1 = getMost(dictionary, 'sad')
			temp_emotion = 'sad'
		afraid_words = ['afraid', 'frightened', 'scared', 'terrified', 'fearful', 'petrified', 'nervous', 'worried', 'panicky', 'timid', 'spooked']
		m1 = re.search(re.compile("what makes you most (" + "|".join(afraid_words) + ")\?*$"), user_message_CHELSEA)
		if (m1):
			max1 = getMost(dictionary, 'afraid')
			temp_emotion = 'afraid'	
		
		#'most' question continued: Get max(es) for emotional words, respond accordingly	
		if (len(max1) == 1):	
			Xchatlog.append("CHELSEA (Thinking): Most " + temp_emotion + " match found.")
			CHELSEA_previous_response = botReply(max1[0] + " makes me most " + temp_emotion)
			response_made = True
			break
		elif (len(max1) > 1):
			Xchatlog.append("CHELSEA (Thinking): Most " + temp_emotion + " matches found.")
			CHELSEA_previous_response = botReply(random.choice(max1) + " is one of many that makes me most " + temp_emotion)
			response_made = True
			break
		
		#Check for exact match under current mood
		try:
			message_dict2_CHELSEA[current_mood_CHELSEA["mood"]][user_message_CHELSEA]
			Xchatlog.append("CHELSEA (Thinking): Exact message match found.")
			CHELSEA_previous_response = botReply(random.choice(message_dict2_CHELSEA[current_mood_CHELSEA["mood"]][user_message_CHELSEA]))
			break
		except(KeyError):
			pass #Exact match not found in message dictionary
				
		#Check for partial match under current mood
		for message in temp_message_keys:
			if message.find(user_message_CHELSEA) != -1:
				Xchatlog.append("CHELSEA (Thinking): Partial message match found.")
				CHELSEA_previous_response = botReply(random.choice(message_dict2_CHELSEA[current_mood_CHELSEA["mood"]][message]))
				response_made = True
				break
		if response_made:
			break
			
		#Check for match with current topic or depth match (Coin flip)
		if ((not(len(topics.keys()) == 0) and (dictionary_count >= 2500 and response_count >= 1200 and random.randint(1, 3) == 1)) or (not(len(topics.keys()) == 0) and (dictionary_count >= 600 and dictionary_count < 2500 and response_count >= 350 and response_count < 1200 and random.randint(1, 4) == 1))):
			if (len(depth_words) >= 2 and random.randint(1, 2) == 1):
				#Depth match
				for message in temp_message_keys:
					depth_found = 0
					two_matched = False
					matched_words = []
					random.shuffle(depth_words)
					for word in depth_words:
						if message.find(word) != -1:
							depth_found += 1
							matched_words.append(word)
						if (depth_found == 2):
							two_matched = True
							break
					if (not(two_matched)):
						continue
					else:
						Xchatlog.append("CHELSEA (Thinking): Depth match found for: " + " ".join(matched_words))
						CHELSEA_previous_response = botReply(message)
						response_made = True
						break
				if response_made:
					break
			else:	
				#Topic match
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
						CHELSEA_previous_response = botReply(random.choice(message_dict2_CHELSEA[current_mood_CHELSEA["mood"]][message]))
						response_made = True
						break
				if response_made:
					break
			
		#Check for single term match under current mood, ignore neutral words
		#Only activated when she has learned enough, though this can easily be adjusted
		if ((dictionary_count >= 4500 and response_count >= 2700 and random.randint(1, 3) == 1) or (dictionary_count >= 2000 and dictionary_count < 4500 and response_count >= 500 and response_count < 2700 and random.randint(1, 4) == 1)):
			response_made = False
			#Coin flip
			if (random.randint(1, 2) == 1):
				#single term match from user message words
				for word in message_words:
					try:
						if (dictionary[word]['emotion'] == "temp neutral" or dictionary[word]['emotion'] == "permanent neutral"):
							continue
						else:
							for message in temp_message_keys:
								if message.find(word) != -1:
									Xchatlog.append("CHELSEA (Thinking): Single term match found for term: " + word)
									CHELSEA_previous_response = botReply(random.choice(message_dict2_CHELSEA[current_mood_CHELSEA["mood"]][message]))
									response_made = True
									break
							if response_made:
								break
					except(KeyError):
						continue
				if response_made:
					break
			else:
				#Single term match for a word associated with highest association count from user message word
				for word in message_words:
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
					try:
						if (dictionary[highest_associated_chosen]['emotion'] == "temp neutral" or dictionary[highest_associated_chosen]['emotion'] == "permanent neutral"):
							continue
					except(KeyError):
						continue		
					for message in temp_message_keys:
						if message.find(highest_associated_chosen) != -1:
							Xchatlog.append("CHELSEA (Thinking): Single term associated match found for associated term: " + highest_associated_chosen)
							CHELSEA_previous_response = botReply(random.choice(message_dict2_CHELSEA[current_mood_CHELSEA["mood"]][message]))
							response_made = True
							break
					if response_made:
						break
				if response_made:
					break
					 	
				
		#No match, either add to list of responses or learn new one based on reply mood
		Xchatlog.append("CHELSEA (Thinking): Message not recognized.")
		try:
			message_dict2_CHELSEA[reply_mood["mood"]][CHELSEA_previous_response]
		except(KeyError):
			Xchatlog.append("CHELSEA (Thinking): Learned new '" + reply_mood["mood"] + "' response.")
			message_dict2_CHELSEA[reply_mood["mood"]][CHELSEA_previous_response] = []
		duplicate_found = False
		for response in message_dict2_CHELSEA[reply_mood["mood"]][CHELSEA_previous_response]:
			if (response == user_message_CHELSEA):
				duplicate_found = True
				break
		if (not(duplicate_found)):
			Xchatlog.append("CHELSEA (Thinking): Added to '" + reply_mood["mood"] + "' responses.")
			message_dict2_CHELSEA[reply_mood["mood"]][CHELSEA_previous_response].append(user_message_CHELSEA)

		#Give random response from current mood
		Xchatlog.append("CHELSEA (Thinking): Gave random response.")	
		CHELSEA_previous_response = botReply(random.choice(random.choice(list(message_dict2_CHELSEA[current_mood_CHELSEA["mood"]].values()))))
		break
			
	time.sleep(1)

	while(True):
		Xchatlog.append("\n\n")
		
		user_message_Dasha = CHELSEA_previous_response
	
		#Start Dasha code
		#Filter certain chars from userMessage
		user_message_Dasha = re.sub(r"([^a-z0-9, \"'\-\?!])", '', user_message_Dasha)
		
		#Detect exclamation points at end of user_message_Dasha to add emotional emphasis (Multiply counts by (exclaim_count + 1))
		exclaim_count = 1
		exclaim_match = re.search(r"(!+)$", user_message_Dasha)
		if (exclaim_match):
			Xchatlog.append("Dasha (Thinking): Exclamation detected, exclaim count: " + str(len(exclaim_match.group(1))))
			exclaim_count = len(exclaim_match.group(1)) + 1
		
		#Filter out punctuation from user message and split to list of words
		message_words = (re.sub(r"([^a-z0-9 '\-])", '', user_message_Dasha)).split(" ")

		#Detect emotion words, get reply mood, add user reply emotional values to Dasha's emotional values
		unknown_words = []
		reply_mood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0}

		word_emotions = ""
		for word in message_words:
			if word == '':
				continue
			try:
				if (dictionary_Dasha[word]['emotion'] != "permanent neutral" and dictionary_Dasha[word]['emotion'] != "temp neutral"):
					reply_mood[dictionary_Dasha[word]['emotion']] += (1 * exclaim_count)
					word_emotions = word_emotions + dictionary_Dasha[word]['emotion'] + " "
				else: 
					word_emotions = word_emotions + " neutral "
			except(KeyError):
				unknown_words.append(word)
				word_emotions = word_emotions + " unknown "
		Xchatlog.append("Word emotions in previous reply: " + word_emotions)
			
		getReplyMood_Dasha()
		addToMood_Dasha()

		#Mark unknown words in the emotion dictionary_Dasha according to the overall mood of the user reply
		if len(unknown_words) > 0:
			Xchatlog.append("Dasha (Thinking): Unknown words detected: " + str(unknown_words))
			for word in unknown_words:
				dictionary_Dasha[word] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 0, 'associated': {}}
				dictionary_Dasha[word]['emotion'] = reply_mood["mood"] 
			Xchatlog.append("Dasha (Thinking): Learned unknown words as '" + reply_mood["mood"] + "' words.")
			
		#Add to counts for each word
		for word in message_words:
			try:
				if (dictionary_Dasha[word]['emotion'] == 'permanent neutral' or dictionary_Dasha[word]['emotion'] == 'temp neutral'):
					continue
			except(KeyError):
				continue
			dictionary_Dasha[word][reply_mood["mood"]] += 1  * exclaim_count
			temp_dict = { 'happy': dictionary_Dasha[word]['happy'], 'angry': dictionary_Dasha[word]['angry'], 'sad': dictionary_Dasha[word]['sad'], 'afraid': dictionary_Dasha[word]['afraid'] }
			word_emotion = getMood2(temp_dict, False)
			if (word_emotion != dictionary_Dasha[word]['emotion']):
				dictionary_Dasha[word]['emotion'] = word_emotion
				Xchatlog.append("Dasha (Thinking): Switched emotion of word '" + word + "' to " + word_emotion)
			
		#Mark associated words in list
		for word in message_words:
			try:
				if (dictionary_Dasha[word]['emotion'] == 'permanent neutral' or dictionary_Dasha[word]['emotion'] == 'temp neutral'):
					continue
			except(KeyError):
				continue
			for word2 in message_words:
				if (word == word2):
					continue
				try:
					if (dictionary_Dasha[word2]['emotion'] == 'permanent neutral' or dictionary_Dasha[word2]['emotion'] == 'temp neutral'):
						continue
				except(KeyError):
					continue
				try:
					dictionary_Dasha[word]['associated'][word2] += 1
					Xchatlog.append("Dasha (Thinking): Added to count of association of " + word + " and " + word2)
					continue
				except(KeyError):
					dictionary_Dasha[word]['associated'][word2] = 1
					Xchatlog.append("Dasha (Thinking): Learned association of " + word + " and " + word2)
					continue
			
		#Get counts for words in current conversation				
		for word in message_words:
			try:
				if (dictionary_Dasha[word]['emotion'] == 'permanent neutral' or dictionary_Dasha[word]['emotion'] == 'temp neutral'):
					continue
			except(KeyError):
				continue
			try:
				topics_Dasha[word] += (1 * exclaim_count)
			except(KeyError):
				topics_Dasha[word] = (1 * exclaim_count)
		
		#Get current topics_Dasha of the conversation by the highest counts
		if (not(len(topics_Dasha.keys()) == 0)):
			temp_highest = max(topics_Dasha.values())
			current_topics_Dasha = [k for k, v in topics_Dasha.items() if v == temp_highest]
			Xchatlog.append("Dasha (Thinking): Current topic(s) is/are " + " & ".join(current_topics_Dasha))
		
		#Add to previous pairs
		temp_pair = []
		temp_pair.append(Dasha_previous_response)
		temp_pair.append(user_message_Dasha)
		previous_pairs_Dasha.append(temp_pair)
		if (len(previous_pairs_Dasha) > 3):
			del previous_pairs_Dasha[0]
		
		#Get depth words
		depth_words = []	
		if (len(previous_pairs_Dasha) == 3):
			temp_depth_words = {}		
			for pair in previous_pairs_Dasha:
				temp_messages = (re.sub(r"([^a-z0-9 '\-])", '', pair[0])).split(" ")
				temp_responses = (re.sub(r"([^a-z0-9 '\-])", '', pair[1])).split(" ")
				for word1 in temp_messages:
					if (dictionary_Dasha[word1]['emotion'] == "permanent neutral" or dictionary_Dasha[word1]['emotion'] == "temp neutral"):
						continue
					for word2 in temp_responses:
						if (dictionary_Dasha[word2]['emotion'] == "permanent neutral" or dictionary_Dasha[word2]['emotion'] == "temp neutral"):
							continue
						if (word1 == word2):
							temp_depth_words[word1] = 1
			depth_words = list(temp_depth_words.keys())
			if (len(depth_words) > 0):
				Xchatlog.append("Dasha (Thinking): Found depth words: " + " ".join(depth_words))
		
		#Check for possible matching answer to What Question in both keys and values under current mood
		response_made = False
		whq_match_object = re.search(r"what (is|are) ([a-z '\-]+)\?*$", user_message_Dasha)

		temp_message_keys = list(message_dict2_Dasha[current_mood_Dasha["mood"]].keys())
		random.shuffle(temp_message_keys) #Note, this shuffled list is potentially re-used in other parts of the script
		
		if (whq_match_object):
			temp_message_values = list(message_dict2_Dasha[current_mood_Dasha["mood"]].values())
			random.shuffle(temp_message_values)
			partial_message = whq_match_object.group(2) + ' ' + whq_match_object.group(1)
			
			#Check values
			for message in temp_message_values:
				message = random.choice(message)
				if (message == Dasha_previous_response):
					continue
				if message.find(partial_message) != -1:
					Xchatlog.append("Dasha (Thinking): WH-Q question match found in values.")
					Dasha_previous_response = botReply_Dasha(message)
					response_made = True
					break
			if response_made:
				break
			#Check keys
			for message in temp_message_keys:
				if (message == Dasha_previous_response):
					continue
				if message.find(partial_message) != -1:
					Xchatlog.append("Dasha (Thinking): WH-Q question match found in keys.")
					Dasha_previous_response = botReply_Dasha(message)
					response_made = True
					break
			if response_made:
				break
		
		#Check for question about previous message meaning
		meaning_match = re.search(r"(what (do you|does that) mean|(can you|(do you|can you) care to) clarify|I('m| am) confused|I do( not|n't) (understand|get( it)?)( what you mean| what (that|this) means)?|why (do|did) you (say|think) (that|this))\?*$", user_message_Dasha)
		if (meaning_match):
			previous_words = (re.sub(r"([^a-z0-9 '\-])", '', Dasha_previous_response)).split(" ")
			random.shuffle(previous_words)
			for message in temp_message_keys:
				if (message == Dasha_previous_response):
					continue
				match_count = 0
				match_words = []
				for word in previous_words:
					try:
						if (dictionary_Dasha[word]['emotion'] == "temp neutral" or dictionary_Dasha[word]['emotion'] == "permanent neutral"):
							continue
					except(KeyError):
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
						Dasha_previous_response = botReply_Dasha(message)
						response_made = True
						break
				if response_made:
					break
			if response_made:
				break
				
		#Ask what Dasha feels about ___
		feel_about_match = re.search(r"(?:how|what) do you (?:feel|think) (?:about|toward(?:s)?) ([a-z0-9, '\-]+)\?*$", user_message_Dasha)
		if (feel_about_match):
			feel_words = (re.sub(r"([^a-z0-9 '\-])", '', feel_about_match.group(1))).split(" ")
			temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in feel_words:
				try:
					if (dictionary_Dasha[word]['emotion'] == 'temp neutral' or dictionary_Dasha[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
					continue
				temp_dict[dictionary_Dasha[word]['emotion']] += 1
			feel_emotion = getMood2(temp_dict, False)
			if (feel_emotion == 'temp neutral'):
				Xchatlog.append("Dasha (Thinking): Feel nothing.")
				Dasha_previous_response = botReply_Dasha("i feel nothing about " + feel_about_match.group(1))
				response_made = True
				break
			else:
				Xchatlog.append("Dasha (Thinking): Have emotion to answer question.")
				Dasha_previous_response = botReply_Dasha("i feel " + feel_emotion + ' about ' + feel_about_match.group(1))
				response_made = True
				break
				
		#Ask do you like question
		like_match = re.search(r"^do you (like|love|enjoy|adore|appreciate|dislike|hate|loathe|detest|despise) ([a-z0-9, '\-]+)\?*$", user_message_Dasha)
		if (like_match):
			like_terms = ['like', 'love', 'enjoy', 'adore', 'appreciate']
			dislike_terms = ['dislike', 'hate', 'loathe', 'detest', 'despise']
			like_words = (re.sub(r"([^a-z0-9 '\-])", '', like_match.group(2))).split(" ")
			temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in like_words:
				try:
					if (dictionary_Dasha[word]['emotion'] == 'temp neutral' or dictionary_Dasha[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
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
					Dasha_previous_response = botReply_Dasha("yes, i " + like_match.group(1) + ' ' + like_match.group(2))
				elif ((like_emotion == 'happy' and like_dislike == 'dislike') or (like_emotion != 'happy' and like_dislike == 'like')):
					Dasha_previous_response = botReply_Dasha("no, i don't " + like_match.group(1) + ' ' + like_match.group(2))
				response_made = True
				break
			else:
				Xchatlog.append("Dasha (Thinking): Neither like or dislike")
				Dasha_previous_response = botReply_Dasha("i don't feel anything about " + like_match.group(2))
				response_made = True
				break
				
		#Ask which is better, 1 or 2?
		better_match = re.search(r"(?:which|what) (?:is (?:better,? ?|best,? ?)|do you (?:like (?:better,? ?|best,? ?|more,? ?))) ([a-z0-9, '\-]+) or ([a-z0-9, '\-]+)\?*$", user_message_Dasha)
		if (better_match):
			better_words1 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(1))).split(" ")
			temp_dict1 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in better_words1:
				try:
					if (dictionary_Dasha[word]['emotion'] == 'temp neutral' or dictionary_Dasha[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
					continue
				temp_dict1[dictionary_Dasha[word]['emotion']] += 1
			better_emotion1 = getMood2(temp_dict1, False)

			better_words2 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(2))).split(" ")
			temp_dict2 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in better_words2:
				try:
					if (dictionary_Dasha[word]['emotion'] == 'temp neutral' or dictionary_Dasha[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
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
					Dasha_previous_response = botReply_Dasha("i like both, but " + better_match.group(1) + ' most')
					response_made = True
					break
				elif (happy_count2 > happy_count1):
					Xchatlog.append("Dasha (Thinking): Determined I like second option better.")
					Dasha_previous_response = botReply_Dasha("i like both, but " + better_match.group(2) + ' most')
					response_made = True
					break
				else:	
					Xchatlog.append("Dasha (Thinking): Determined I like both equally.")
					Dasha_previous_response = botReply_Dasha("i like both " + better_match.group(1) + ' & ' + better_match.group(2) + ' the same')
					response_made = True
					break
			elif (better_emotion1 == 'happy' and better_emotion2 != 'happy'):
				Xchatlog.append("Dasha (Thinking): Found like first.")
				Dasha_previous_response = botReply_Dasha("i like " + better_match.group(1) + ' better ')
				response_made = True
				break
			elif (better_emotion1 != 'happy' and better_emotion2 == 'happy'):
				Xchatlog.append("Dasha (Thinking): Found like second.")
				Dasha_previous_response = botReply_Dasha("i like " + better_match.group(2) + ' better ')
				response_made = True
				break
			elif (better_emotion1 != 'happy' and better_emotion2 != 'happy'):
				Xchatlog.append("Dasha (Thinking): Like neither.")
				Dasha_previous_response = botReply_Dasha("i don't prefer either " + better_match.group(1) + ' or ' + better_match.group(2))
				response_made = True
				break
				
		#Check for 'why is' question match
		whyis_match = re.search(r"why (?:is|are) ([a-z0-9, '\-]+)\?*$", user_message_Dasha)
		if (whyis_match):
			whyis_words = (re.sub(r"([^a-z0-9 '\-])", '', whyis_match.group(1))).split(" ")
			temp_message_values = list(message_dict2_Dasha[current_mood_Dasha["mood"]].values())
			random.shuffle(temp_message_values)

			#Check values
			for message in temp_message_values:
				message = random.choice(message)
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
							Dasha_previous_response = botReply_Dasha(message)
							response_made = True
							break
					if response_made:
						break
			if response_made:
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
							Dasha_previous_response = botReply_Dasha(message)
							response_made = True
							break
					if response_made:
						break
			if response_made:
				break
		
		#Ask 'most' question		
		max1 = []
		temp_emotion = ''
		happy_words = ['happy', 'contented', 'content', 'cheerful', 'cheery', 'merry', 'joyful', 'jovial', 'jolly', 'gleeful', 'delighted', 'joyous', 'thrilled', 'exuberant', 'elated', 'exhilarated', 'ecstatic', 'blissful', 'overjoyed']
		m1 = re.search(re.compile("what makes you most (" + "|".join(happy_words) + ")\?*$"), user_message_Dasha)
		if (m1):
			max1 = getMost(dictionary_Dasha, 'happy')
			temp_emotion = 'happy'
			
		angry_words = ['angry', 'frustrated', 'irate', 'vexed', 'irritated', 'exasperated', 'indignant', 'aggrieved', 'irked', 'piqued', 'displeased', 'provoked', 'galled', 'resentful', 'furious', 'enraged', 'infuriated', 'raging', 'incandescent', 'wrathful', 'fuming', 'ranting', 'raving', 'seething', 'frenzied', 'beside oneself', 'outraged', 'choleric', 'crabby', 'waspish', 'hostile', 'antagonistic', 'mad', 'livid', 'boiling', 'riled', 'aggravated', 'sore', 'ticked off', 'ill-tempered', 'acrimonious']
		m1 = re.search(re.compile("what makes you most (" + "|".join(angry_words) + ")\?*$"), user_message_Dasha)
		if (m1):
			max1 = getMost(dictionary_Dasha, 'angry')
			temp_emotion = 'angry'
		sad_words = ['sad', 'unhappy', 'sorrowful', 'depressed', 'downcast', 'miserable', 'glum', 'gloomy', 'dismal', 'blue', 'melancholy']
		m1 = re.search(re.compile("what makes you most (" + "|".join(sad_words) + ")\?*$"), user_message_Dasha)
		if (m1):
			max1 = getMost(dictionary_Dasha, 'sad')
			temp_emotion = 'sad'
		afraid_words = ['afraid', 'frightened', 'scared', 'terrified', 'fearful', 'petrified', 'nervous', 'worried', 'panicky', 'timid', 'spooked']
		m1 = re.search(re.compile("what makes you most (" + "|".join(afraid_words) + ")\?*$"), user_message_Dasha)
		if (m1):
			max1 = getMost(dictionary_Dasha, 'afraid')
			temp_emotion = 'afraid'	
		
		#'most' question continued: Get max(es) for emotional words, respond accordingly	
		if (len(max1) == 1):	
			Xchatlog.append("Dasha (Thinking): Most " + temp_emotion + " match found.")
			Dasha_previous_response = botReply_Dasha(max1[0] + " makes me most " + temp_emotion)
			response_made = True
			break
		elif (len(max1) > 1):
			Xchatlog.append("Dasha (Thinking): Most " + temp_emotion + " matches found.")
			Dasha_previous_response = botReply_Dasha(random.choice(max1) + " is one of many that makes me most " + temp_emotion)
			response_made = True
			break
		
		#Check for exact match under current mood
		try:
			message_dict2_Dasha[current_mood_Dasha["mood"]][user_message_Dasha]
			Xchatlog.append("Dasha (Thinking): Exact message match found.")
			Dasha_previous_response = botReply_Dasha(random.choice(message_dict2_Dasha[current_mood_Dasha["mood"]][user_message_Dasha]))
			break
		except(KeyError):
			pass #Exact match not found in message dictionary_Dasha
				
		#Check for partial match under current mood
		for message in temp_message_keys:
			if message.find(user_message_Dasha) != -1:
				Xchatlog.append("Dasha (Thinking): Partial message match found.")
				Dasha_previous_response = botReply_Dasha(random.choice(message_dict2_Dasha[current_mood_Dasha["mood"]][message]))
				response_made = True
				break
		if response_made:
			break
			
		#Check for match with current topic or depth match (Coin flip)
		if ((not(len(topics_Dasha.keys()) == 0) and (dictionary_count_Dasha >= 2500 and response_count_Dasha >= 1200 and random.randint(1, 3) == 1)) or (not(len(topics_Dasha.keys()) == 0) and (dictionary_count_Dasha >= 600 and dictionary_count_Dasha < 2500 and response_count_Dasha >= 350 and response_count_Dasha < 1200 and random.randint(1, 4) == 1))):
			if (len(depth_words) >= 2 and random.randint(1, 2) == 1):
				#Depth match
				for message in temp_message_keys:
					depth_found = 0
					two_matched = False
					matched_words = []
					random.shuffle(depth_words)
					for word in depth_words:
						if message.find(word) != -1:
							depth_found += 1
							matched_words.append(word)
						if (depth_found == 2):
							two_matched = True
							break
					if (not(two_matched)):
						continue
					else:
						Xchatlog.append("Dasha (Thinking): Depth match found for: " + " ".join(matched_words))
						Dasha_previous_response = botReply_Dasha(message)
						response_made = True
						break
				if response_made:
					break
			else:	
				#Topic match
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
						Dasha_previous_response = botReply_Dasha(random.choice(message_dict2_Dasha[current_mood_Dasha["mood"]][message]))
						response_made = True
						break
				if response_made:
					break
			
		#Check for single term match under current mood, ignore neutral words
		#Only activated when she has learned enough, though this can easily be adjusted
		if ((dictionary_count_Dasha >= 4500 and response_count_Dasha >= 2700 and random.randint(1, 3) == 1) or (dictionary_count_Dasha >= 2000 and dictionary_count_Dasha < 4500 and response_count_Dasha >= 500 and response_count_Dasha < 2700 and random.randint(1, 4) == 1)):
			response_made = False
			#Coin flip
			if (random.randint(1, 2) == 1):
				#single term match from user message words
				for word in message_words:
					try:
						if (dictionary_Dasha[word]['emotion'] == "temp neutral" or dictionary_Dasha[word]['emotion'] == "permanent neutral"):
							continue
						else:
							for message in temp_message_keys:
								if message.find(word) != -1:
									Xchatlog.append("Dasha (Thinking): Single term match found for term: " + word)
									Dasha_previous_response = botReply_Dasha(random.choice(message_dict2_Dasha[current_mood_Dasha["mood"]][message]))
									response_made = True
									break
							if response_made:
								break
					except(KeyError):
						continue
				if response_made:
					break
			else:
				#Single term match for a word associated with highest association count from user message word
				for word in message_words:
					temp_dictionary_Dasha = {}
					try:
						temp_dictionary_Dasha = dictionary_Dasha[word]['associated']
						if (len(temp_dictionary_Dasha.keys()) == 0):
							continue
					except(KeyError):
						continue
					temp_highest = max(temp_dictionary_Dasha.values())
					highest_associated = [k for k, v in temp_dictionary_Dasha.items() if v == temp_highest]
					highest_associated_chosen = ''
					if (len(highest_associated) == 1):
						highest_associated_chosen = highest_associated[0]
					else:
						highest_associated_chosen = random.choice(highest_associated)
					if (dictionary_Dasha[highest_associated_chosen]['emotion'] == "temp neutral" or dictionary_Dasha[highest_associated_chosen]['emotion'] == "permanent neutral"):
						continue
							
					for message in temp_message_keys:
						if message.find(highest_associated_chosen) != -1:
							Xchatlog.append("Dasha (Thinking): Single term associated match found for associated term: " + highest_associated_chosen)
							Dasha_previous_response = botReply_Dasha(random.choice(message_dict2_Dasha[current_mood_Dasha["mood"]][message]))
							response_made = True
							break
					if response_made:
						break
				if response_made:
					break
					 	
				
		#No match, either add to list of responses or learn new one based on reply mood
		Xchatlog.append("Dasha (Thinking): Message not recognized.")
		try:
			message_dict2_Dasha[reply_mood["mood"]][Dasha_previous_response]
		except(KeyError):
			Xchatlog.append("Dasha (Thinking): Learned new '" + reply_mood["mood"] + "' response.")
			message_dict2_Dasha[reply_mood["mood"]][Dasha_previous_response] = []
		duplicate_found = False
		for response in message_dict2_Dasha[reply_mood["mood"]][Dasha_previous_response]:
			if (response == user_message_Dasha):
				duplicate_found = True
				break
		if (not(duplicate_found)):
			Xchatlog.append("Dasha (Thinking): Added to '" + reply_mood["mood"] + "' responses.")
			message_dict2_Dasha[reply_mood["mood"]][Dasha_previous_response].append(user_message_Dasha)

		#Give random response from current mood
		Xchatlog.append("Dasha (Thinking): Gave random response.")	
		Dasha_previous_response = botReply_Dasha(random.choice(random.choice(list(message_dict2_Dasha[current_mood_Dasha["mood"]].values()))))
		break
		

print("\nEND OF CHAT\n")

print("Outputting chatlogs...")
#Output regular and extended chatlogs
chatlogOutput(chatlogFile["regular"], chatlog)
chatlogOutput(chatlogFile["extended"], Xchatlog)
print("Chatlog output complete.")
