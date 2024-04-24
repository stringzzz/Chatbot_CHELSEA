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

# Chatbot CHELSEA: CHat Emotion Logic SEnse Automator (0.13) (BETA)
# Project Start Date: 02-20-2024
# Version 0.04 (Not fully tested): 02-27-2024
# Version 0.05 (All tested except Math Logic) 02-28-2024
# Version 0.06 (Added current topic logic) 03-02-2024
# Version 0.07 (Added WH-Question logic) 03-02-2024
# Version 0.08 (Added 'What do you mean' logic) 03-03-2024
# Version 0.09 (Added more question logic, some other small changes) 03-05-2024
# Version 0.10 (Added counts for all associated words and converted file i/o to json) 03-10-2024
# Version 0.11 ('depth match', uses matching words from previous 3 msg/resp. pairs) 03-11-2024
# Version 0.12 (Cleaned inconsistent var cases, added detection of exclaim for emphasis) 03-15-2024
# Version 0.13 (Expanded on message dictionary so multiple responses can be stored per message) 03-15-2024
# Version 0.14 (Gave her method for storing and asking unanswered questions about words in her dictionary) 04-05-2024 

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
# 12. Keep track of matching words from 3 previous message/response pairs
# Get list of these 'depth words'
#
# 13. Mark unknown words in dictionary for 'what is/are __' unanswered questions
#
# 14. Check for answer to previous 'what is/are question'
#
# 15. Check if user is asking What Question, give possible answer response if so
#
# 16. Check if user asking for clarification on previous response,
# try to find matching message containing 2 or more words from
# previous response
#
# 17. Check if asking what CHELSEA feels about ___,
# respond according to the tied emotions with the words in ___
#
# 18. Check if asking 'do you like/dislike ___' question
# respond according to tied emotions to words in ___,
# agreement or disagreement depends on emotion and like/dislike
# word used
#
# 19. Check if asking 'which is better, _1_ or _2_'
# Used emotions tied to the words to decide which CHELSEA likes better,
# or indifferent if neither is tied to happy overall
#
# 20. Check if asking 'why is' question, try to find match involving
# 'because' words a possible answer
# 
# 21. Check for 'most __emotion__' question, respond with biggest word(s) tied to emotion
#
# 22. Check for an exact match of message, give linked response if so
#
# 23. Check if message matches as part of a message in memory,
# give linked reponse if so
#
# 24. If certain # or greater messages and words in dictionary, PRNG to
# determine if attempting topic match, or 'depth match' (Coin flip between two) 
#
# 25. If certain # or greater messages and words in dictionary, PRNG to
# determine if doing single term match. If so, coin flip to determine whether
# trying to match single word from message as part of message in memory,
# or single word associated with word from message. Repond with linked 
# response if so
#
# 26. No match, add response to list in message memory or learn brand new message/response pair
#
# 27. 1/3 chance asking unanswered question, else respond with random response from memory to keep conversation going
#########################################   

import random
import re
import os
import json
from datetime import datetime
from CHELSEA_MATH_LOGIC import CHELSEA_Math_Logic

dictionary = {}
message_dict2 = {}
unanswered_questions = {}
nEmotions = ["happy", "angry", "sad", "afraid"]
current_mood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
pitches = {"happy": 95, "angry": 80, "sad": 90, "afraid": 99}
speeds = {"happy": 150, "angry": 155, "sad": 135, "afraid": 155}
user_message = " "
user_self = {}
chatlog = []
Xchatlog = []
chatlog_file = {"regular": "CHELSEAchatlog.txt", "extended": "CHELSEAXchatlog.txt" }
self = {}
agree = ['Agreed, ', 'True ', 'Yes ', 'I know ', 'True that, ', 'Okay ', 'For sure, ', 'Oh yeah, ', 'Indeed, ', 'Yep, ', 'You know it, ', 'Correct, ']
disagree = ['No, ', 'Disagree, ', 'Wrong, ', 'Not true, ', 'False, ', 'Nope, ', 'Incorrect, ', 'I know otherwise, ', 'Oh no, ', 'Not valid, ', 'Negative, ']
topics = {}
previous_pairs = []
unanswered_question_asked = False

def addToMood():
	#Add the emotional values of the user reply to CHELSEA's emotional values
	for emotion in nEmotions:
		current_mood[emotion] += reply_mood[emotion]

	#Change mood, pitch, and speaking speed according to CHELSEA's emotional values
	temp_dict = { 'happy': current_mood['happy'], 'angry': current_mood['angry'], 'sad': current_mood['sad'], 'afraid': current_mood['afraid'] }
	current_mood["mood"] = getMood2(temp_dict, True)
	current_mood["pitch"] = pitches[current_mood["mood"]]
	current_mood["speed"] = speeds[current_mood["mood"]]
	Xchatlog.append("CHELSEA (Thinking): I feel " + current_mood["mood"])

def getReplyMood():
	#Get the mood of the user reply by looking at the emotion counts gathered on it
	temp_dict = { 'happy': reply_mood['happy'], 'angry': reply_mood['angry'], 'sad': reply_mood['sad'], 'afraid': reply_mood['afraid'] }
	reply_mood["mood"] = getMood2(temp_dict, True)
	Xchatlog.append("CHELSEA (Thinking): " + username + " seems to be " + reply_mood["mood"])

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
	os.system("espeak -v en+f3 -p {} -s {} \" {} \"".format(str(current_mood["pitch"]), str(current_mood["speed"]), botResponse))
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

with open("dictionary.json", 'r') as dictionary_file:
	dictionary = json.load(dictionary_file)
	
with open("messageDictionary2.json", 'r') as message_dictionary_file:
	message_dict2 = json.load(message_dictionary_file)

with open("unanswered_questions.json", 'r') as unanswered_questions_file:
	unanswered_questions = json.load(unanswered_questions_file)

#Get counts for use in activating certain types of message detection
dictionary_count = len(dictionary.keys())
response_count = 0
for emotion in nEmotions:
	response_count += len(message_dict2[emotion])
	
#Input CHELSEA self file
with open("CHELSEAself.json", 'r') as self_file:
	self = json.load(self_file)
			
print("Memory input complete!\n")

#Get username
botReply("What is your name? ")
username = input("")
username = re.sub(r"( )", "_", username)

#Input the user file for the current user, if it exists
try: 
	with open("" + username + ".json", 'r') as user_file:
		user_self = json.load(user_file)
except(FileNotFoundError):
	#New user detected
	user_self = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'uam': [], 'uamnot': []}

#Initial message
CHELSEA_previous_response = "hello"
botReply("hello, " + username)

#Chat loop
while user_message != "//exit":

	#User reply
	print(username + ": ", end = '')
	user_message = (input("")).lower()
	chatlog.append(username + ": " + user_message)
	Xchatlog.append("\n" + username + ": " + user_message)
	if user_message == "//exit":
		break
		
	#Math comprehension logic
	m1 = re.search(r"what does ([a-zA-Z0-9\(\)\*/\^\-\+ ,]*) (equal|=)\??", user_message)
	if (m1):
		Xchatlog.append("CHELSEA (Thinking): Was asked a math question.")
		math_output = CHELSEA_Math_Logic(m1)
		print("CHELSEA: " + math_output)
		if (math_output == "Invalid expression!"):
			Xchatlog.append("CHELSEA (Thinking): Incorrect syntax or error for math question.")
			os.system("espeak -v en+f4 -p {} -s {} \" {} \"".format(str(current_mood["pitch"]), str(current_mood["speed"]), math_output))
		else:
			Xchatlog.append("CHELSEA (Thinking): I have the solution to the math question.")
		chatlog.append("CHELSEA: " + math_output)
		Xchatlog.append("CHELSEA: " + math_output)
		continue
	
	#Ask CHELSEA what she is or is not
	match1 = re.search(r"what are you( not)?\?*$", user_message)
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
	match1 = re.search(r"what am i( not)?\?*$", user_message)
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
	match1 = re.search(r"^(?:are you|you are|you're) (not )?([a-z0-9, '\-]*)\?*", user_message)
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
			if (not(re.search(r"are you[a-z ]*\?*", user_message))):
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
			if (not(re.search(r"are you[a-z '\-]*\?*", user_message))):
				self['iamnot'].append(match1.group(2))		
				Xchatlog.append("CHELSEA (Thinking): Learned new 'I am not'.")
		
	#Deal with current user's identity properties	
	match1 = re.search(r"^(?:i am|i'm) (not )?(.*)", user_message)
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
				
	#Filter certain chars from userMessage
	user_message = re.sub(r"([^a-z0-9, \"'\-\?!])", '', user_message)
	
	#Detect exclamation points at end of user_message to add emotional emphasis (Multiply counts by (exclaim_count + 1))
	exclaim_count = 1
	exclaim_match = re.search(r"(!+)$", user_message)
	if (exclaim_match):
		Xchatlog.append("CHELSEA (Thinking): Exclamation detected, exclaim count: " + str(len(exclaim_match.group(1))))
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
				user_self[dictionary[word]['emotion']] += (1 * exclaim_count)
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
		for word in unknown_words:
			unanswered_questions["what is/are " + word + '?'] = ''
			Xchatlog.append("CHELSEA (Thinking): Learned unknown words as unanswered questions")
		
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
	temp_pair.append(user_message)
	previous_pairs.append(temp_pair)
	if (len(previous_pairs) > 3):
		del previous_pairs[0]
	
	#Get depth words
	depth_words = []	
	if (len(previous_pairs) == 3):
		temp_depth_words = {}		
		for pair in previous_pairs:
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
			
	#Check for answer to previous what is/are question
	if (unanswered_question_asked):
		question_word = re.search(r"what is/are ([a-z '\-]+)", CHELSEA_previous_response)
		if (question_word):
			question_word = question_word.group(1)
			answer = re.search(re.compile("(" + question_word + " (is|are) [a-z '\-]+)"), user_message)
			if (answer):
				Xchatlog.append("CHELSEA (Thinking): Answered what is/are question.")
				temp_question = CHELSEA_previous_response
				CHELSEA_previous_response = re.sub(r"(is/are)", answer.group(2), CHELSEA_previous_response)
				message_dict2[reply_mood["mood"]][CHELSEA_previous_response] = []
				message_dict2[reply_mood["mood"]][CHELSEA_previous_response].append(user_message)
				Xchatlog.append("CHELSEA (Thinking): Deleted unanswered what is/are question.")
				del unanswered_questions[temp_question]
			else:
				Xchatlog.append("CHELSEA (Thinking): Unanswered question still not answered, moving on.")		
	unanswered_question_asked = False
	
	#Check for possible matching answer to What Question in both keys and values under current mood
	response_made = False
	whq_match_object = re.search(r"what (is|are) ([a-z '\-]+)\?*$", user_message)

	temp_message_keys = list(message_dict2[current_mood["mood"]].keys())
	random.shuffle(temp_message_keys) #Note, this shuffled list is potentially re-used in other parts of the script
	
	if (whq_match_object):
		temp_message_values = list(message_dict2[current_mood["mood"]].values())
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
			continue
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
			continue
	
	#Check for question about previous message meaning
	meaning_match = re.search(r"(what (do you|does that) mean|(can you|(do you|can you) care to) clarify|I('m| am) confused|I do( not|n't) (understand|get( it)?)( what you mean| what (that|this) means)?|why (do|did) you (say|think) (that|this))\?*$", user_message)
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
			continue
			
	#Ask what CHELSEA feels about ___
	feel_about_match = re.search(r"(?:how|what) do you (?:feel|think) (?:about|toward(?:s)?) ([a-z0-9, '\-]+)\?*$", user_message)
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
			continue
		else:
			Xchatlog.append("CHELSEA (Thinking): Have emotion to answer question.")
			CHELSEA_previous_response = botReply("i feel " + feel_emotion + ' about ' + feel_about_match.group(1))
			response_made = True
			continue
			
	#Ask do you like question
	like_match = re.search(r"^do you (like|love|enjoy|adore|appreciate|dislike|hate|loathe|detest|despise) ([a-z0-9, '\-]+)\?*$", user_message)
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
			continue
		else:
			Xchatlog.append("CHELSEA (Thinking): Neither like or dislike")
			CHELSEA_previous_response = botReply("i don't feel anything about " + like_match.group(2))
			response_made = True
			continue
			
	#Ask which is better, 1 or 2?
	better_match = re.search(r"(?:which|what) (?:is (?:better,? ?|best,? ?)|do you (?:like (?:better,? ?|best,? ?|more,? ?))) ([a-z0-9, '\-]+) or ([a-z0-9, '\-]+)\?*$", user_message)
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
				continue
			elif (happy_count2 > happy_count1):
				Xchatlog.append("CHELSEA (Thinking): Determined I like second option better.")
				CHELSEA_previous_response = botReply("i like both, but " + better_match.group(2) + ' most')
				response_made = True
				continue
			else:	
				Xchatlog.append("CHELSEA (Thinking): Determined I like both equally.")
				CHELSEA_previous_response = botReply("i like both " + better_match.group(1) + ' & ' + better_match.group(2) + ' the same')
				response_made = True
				continue
		elif (better_emotion1 == 'happy' and better_emotion2 != 'happy'):
			Xchatlog.append("CHELSEA (Thinking): Found like first.")
			CHELSEA_previous_response = botReply("i like " + better_match.group(1) + ' better ')
			response_made = True
			continue
		elif (better_emotion1 != 'happy' and better_emotion2 == 'happy'):
			Xchatlog.append("CHELSEA (Thinking): Found like second.")
			CHELSEA_previous_response = botReply("i like " + better_match.group(2) + ' better ')
			response_made = True
			continue
		elif (better_emotion1 != 'happy' and better_emotion2 != 'happy'):
			Xchatlog.append("CHELSEA (Thinking): Like neither.")
			CHELSEA_previous_response = botReply("i don't prefer either " + better_match.group(1) + ' or ' + better_match.group(2))
			response_made = True
			continue
			
	#Check for 'why is' question match
	whyis_match = re.search(r"why (?:is|are) ([a-z0-9, '\-]+)\?*$", user_message)
	if (whyis_match):
		whyis_words = (re.sub(r"([^a-z0-9 '\-])", '', whyis_match.group(1))).split(" ")
		temp_message_values = list(message_dict2[current_mood["mood"]].values())
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
						CHELSEA_previous_response = botReply(message)
						response_made = True
						break
				if response_made:
					break
		if response_made:
			continue
	
	#Ask 'most' question		
	max1 = []
	temp_emotion = ''
	happy_words = ['happy', 'contented', 'content', 'cheerful', 'cheery', 'merry', 'joyful', 'jovial', 'jolly', 'gleeful', 'delighted', 'joyous', 'thrilled', 'exuberant', 'elated', 'exhilarated', 'ecstatic', 'blissful', 'overjoyed']
	m1 = re.search(re.compile("what makes you most (" + "|".join(happy_words) + ")\?*$"), user_message)
	if (m1):
		max1 = getMost(dictionary, 'happy')
		temp_emotion = 'happy'
		
	angry_words = ['angry', 'frustrated', 'irate', 'vexed', 'irritated', 'exasperated', 'indignant', 'aggrieved', 'irked', 'piqued', 'displeased', 'provoked', 'galled', 'resentful', 'furious', 'enraged', 'infuriated', 'raging', 'incandescent', 'wrathful', 'fuming', 'ranting', 'raving', 'seething', 'frenzied', 'beside oneself', 'outraged', 'choleric', 'crabby', 'waspish', 'hostile', 'antagonistic', 'mad', 'livid', 'boiling', 'riled', 'aggravated', 'sore', 'ticked off', 'ill-tempered', 'acrimonious']
	m1 = re.search(re.compile("what makes you most (" + "|".join(angry_words) + ")\?*$"), user_message)
	if (m1):
		max1 = getMost(dictionary, 'angry')
		temp_emotion = 'angry'
	sad_words = ['sad', 'unhappy', 'sorrowful', 'depressed', 'downcast', 'miserable', 'glum', 'gloomy', 'dismal', 'blue', 'melancholy']
	m1 = re.search(re.compile("what makes you most (" + "|".join(sad_words) + ")\?*$"), user_message)
	if (m1):
		max1 = getMost(dictionary, 'sad')
		temp_emotion = 'sad'
	afraid_words = ['afraid', 'frightened', 'scared', 'terrified', 'fearful', 'petrified', 'nervous', 'worried', 'panicky', 'timid', 'spooked']
	m1 = re.search(re.compile("what makes you most (" + "|".join(afraid_words) + ")\?*$"), user_message)
	if (m1):
		max1 = getMost(dictionary, 'afraid')
		temp_emotion = 'afraid'	
	
	#'most' question continued: Get max(es) for emotional words, respond accordingly	
	if (len(max1) == 1):	
		Xchatlog.append("CHELSEA (Thinking): Most " + temp_emotion + " match found.")
		CHELSEA_previous_response = botReply(max1[0] + " makes me most " + temp_emotion)
		response_made = True
		continue
	elif (len(max1) > 1):
		Xchatlog.append("CHELSEA (Thinking): Most " + temp_emotion + " matches found.")
		CHELSEA_previous_response = botReply(random.choice(max1) + " is one of many that makes me most " + temp_emotion)
		response_made = True
		continue
	
	#Check for exact match under current mood
	try:
		message_dict2[current_mood["mood"]][user_message]
		Xchatlog.append("CHELSEA (Thinking): Exact message match found.")
		CHELSEA_previous_response = botReply(random.choice(message_dict2[current_mood["mood"]][user_message]))
		continue
	except(KeyError):
		pass #Exact match not found in message dictionary
			
	#Check for partial match under current mood
	for message in temp_message_keys:
		if message.find(user_message) != -1:
			Xchatlog.append("CHELSEA (Thinking): Partial message match found.")
			CHELSEA_previous_response = botReply(random.choice(message_dict2[current_mood["mood"]][message]))
			response_made = True
			break
	if response_made:
		continue
		
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
				continue
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
					CHELSEA_previous_response = botReply(random.choice(message_dict2[current_mood["mood"]][message]))
					response_made = True
					break
			if response_made:
				continue
		
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
								CHELSEA_previous_response = botReply(random.choice(message_dict2[current_mood["mood"]][message]))
								response_made = True
								break
						if response_made:
							break
				except(KeyError):
					continue
			if response_made:
				continue
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
						CHELSEA_previous_response = botReply(random.choice(message_dict2[current_mood["mood"]][message]))
						response_made = True
						break
				if response_made:
					break
			if response_made:
				continue
				 	
			
	#No match, either add to list of responses or learn new one based on reply mood
	Xchatlog.append("CHELSEA (Thinking): Message not recognized.")
	try:
		message_dict2[reply_mood["mood"]][CHELSEA_previous_response]
	except(KeyError):
		Xchatlog.append("CHELSEA (Thinking): Learned new '" + reply_mood["mood"] + "' response.")
		message_dict2[reply_mood["mood"]][CHELSEA_previous_response] = []
	duplicate_found = False
	for response in message_dict2[reply_mood["mood"]][CHELSEA_previous_response]:
		if (response == user_message):
			duplicate_found = True
			break
	if (not(duplicate_found)):
		Xchatlog.append("CHELSEA (Thinking): Added to '" + reply_mood["mood"] + "' responses.")
		message_dict2[reply_mood["mood"]][CHELSEA_previous_response].append(user_message)

	if (random.randint(1, 6) == 1 and len(list(unanswered_questions.keys())) > 0):
		#Ask unanswered question
		Xchatlog.append("CHELSEA (Thinking): Asked random what is/are question, waiting for valid answer.")
		CHELSEA_previous_response = botReply(random.choice(list(unanswered_questions.keys())))
		unanswered_question_asked = True
	else:
		#Give random response from current mood
		Xchatlog.append("CHELSEA (Thinking): Gave random response.")	
		CHELSEA_previous_response = botReply(random.choice(random.choice(list(message_dict2[current_mood["mood"]].values()))))

#Output memory
print("\nOutputting memory...")

#Output word dictionary
with open("dictionary.json", 'w') as dictionary_file:
	json.dump(dictionary, dictionary_file)
	
#Output message/response dictionary
with open("messageDictionary2.json", 'w') as message_dictionary_file:
	json.dump(message_dict2, message_dictionary_file)

#Output unanswered questions dictionary
with open("unanswered_questions.json", 'w') as unanswered_questions_file:
	json.dump(unanswered_questions, unanswered_questions_file)
	
#Output regular and extended chatlogs
chatlogOutput(chatlog_file["regular"], chatlog)
chatlogOutput(chatlog_file["extended"], Xchatlog)

#Output CHELSEA data file
data_file = open("CHELSEAdata.txt", 'w')
data_file.write(username + "\nWords in emotion dictionary: " + str(len(dictionary.keys())) + "\n")
message_count = 0
for emotion in nEmotions:
	message_count += len(message_dict2[emotion])
	data_file.write("Number of " + emotion + " message/response pairs: " + str(len(message_dict2[emotion])) + "\n")
data_file.write("Total message/response pairs: " + str(message_count))
data_file.write("\nNumber of unanswered questions: " + str(len(unanswered_questions.keys())))
data_file.close()

#Output user profile (With educated guess emotional state) and user self properties
user_emotions = {}
for emotion in nEmotions:
	user_emotions[emotion] = user_self[emotion]
user_overall_mood = getMood2(user_emotions, True)
user_self['mood'] = username + " seems to be a(n) " + user_overall_mood + " person."
with open("" + username + ".json", 'w') as user_file:
	json.dump(user_self, user_file)

#Output CHELSEA self file
with open("CHELSEAself.json", 'w') as self_file:
	json.dump(self, self_file)

print("Memory output complete.\n")
