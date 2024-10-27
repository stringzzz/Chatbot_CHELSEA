#   chatbotCHELSEA, an AI chatbot with simulated emotions, math logic, and some self identity (chelsea class)
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

# Chatbot CHELSEA: CHat Emotion Logic SEnse Automator (0.18) (BETA)
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
# ##########################################################################################################
# Major changes (Version 0.15):
# Converted all of CHELSEA's variables  and i/o into a class with different methods 10-04-2024
# Changed all concatenated strings to f-strings 10-05-2024
# Continued putting all code into class methods. I am more convinced this is the correct decision now,
# 	as it seems like CHELSEA will be easier to work with and add to now.
# All the changes to the code for this version were purely cosmetic, except that now the user can easily
# choose to give their own chatbot whatever name they like. 10-06-2024
# Added indentation to all json dump outputs to allow for human-readeable memory files 10-10-2024
############################################################################################################
# Version 0.16 (Chooses word from previous user reply to try and find unanswered question to ask) 10-25-2024
# Version 0.17 (Reimplemented unused seen count, used currently for determining popular words, 
# also uses in 'what is/are' questions) 10-26-2024
############################################################################################################
# Version 0.18 (Memory conversion! 'unanswered_questions2.json' now includes 'why is/are' questions) 10-27-2024
# When learning new response, checks for '_1_ is/are _2_' pattern, then checks if 'because/etc' answer exists in memory
# If not, learn new question, has chance of asking one of these questions later on
# If question asked, waits for valid answer to question, or moves on if user doesn't answer it
# Experimental! Would be much better if it filtered improper grammar, but for not answering the question with:
# "that's not proper grammar", "that is incorrect grammar", etc. will delete the question
############################################################################################################

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
# 14. Check for answer to previous 'what is/are' question
#
# 15. Check for answer to previous 'why is/are' question
#
# 16. Check if user is asking What Question, give possible answer response if so
#
# 17. Check if user asking for clarification on previous response,
# try to find matching message containing 2 or more words from
# previous response
#
# 18. Check if asking what CHELSEA feels about ___,
# respond according to the tied emotions with the words in ___
#
# 19. Check if asking 'do you like/dislike ___' question
# respond according to tied emotions to words in ___,
# agreement or disagreement depends on emotion and like/dislike
# word used
#
# 20. Check if asking 'which is better, _1_ or _2_'
# Used emotions tied to the words to decide which CHELSEA likes better,
# or indifferent if neither is tied to happy overall
#
# 21. Check if asking 'why is' question, try to find match involving
# 'because' words a possible answer
# 
# 22. Check for 'most __emotion__' question, respond with biggest word(s) tied to emotion
#
# 23. Check for an exact match of message, give linked response if so
#
# 24. Check if message matches as part of a message in memory,
# give linked reponse if so
#
# 25. If certain # or greater messages and words in dictionary, PRNG to
# determine if attempting topic match, or 'depth match' (Coin flip between two) 
#
# 26. If certain # or greater messages and words in dictionary, PRNG to
# determine if doing single term match. If so, coin flip to determine whether
# trying to match single word from message as part of message in memory,
# or single word associated with word from message. Repond with linked 
# response if so
#
# 27. No match, add response to list in message memory or learn brand new message/response pair
#
# 28. 1/6 chance asking unanswered question, else respond with random response from memory to keep conversation going
#########################################  

import json
import os
import re
import random
from datetime import datetime
from CHELSEA_MATH_LOGIC import CHELSEA_Math_Logic

class chelsea:
	def __init__(self, bot_name):
		self.bot_name = bot_name
		self.dictionary = {}
		self.message_dict2 = {}
		self.unanswered_questions = {}
		self.popular_words = {"happy": [], "angry": [], "sad": [], "afraid": []}
		self.nEmotions = ["happy", "angry", "sad", "afraid"]
		self.current_mood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
		self.pitches = {"happy": 95, "angry": 80, "sad": 90, "afraid": 99}
		self.speeds = {"happy": 150, "angry": 155, "sad": 135, "afraid": 155}
		self.user_message = " "
		self.user_self = {}
		self.chatlog = []
		self.Xchatlog = []
		self.chatlog_file = {"regular": f"{self.bot_name}chatlog.txt", "extended": f"{self.bot_name}Xchatlog.txt" }
		self.chelsea_self = {}
		self.agree = ['agreed, ', 'true ', 'yes ', 'i know ', 'true that, ', 'okay ', 'for sure, ', 'oh yeah, ', 'indeed, ', 'yep, ', 'you know it, ', 'correct, ']
		self.disagree = ['no, ', 'disagree, ', 'wrong, ', 'not true, ', 'false, ', 'nope, ', 'incorrect, ', 'i know otherwise, ', 'oh no, ', 'not valid, ', 'negative, ']
		self.topics = {}
		self.previous_pairs = []

		self.unanswered = {"what": False, "why is": False, "why are": False}

	#Input memory
	def input_dictionary(self):
		with open("dictionary.json", 'r') as dictionary_file:
			self.dictionary = json.load(dictionary_file)
		
		self.dictionary_count = len(self.dictionary.keys())

	def input_message_dictionary(self):
		with open("messageDictionary2.json", 'r') as message_dictionary_file:
			self.message_dict2 = json.load(message_dictionary_file)

		self.response_count = 0
		for emotion in self.nEmotions:
			self.response_count += len(self.message_dict2[emotion])

	def input_unanswered_questions(self):
		with open("unanswered_questions2.json", 'r') as unanswered_questions_file:
			self.unanswered_questions = json.load(unanswered_questions_file)

	def input_self(self):
		try:
			with open(f"{self.bot_name}self.json", 'r') as self_file:
				self.chelsea_self = json.load(self_file)
		except(FileNotFoundError):
			self.chelsea_self = {"iam": [], "iamnot": []}

	def input_memory(self):
		#Input memory
		self.input_dictionary()
		self.input_message_dictionary()
		self.input_unanswered_questions()
		self.input_self()

	def input_user_self(self):
		#Get self.username
		self.botReply("What is your name? ")
		self.username = input("")
		self.username = re.sub(r"( )", "_", self.username)

		#Input the user file for the current user, if it exists
		try: 
			with open(f"{self.username}.json", 'r') as user_file:
				self.user_self = json.load(user_file)
		except(FileNotFoundError):
			#New user detected
			self.user_self = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'uam': [], 'uamnot': []}

	#Output memory
	def output_dictionary(self):
		with open("dictionary.json", 'w') as dictionary_file:
			json.dump(self.dictionary, dictionary_file, indent=4)
			
	def output_message_dictionary(self):
		with open("messageDictionary2.json", 'w') as message_dictionary_file:
			json.dump(self.message_dict2, message_dictionary_file, indent=4)

	def output_unanswered_questions(self):
		with open("unanswered_questions2.json", 'w') as unanswered_questions_file:
			json.dump(self.unanswered_questions, unanswered_questions_file, indent=4)

	def output_self(self):
		with open(f"{self.bot_name}self.json", 'w') as self_file:
			json.dump(self.chelsea_self, self_file, indent=4)

	def chatlogOutput(self, chatlogFile, chatList):
		chatlog_file = open(f"{chatlogFile}", 'a')
		chatlog_file.write(f"\n\n\n{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}")
		for line in chatList:
			chatlog_file.write(f"\n{line}")
		chatlog_file.close()		
	
	def output_chatlogs(self):
		self.chatlogOutput(self.chatlog_file["regular"], self.chatlog)
		self.chatlogOutput(self.chatlog_file["extended"], self.Xchatlog)

	def output_chelsea_data(self):
		data_file = open(f"{self.bot_name}data.txt", 'w')
		data_file.write(f"Words in emotion dictionary: {len(self.dictionary.keys())}\n")
		for emotion in self.nEmotions:
			data_file.write(f"Number of {emotion} words in dictionary: {len([word for word in self.dictionary.keys() if self.dictionary[word]["emotion"] == emotion])}\n")
		data_file.write("\n")
		
		message_count = 0
		for emotion in self.nEmotions:
			message_count += len(self.message_dict2[emotion])
			data_file.write(f"Number of {emotion} message/response pairs: {len(self.message_dict2[emotion])}\n")
		data_file.write(f"Total message/response pairs: {message_count}")

		data_file.write(f"\n\nNumber of unanswered 'what is/are' questions: {len(self.unanswered_questions["what"].keys())}")
		data_file.write(f"\nNumber of unanswered 'why is' questions: {len(self.unanswered_questions["why is"].keys())}")
		data_file.write(f"\nNumber of unanswered 'why are' questions: {len(self.unanswered_questions["why are"].keys())}")
		for emotion in self.nEmotions:
			data_file.write(f"\n\nPopular {emotion} words: {", ".join(self.popular_words[emotion])}")
		data_file.close()

	def output_memory(self):
		self.output_dictionary()
		self.output_message_dictionary()
		self.output_unanswered_questions()
		self.output_self()
		self.output_chatlogs()
		self.output_chelsea_data()

	def output_user_self(self):
		#Output user profile (With educated guess emotional state) and user self properties
		user_emotions = {}
		for emotion in self.nEmotions:
			user_emotions[emotion] = self.user_self[emotion]
		user_overall_mood = self.getMood2(user_emotions, True)
		self.user_self['mood'] = f"{self.username} seems to be a(n) {user_overall_mood} person."
		with open(f"{self.username}.json", 'w') as user_file:
			json.dump(self.user_self, user_file, indent=4)
		
	#Other methods
	def addToMood(self):
		#Add the emotional values of the user reply to CHELSEA's emotional values
		for emotion in self.nEmotions:
			self.current_mood[emotion] += self.reply_mood[emotion]

		#Change mood, pitch, and speaking speed according to CHELSEA's emotional values
		temp_dict = { 'happy': self.current_mood['happy'], 'angry': self.current_mood['angry'], 'sad': self.current_mood['sad'], 'afraid': self.current_mood['afraid'] }
		self.current_mood["mood"] = self.getMood2(temp_dict, True)
		self.current_mood["pitch"] = self.pitches[self.current_mood["mood"]]
		self.current_mood["speed"] = self.speeds[self.current_mood["mood"]]
		self.Xchatlog.append(f"{self.bot_name} (Thinking): I feel {self.current_mood["mood"]}")

	def getReplyMood(self):
		#Get the mood of the user reply by looking at the emotion counts gathered on it
		temp_dict = { 'happy': self.reply_mood['happy'], 'angry': self.reply_mood['angry'], 'sad': self.reply_mood['sad'], 'afraid': self.reply_mood['afraid'] }
		self.reply_mood["mood"] = self.getMood2(temp_dict, True)
		self.Xchatlog.append(f"{self.bot_name} (Thinking): {self.username} seems to be {self.reply_mood["mood"]}")

	def getMood2(self, moodDictionary, botTF):
		#Get the overall mood of either CHELSEA or the user's response
		highest = max(moodDictionary.values())
		max1 = [k for k, v in moodDictionary.items() if v == highest]
		if (len(max1) == 1):	
			return max1[0]
		if (botTF):
			return 'happy'
		else:
			return 'temp neutral'

	def botReply(self, botResponse):
		#Do the various parts of CHELSEA's response, text output, text-to-speech with espeak, chatlogs
		print(f"{self.bot_name}: {botResponse}")
		os.system(f"espeak -v en+f3 -p {self.current_mood["pitch"]} -s {self.current_mood["speed"]} \" {botResponse} \"")
		self.chatlog.append(f"{self.bot_name}: {botResponse}")
		self.Xchatlog.append(f"{self.bot_name}: {botResponse}")
		return botResponse

	def getMost(self, dictio, emotion):
		temp_dict = {}
		for key in dictio.keys():
			if (dictio[key]['emotion'] == emotion):
				temp_dict[key] = dictio[key][emotion]
		highest = max(temp_dict.values())
		max1 = [k for k, v in temp_dict.items() if v == highest]
		return max1
	
	#Chat methods
	def initial_greeting(self):
		#Initial message
		self.CHELSEA_previous_response = "hello"
		self.botReply(f"hello, {self.username}")

	def get_user_reply(self):
		#User reply
		print(f"{self.username}: ", end = '')
		self.user_message = (input("")).lower()
		self.chatlog.append(f"{self.username}: {self.user_message}")
		self.Xchatlog.append(f"\n{self.username}: {self.user_message}")
		if self.user_message == "//exit":
			return True
		return False
		
	def math_comprehension(self):
		#Math comprehension logic
		m1 = re.search(r"what does ([a-zA-Z0-9\(\)\*/\^\-\+ ,]*) (equal|=)\??", self.user_message)
		if (m1):
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked a math question.")
			math_output = CHELSEA_Math_Logic(m1)
			print(f"{self.bot_name}: {math_output}")
			if (math_output == "Invalid expression!"):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Incorrect syntax or error for math question.")
				os.system("espeak -v en+f4 -p {} -s {} \" {} \"".format(str(self.current_mood["pitch"]), str(self.current_mood["speed"]), math_output))
			else:
				self.Xchatlog.append(f"{self.bot_name} (Thinking): I have the solution to the math question.")
			self.chatlog.append(f"{self.bot_name}: {math_output}")
			self.Xchatlog.append(f"{self.bot_name}: {math_output}")
			return True
		return False
	
	def ask_if_is(self):
		#Ask CHELSEA what she is or is not
		match1 = re.search(r"what are you( not)?\?*$", self.user_message)
		if (match1):
			if (not(match1.group(1)) and len(self.chelsea_self['iam']) != 0):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked what I am, have an answer.")
				self.botReply(f"I am {random.choice(self.chelsea_self['iam'])}")
				return True
			elif (match1.group(1) and len(self.chelsea_self['iamnot']) != 0):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked what I am not, have an answer.")
				self.botReply(f"I am not {random.choice(self.chelsea_self['iamnot'])}")
				return True
		return False
	
	def ask_if_user_is(self):
		#Ask CHELSEA what user is or is not
		match1 = re.search(r"what am i( not)?\?*$", self.user_message)
		if (match1):
			if (not(match1.group(1)) and len(self.user_self['uam']) != 0):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked what user is, have an answer.")
				self.botReply(f"You are {re.sub(r"(your)", "my", random.choice(self.user_self['uam']))}")
				return True
			elif (match1.group(1) and len(self.user_self['uamnot']) != 0):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked what user is not, have an answer.")
				self.botReply(f"You are not {re.sub(r"(your)", "my", random.choice(self.user_self['uamnot']))}")
				return True
		return False
	
	def tell_what_is(self):
		#Tell CHELSEA what she is or is not and see if there's agreement according to her self memory
		match1 = re.search(r"^(?:are you|you are|you're) (not )?([a-z0-9, '\-]*)\?*", self.user_message)
		if (match1):
			if (not(match1.group(1))):
				breakout = False
				for iam in self.chelsea_self['iam']:
					if (iam == match1.group(2)):
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found agreement with 'I am'.")
						self.botReply(f"{random.choice(self.agree)}I am {match1.group(2)}")
						breakout = True
						break
				if (breakout):
					return True
				for iamnot in self.chelsea_self['iamnot']:
					if (iamnot == match1.group(2)):
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found disagreement with 'I am'.")
						self.botReply(f"{random.choice(self.disagree)}I am not {match1.group(2)}")
						breakout = True
						break
				if (breakout):
					return True
				if (not(re.search(r"are you[a-z ]*\?*", self.user_message))):
					self.chelsea_self['iam'].append(match1.group(2))		
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new 'I am'.")
			else:
				breakout = False
				for iamnot in self.chelsea_self['iamnot']:
					if (iamnot == match1.group(2)):
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found agreement with 'I am not'.")
						self.botReply(f"{random.choice(self.agree)}I am not {match1.group(2)}")
						breakout = True
						break
				if (breakout):
					return True
				for iam in self.chelsea_self['iam']:
					if (iam == match1.group(2)):
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found disagreement with 'I am not'.")
						self.botReply(f"{random.choice(self.disagree)}I am {match1.group(2)}")
						breakout = True
						break
				if (breakout):
					return True
				if (not(re.search(r"are you[a-z '\-]*\?*", self.user_message))):
					self.chelsea_self['iamnot'].append(match1.group(2))		
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new 'I am not'.")
		return False
	
	def tell_what_user_is(self):
		#Deal with current user's identity properties	
		match1 = re.search(r"^(?:i am|i'm) (not )?(.*)", self.user_message)
		if (match1):
			if (not(match1.group(1))):
				breakout = False
				for uam in self.user_self['uam']:
					if (uam == match1.group(2)):
						uam = re.sub(r"(your)", "my", uam)
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found agreement with 'User am'.")
						self.botReply(f"{random.choice(self.agree)}you are {uam}")
						breakout = True
						break
				if (breakout):
					return True
				for uamnot in self.user_self['uamnot']:
					if (uamnot == match1.group(2)):
						uamnot = re.sub(r"(your)", "my", uamnot)
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found disagreement with 'User am'.")
						self.botReply(f"{random.choice(self.disagree)}you are not {uamnot}")
						breakout = True
						break
				if (breakout):
					return True
				self.user_self['uam'].append(match1.group(2))	
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new 'User am'.")
			else:
				breakout = False
				for uamnot in self.user_self['uamnot']:
					if (uamnot == match1.group(2)):
						uamnot = re.sub(r"(your)", "my", uamnot)
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found agreement with 'User am not'.")
						self.botReply(f"{random.choice(self.agree)}you are not {uamnot}")
						breakout = True
						break
				if (breakout):
					return True
				for uam in self.user_self['uam']:
					if (uam == match1.group(2)):
						uam = re.sub(r"(your)", "my", uam)
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found disagreement with 'User am not'.")
						self.botReply(f"{random.choice(self.disagree)}you are {uam}")
						breakout = True
						break
				if (breakout):
					return True
				self.user_self['uamnot'].append(match1.group(2))		
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new 'User am not'.")
		return False

	def filter_user_reply(self):
		#Filter certain chars from userMessage
		self.user_message = re.sub(r"([^a-z0-9, \"'\-\?!])", '', self.user_message)

	def get_exclaim_count(self):
		#Detect exclamation points at end of user_message to add emotional emphasis (Multiply counts by (self.exclaim_count + 1))
		self.exclaim_count = 1
		exclaim_match = re.search(r"(!+)$", self.user_message)
		if (exclaim_match):
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Exclamation detected, exclaim count: {len(exclaim_match.group(1))}")
			self.exclaim_count = len(exclaim_match.group(1)) + 1

	def split_user_reply(self):
		#Filter out punctuation from user message and split to list of words
		self.message_words = (re.sub(r"([^a-z0-9 '\-])", '', self.user_message)).split(" ")

	def reset_temp_vars(self):
		#Use var name change to self after everything else is added
		self.unknown_words = []
		self.reply_mood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0}
		self.word_emotions = ""
	
	#Detect emotion words, get reply mood, add user reply emotional values to CHELSEA's emotional values
	def detect_emotion_words(self):
		for word in self.message_words:
			if word == '':
				continue
			try:
				if (self.dictionary[word]['emotion'] != "permanent neutral" and self.dictionary[word]['emotion'] != "temp neutral"):
					self.reply_mood[self.dictionary[word]['emotion']] += (1 * self.exclaim_count)
					self.user_self[self.dictionary[word]['emotion']] += (1 * self.exclaim_count)
					self.word_emotions = f"{self.word_emotions}{self.dictionary[word]['emotion']} "
				else: 
					self.word_emotions = f"{self.word_emotions} neutral "
			except(KeyError):
				self.unknown_words.append(word)
				self.word_emotions = f"{self.word_emotions} unknown "
		self.Xchatlog.append(f"Word emotions in previous reply: {self.word_emotions}")

	def detect_unkown_words(self):
		#Mark unknown words in the emotion dictionary according to the overall mood of the user reply
		if len(self.unknown_words) > 0:
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Unknown words detected: {self.unknown_words}")
			for word in self.unknown_words:
				self.dictionary[word] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 1, 'associated': {}}
				self.dictionary[word]['emotion'] = self.reply_mood["mood"] 
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned unknown words as '{self.reply_mood["mood"]}' words.")
			for word in self.unknown_words:
				self.unanswered_questions["what"][f"what is/are {word}?"] = ''
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned unknown words as unanswered questions")

	def add_to_word_counts(self):
		#Add to counts for each word
		for word in self.message_words:
			try:
				if (self.dictionary[word]['emotion'] == 'permanent neutral'):
					continue
			except(KeyError):
				continue
			self.dictionary[word][self.reply_mood["mood"]] += 1  * self.exclaim_count
			self.dictionary[word]["seen"] += 1
			temp_dict = { 'happy': self.dictionary[word]['happy'], 'angry': self.dictionary[word]['angry'], 'sad': self.dictionary[word]['sad'], 'afraid': self.dictionary[word]['afraid'] }
			word_emotion = self.getMood2(temp_dict, False)
			if (word_emotion != self.dictionary[word]['emotion']):
				self.dictionary[word]['emotion'] = word_emotion
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Switched emotion of word '{word}' to {word_emotion}")

	def mark_associated_words(self):
		#Mark associated words in list
		for word in self.message_words:
			try:
				if (self.dictionary[word]['emotion'] == 'permanent neutral' or self.dictionary[word]['emotion'] == 'temp neutral'):
					continue
			except(KeyError):
				continue
			for word2 in self.message_words:
				if (word == word2):
					continue
				try:
					if (self.dictionary[word2]['emotion'] == 'permanent neutral' or self.dictionary[word2]['emotion'] == 'temp neutral'):
						continue
				except(KeyError):
					continue
				try:
					self.dictionary[word]['associated'][word2] += 1
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Added to count of association of {word} and {word2}")
					continue
				except(KeyError):
					self.dictionary[word]['associated'][word2] = 1
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned association of {word} and {word2}")
					continue

	def get_topic_counts(self):
		#Get counts for words in current conversation				
		for word in self.message_words:
			try:
				if (self.dictionary[word]['emotion'] == 'permanent neutral' or self.dictionary[word]['emotion'] == 'temp neutral'):
					continue
			except(KeyError):
				continue
			try:
				self.topics[word] += (1 * self.exclaim_count)
			except(KeyError):
				self.topics[word] = (1 * self.exclaim_count)

	def determine_current_topics(self):
		#Get current topics of the conversation by the highest counts
		if (not(len(self.topics.keys()) == 0)):
			temp_highest = max(self.topics.values())
			self.current_topics = [k for k, v in self.topics.items() if v == temp_highest]
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Current topic(s) is/are {" & ".join(self.current_topics)}")

	def add_to_previous_pairs(self):
		#Add to previous pairs (For depth words)
		self.previous_pairs.append([self.CHELSEA_previous_response, self.user_message])
		if (len(self.previous_pairs) > 3):
			del self.previous_pairs[0]

	def get_depth_words(self):
		#Get depth words
		self.depth_words = []	
		if (len(self.previous_pairs) == 3):
			temp_depth_words = {}		
			for pair in self.previous_pairs:
				temp_messages = (re.sub(r"([^a-z0-9 '\-])", '', pair[0])).split(" ")
				temp_responses = (re.sub(r"([^a-z0-9 '\-])", '', pair[1])).split(" ")
				for word1 in temp_messages:
					try:
						if (self.dictionary[word1]['emotion'] == "permanent neutral" or self.dictionary[word1]['emotion'] == "temp neutral"):
							continue
					except(KeyError):
						continue
					for word2 in temp_responses:
						try:
							if (self.dictionary[word2]['emotion'] == "permanent neutral" or self.dictionary[word2]['emotion'] == "temp neutral"):
								continue
						except(KeyError):
							continue
						if (word1 == word2):
							temp_depth_words[word1] = 1
			self.depth_words = list(temp_depth_words.keys())
			if (len(self.depth_words) > 0):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found depth words: {" ".join(self.depth_words)}")

	def get_popular_words(self):
		#Determine the lists of words for each emotion given highest 'seen' count
		for emotion in self.nEmotions:
			words = [word for word in self.dictionary.keys() if self.dictionary[word]["emotion"] == emotion]
			temp_highest = max([self.dictionary[word]["seen"] for word in words])
			self.popular_words[emotion] = [word for word in words if self.dictionary[word]["seen"] == temp_highest]
	
	def learn_why_isare_question(self):
		#FLAG
		#Detect if _1_ is/are _2_ pattern in previous user reply
		if not(re.search(r'^why', self.user_message)):
			m1 = re.search(r'([a-z ,\'\-]+) (is|are) ([a-z ,\'\-]+)', self.user_message)
			is_match1 = ""
			is_are = ""
			is_match2 = ""
			if m1:
				is_match1 = m1.group(1)
				is_are = m1.group(2)
				is_match2 = m1.group(3)
			else:
				return
			messages = [message for message in self.message_dict2["happy"].keys()]
			for response in self.message_dict2["happy"].values():
				messages.extend(response)
			if not(re.search(r'(because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)', is_match2)):
				because_match_found = False
				#Determine is _1_ is/are _2_ because/etc is found in memory (Answer to question)
				for message2 in messages:
					if not(re.search(r'^why', message2)):
						if message2.find(self.user_message) != -1:
							m1 = re.search(r'[a-z ,\'\-]+ (is|are) ([a-z ,\'\-]+)', message2)
							is_match3 = ""
							if m1:
								is_are2 = m1.group(1)
								is_match3 = m1.group(2)
							else:
								continue
							if re.search(r'(because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)', is_match3) and is_are == is_are2:
								because_match_found = True
								break
							else:
								continue
				if not(because_match_found):
					#Answer to why _1_ is/are _2_ not found, add question
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new 'why is/are' question: 'why {is_are} {is_match1} {is_match2}?'")
					self.unanswered_questions[f"why {is_are}"][f"why {is_are} {is_match1} {is_match2}?".replace("  ", " ")] = ""
			else:
				return

	def check_for_answer_what(self):
		#Check for answer to previous what is/are question
		if (self.unanswered["what"]):
			question_word = re.search(r"what is/are ([a-z ,'\-]+)", self.CHELSEA_previous_response)
			if (question_word):
				question_word = question_word.group(1)
				answer = re.search(re.compile(f"({question_word} (is|are) [a-z ,'\\-]+)"), self.user_message)
				if (answer):
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered what is/are question.")
					temp_question = self.CHELSEA_previous_response
					self.CHELSEA_previous_response = re.sub(r"(is/are)", answer.group(2), self.CHELSEA_previous_response)
					self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response] = []
					self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response].append(self.user_message)
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Deleted unanswered what is/are question, have answer now.")
					del self.unanswered_questions["what"][temp_question]

					#Possibly learn new question from answer:
					self.learn_why_isare_question()
				else:
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Unanswered what is/are question still not answered, moving on.")		
		self.unanswered["what"] = False

	def check_for_answer_why_general(self, isare):
		#FLAG
		if re.search(r"that('s| is) ((not (proper|right|accurate|flawless|good|correct|acceptable|suitable))|(improper|inaccurate|flawed|incorrect|unacceptable|unsuitable)) grammar", self.user_message):
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Deleted unanswered why is question with improper grammar.")
			del self.unanswered_questions[f"why {isare}"][self.CHELSEA_previous_response]
			self.unanswered[f"why {isare}"] = False
			#Give random response from current mood
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Gave random response.")	
			self.CHELSEA_previous_response = self.botReply(random.choice(random.choice(list(self.message_dict2[self.current_mood["mood"]].values()))))
			return True
		question_word = re.search(re.compile(f"why {isare} ([a-z ,'\\-]+)"), self.CHELSEA_previous_response)
		if (question_word):
			question_words = question_word.group(1).replace(",", '').split(" ")
			question_words.append(isare)
			answer = re.search(r"([a-z ,'\-]+) (because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)", self.user_message)
			if not(answer):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Unanswered why {isare} question still not answered, moving on.")
				self.unanswered[f"why {isare}"] = False
				return False
			answer = answer.group(1)
			answer_not_found = False
			for word in question_words:
				if answer.find(word) == -1:
					answer_not_found = True
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Unanswered why {isare} question still not answered, moving on.")
					break
			if not(answer_not_found):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered why {isare} question.")
				temp_question = self.CHELSEA_previous_response
				self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response] = []
				self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response].append(self.user_message)
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Deleted unanswered why {isare} question, have answer now.")
				del self.unanswered_questions[f"why {isare}"][temp_question]
			else:
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Unanswered why {isare} question still not answered, moving on.")

	def check_for_answer_why(self):
		#FLAG
		#Check for answer to previous why is/are question
		if (self.unanswered["why is"]):
			#Why is
			if self.check_for_answer_why_general("is"):
				return True

		elif (self.unanswered["why are"]):
			#Why are 
			if self.check_for_answer_why_general("are"):
				return True
			
		self.unanswered["why is"] = False
		self.unanswered["why are"] = False
		return False

	def answer_whq_question(self):
		#Check for possible matching answer to What Question in both keys and values under current mood
		response_made = False
		whq_match_object = re.search(r"what (is|are) ([a-z '\-]+)\?*$", self.user_message)

		self.temp_message_keys = list(self.message_dict2[self.current_mood["mood"]].keys())
		random.shuffle(self.temp_message_keys) #Note, this shuffled list is potentially re-used in other parts of the script
		
		if (whq_match_object):
			temp_message_values = list(self.message_dict2[self.current_mood["mood"]].values())
			random.shuffle(temp_message_values)
			partial_message = f"{whq_match_object.group(2)} {whq_match_object.group(1)}"
			
			#Check values
			for message in temp_message_values:
				message = random.choice(message)
				if (message == self.CHELSEA_previous_response):
					continue
				if message.find(partial_message) != -1:
					self.Xchatlog.append(f"{self.bot_name} (Thinking): WH-Q question match found in values.")
					self.CHELSEA_previous_response = self.botReply(message)
					response_made = True
					break
			if response_made:
				return True
			#Check keys
			for message in self.temp_message_keys:
				if (message == self.CHELSEA_previous_response):
					continue
				if message.find(partial_message) != -1:
					self.Xchatlog.append(f"{self.bot_name} (Thinking): WH-Q question match found in keys.")
					self.CHELSEA_previous_response = self.botReply(message)
					response_made = True
					break
			if response_made:
				return True
		return False
	
	def give_clarification(self):
		#Check for question about previous message meaning
		response_made = False
		meaning_match = re.search(r"(what (do you|does that) mean|(can you|(do you|can you) care to) clarify|I('m| am) confused|I do( not|n't) (understand|get( it)?)( what you mean| what (that|this) means)?|why (do|did) you (say|think) (that|this))\?*$", self.user_message)
		if (meaning_match):
			previous_words = (re.sub(r"([^a-z0-9 '\-])", '', self.CHELSEA_previous_response)).split(" ")
			random.shuffle(previous_words)
			for message in self.temp_message_keys:
				if (message == self.CHELSEA_previous_response):
					continue
				match_count = 0
				match_words = []
				for word in previous_words:
					try:
						if (self.dictionary[word]['emotion'] == "temp neutral" or self.dictionary[word]['emotion'] == "permanent neutral"):
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
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Previous words meaning match found for: {" & ".join(match_words)}")
						self.CHELSEA_previous_response = self.botReply(message)
						response_made = True
						break
				if response_made:
					break
			if response_made:
				return True
		return False
	
	def ask_what_feel(self):
		#Ask what CHELSEA feels about ___
		feel_about_match = re.search(r"(?:how|what) do you (?:feel|think) (?:about|toward(?:s)?) ([a-z0-9, '\-]+)\?*$", self.user_message)
		if (feel_about_match):
			feel_words = (re.sub(r"([^a-z0-9 '\-])", '', feel_about_match.group(1))).split(" ")
			temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in feel_words:
				try:
					if (self.dictionary[word]['emotion'] == 'temp neutral' or self.dictionary[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
					continue
				temp_dict[self.dictionary[word]['emotion']] += 1
			feel_emotion = self.getMood2(temp_dict, False)
			if (feel_emotion == 'temp neutral'):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Feel nothing.")
				self.CHELSEA_previous_response = self.botReply(f"i feel nothing about {feel_about_match.group(1)}")
				return True
			else:
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Have emotion to answer question.")
				self.CHELSEA_previous_response = self.botReply(f"i feel {feel_emotion} about {feel_about_match.group(1)}")
				return True
		return False
	
	def ask_if_like(self):
		#Ask do you like question
		like_match = re.search(r"^do you (like|love|enjoy|adore|appreciate|dislike|hate|loathe|detest|despise) ([a-z0-9, '\-]+)\?*$", self.user_message)
		if (like_match):
			like_terms = ['like', 'love', 'enjoy', 'adore', 'appreciate']
			dislike_terms = ['dislike', 'hate', 'loathe', 'detest', 'despise']
			like_words = (re.sub(r"([^a-z0-9 '\-])", '', like_match.group(2))).split(" ")
			temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in like_words:
				try:
					if (self.dictionary[word]['emotion'] == 'temp neutral' or self.dictionary[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
					continue
				temp_dict[self.dictionary[word]['emotion']] += 1
			like_emotion = self.getMood2(temp_dict, False)
			if (like_emotion != 'temp neutral'):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Like or dislike match found.")
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
					self.CHELSEA_previous_response = self.botReply(f"yes, i {like_match.group(1)} {like_match.group(2)}")
				elif ((like_emotion == 'happy' and like_dislike == 'dislike') or (like_emotion != 'happy' and like_dislike == 'like')):
					self.CHELSEA_previous_response = self.botReply(f"no, i don't {like_match.group(1)} {like_match.group(2)}")
				return True
			else:
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Neither like or dislike")
				self.CHELSEA_previous_response = self.botReply(f"i don't feel anything about {like_match.group(2)}")
				return True
		return False
	
	def ask_which_better(self):
		#Ask which is better, 1 or 2?
		better_match = re.search(r"(?:which|what) (?:is (?:better,? ?|best,? ?)|do you (?:like (?:better,? ?|best,? ?|more,? ?))) ([a-z0-9, '\-]+) or ([a-z0-9, '\-]+)\?*$", self.user_message)
		if (better_match):
			better_words1 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(1))).split(" ")
			temp_dict1 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in better_words1:
				try:
					if (self.dictionary[word]['emotion'] == 'temp neutral' or self.dictionary[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
					continue
				temp_dict1[self.dictionary[word]['emotion']] += 1
			better_emotion1 = self.getMood2(temp_dict1, False)

			better_words2 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(2))).split(" ")
			temp_dict2 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			for word in better_words2:
				try:
					if (self.dictionary[word]['emotion'] == 'temp neutral' or self.dictionary[word]['emotion'] == 'permanent neutral'):
						continue
				except(KeyError):
					continue
				temp_dict2[self.dictionary[word]['emotion']] += 1
			better_emotion2 = self.getMood2(temp_dict2, False)
			
			if (better_emotion1 == 'happy' and better_emotion2 == 'happy'):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found like both, determining which more.")
				happy_count1 = 0
				happy_count2 = 0
				for word in better_words1:
					happy_count1 += self.dictionary[word]['happy']
				for word in better_words2:
					happy_count2 += self.dictionary[word]['happy']
				if (happy_count1 > happy_count2):
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Determined I like first option better.")
					self.CHELSEA_previous_response = self.botReply(f"i like both, but {better_match.group(1)} most")
					return True
				elif (happy_count2 > happy_count1):
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Determined I like second option better.")
					self.CHELSEA_previous_response = self.botReply(f"i like both, but {better_match.group(2)} most")
					return True
				else:	
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Determined I like both equally.")
					self.CHELSEA_previous_response = self.botReply(f"i like both {better_match.group(1)} & {better_match.group(2)} the same")
					return True
			elif (better_emotion1 == 'happy' and better_emotion2 != 'happy'):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found like first.")
				self.CHELSEA_previous_response = self.botReply(f"i like {better_match.group(1)} better ")
				return True
			elif (better_emotion1 != 'happy' and better_emotion2 == 'happy'):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found like second.")
				self.CHELSEA_previous_response = self.botReply(f"i like {better_match.group(2)} better ")
				return True
			elif (better_emotion1 != 'happy' and better_emotion2 != 'happy'):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Like neither.")
				self.CHELSEA_previous_response = self.botReply(f"i don't prefer either {better_match.group(1)} or {better_match.group(2)}")
				return True
		return False
	
	def ask_why_is(self):
		#Check for 'why is' question match
		response_made = False
		whyis_match = re.search(r"why (?:is|are) ([a-z0-9, '\-]+)\?*$", self.user_message)
		if (whyis_match):
			whyis_words = (re.sub(r"([^a-z0-9 '\-])", '', whyis_match.group(1))).split(" ")
			temp_message_values = list(self.message_dict2[self.current_mood["mood"]].values())
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
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Possible answer to 'why is' question match found in values for: {" ".join(whyis_words)}")
							self.CHELSEA_previous_response = self.botReply(message)
							response_made = True
							break
					if response_made:
						break
			if response_made:
				return True
			
			#Check keys
			for message in self.temp_message_keys:
				because_match = re.search(r"([a-z0-9, '\-]+) (because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)", message)
				if (because_match):
					match_count = 0
					for word in whyis_words:
						if ((because_match.group(1)).find(word) != -1):
							match_count += 1
						else:
							break
						if (match_count == len(whyis_words)):
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Possible answer to 'why is' question match found in keys for: {" ".join(whyis_words)}")
							self.CHELSEA_previous_response = self.botReply(message)
							response_made = True
							break
					if response_made:
						break
			if response_made:
				return True
		return False
	
	def ask_most_question(self):
		#Ask 'most' question		
		max1 = []
		temp_emotion = ''
		happy_words = ['happy', 'contented', 'content', 'cheerful', 'cheery', 'merry', 'joyful', 'jovial', 'jolly', 'gleeful', 'delighted', 'joyous', 'thrilled', 'exuberant', 'elated', 'exhilarated', 'ecstatic', 'blissful', 'overjoyed']
		m1 = re.search(re.compile(f"what makes you most ({"|".join(happy_words)})\\?*$"), self.user_message)
		if (m1):
			max1 = self.getMost(self.dictionary, 'happy')
			temp_emotion = 'happy'
			
		angry_words = ['angry', 'frustrated', 'irate', 'vexed', 'irritated', 'exasperated', 'indignant', 'aggrieved', 'irked', 'piqued', 'displeased', 'provoked', 'galled', 'resentful', 'furious', 'enraged', 'infuriated', 'raging', 'incandescent', 'wrathful', 'fuming', 'ranting', 'raving', 'seething', 'frenzied', 'beside oneself', 'outraged', 'choleric', 'crabby', 'waspish', 'hostile', 'antagonistic', 'mad', 'livid', 'boiling', 'riled', 'aggravated', 'sore', 'ticked off', 'ill-tempered', 'acrimonious']
		m1 = re.search(re.compile(f"what makes you most ({"|".join(angry_words)})\\?*$"), self.user_message)
		if (m1):
			max1 = self.getMost(self.dictionary, 'angry')
			temp_emotion = 'angry'
		sad_words = ['sad', 'unhappy', 'sorrowful', 'depressed', 'downcast', 'miserable', 'glum', 'gloomy', 'dismal', 'blue', 'melancholy']
		m1 = re.search(re.compile(f"what makes you most ({"|".join(sad_words)})\\?*$"), self.user_message)
		if (m1):
			max1 = self.getMost(self.dictionary, 'sad')
			temp_emotion = 'sad'
		afraid_words = ['afraid', 'frightened', 'scared', 'terrified', 'fearful', 'petrified', 'nervous', 'worried', 'panicky', 'timid', 'spooked']
		m1 = re.search(re.compile(f"what makes you most ({"|".join(afraid_words)})\\?*$"), self.user_message)
		if (m1):
			max1 = self.getMost(self.dictionary, 'afraid')
			temp_emotion = 'afraid'	
		
		#'most' question continued: Get max(es) for emotional words, respond accordingly	
		if (len(max1) == 1):	
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Most {temp_emotion} match found.")
			self.CHELSEA_previous_response = self.botReply(f"{max1[0]} makes me most {temp_emotion}")
			return True
		elif (len(max1) > 1):
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Most {temp_emotion} matches found.")
			self.CHELSEA_previous_response = self.botReply(f"{random.choice(max1)} is one of many that makes me most {temp_emotion}")
			return True
		return False
	
	def check_exact_message_match(self):
		#Check for exact match under current mood
		try:
			self.message_dict2[self.current_mood["mood"]][self.user_message]
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Exact message match found.")
			self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][self.user_message]))
			return True
		except(KeyError):
			return False
		
	def check_partial_message_match(self):
		#Check for partial match under current mood
		response_made = False
		for message in self.temp_message_keys:
			if message.find(self.user_message) != -1:
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Partial message match found.")
				self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][message]))
				response_made = True
				break
		if response_made:
			return True
		return False
	
	def check_topic_or_depth_match(self):
		#Check for match with current topic or depth match (Coin flip)
		response_made = False
		if ((not(len(self.topics.keys()) == 0) and (self.dictionary_count >= 2500 and self.response_count >= 1200 and random.randint(1, 3) == 1)) or (not(len(self.topics.keys()) == 0) and (self.dictionary_count >= 600 and self.dictionary_count < 2500 and self.response_count >= 350 and self.response_count < 1200 and random.randint(1, 4) == 1))):
			if (len(self.depth_words) >= 2 and random.randint(1, 2) == 1):
				#Depth match
				for message in self.temp_message_keys:
					depth_found = 0
					two_matched = False
					matched_words = []
					random.shuffle(self.depth_words)
					for word in self.depth_words:
						if message.find(word) != -1:
							depth_found += 1
							matched_words.append(word)
						if (depth_found == 2):
							two_matched = True
							break
					if (not(two_matched)):
						continue
					else:
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Depth match found for: {" ".join(matched_words)}")
						self.CHELSEA_previous_response = self.botReply(message)
						response_made = True
						break
				if response_made:
					return True
			else:	
				#Topic match
				for message in self.temp_message_keys:
					topics_found = True
					for topic in self.current_topics:
						if message.find(topic) == -1:
							topics_found = False
							break
					if (not(topics_found)):
						continue
					else:
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Topic match found.")
						self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][message]))
						response_made = True
						break
				if response_made:
					return True
		return False
	
	def check_single_term_match(self):
		#Check for single term match under current mood, ignore neutral words
		#Only activated when she has learned enough, though this can easily be adjusted
		response_made = False
		if ((self.dictionary_count >= 4500 and self.response_count >= 2700 and random.randint(1, 3) == 1) or (self.dictionary_count >= 2000 and self.dictionary_count < 4500 and self.response_count >= 500 and self.response_count < 2700 and random.randint(1, 4) == 1)):
			response_made = False
			#Coin flip
			if (random.randint(1, 2) == 1):
				#single term match from user message words
				for word in self.message_words:
					try:
						if (self.dictionary[word]['emotion'] == "temp neutral" or self.dictionary[word]['emotion'] == "permanent neutral"):
							continue
						else:
							for message in self.temp_message_keys:
								if message.find(word) != -1:
									self.Xchatlog.append(f"{self.bot_name} (Thinking): Single term match found for term: {word}")
									self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][message]))
									response_made = True
									break
							if response_made:
								break
					except(KeyError):
						continue
				if response_made:
					return True
			else:
				#Single term match for a word associated with highest association count from user message word
				for word in self.message_words:
					temp_dictionary = {}
					try:
						temp_dictionary = self.dictionary[word]['associated']
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
						if (self.dictionary[highest_associated_chosen]['emotion'] == "temp neutral" or self.dictionary[highest_associated_chosen]['emotion'] == "permanent neutral"):
							continue
					except(KeyError):
						continue		
					for message in self.temp_message_keys:
						if message.find(highest_associated_chosen) != -1:
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Single term associated match found for associated term: {highest_associated_chosen}")
							self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][message]))
							response_made = True
							break
					if response_made:
						break
				if response_made:
					return True
		return False
	
	def learn_new_response(self):
		#No match, either add to list of responses or learn new one based on reply mood
		self.Xchatlog.append(f"{self.bot_name} (Thinking): Message not recognized.")
		try:
			self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response]
		except(KeyError):
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new '{self.reply_mood["mood"]}' response.")
			self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response] = []
		duplicate_found = False
		for response in self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response]:
			if (response == self.user_message):
				duplicate_found = True
				break
		if (not(duplicate_found)):
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Added to '{self.reply_mood["mood"]}' responses.")
			self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response].append(self.user_message)

		#Possibly learn new why is/are question from user_message
		self.learn_why_isare_question()


	def give_random_or_question_response(self):
		if random.randint(1, 6) == 1:
			#Ask unanswered question
			if (random.randint(1, 2) == 1 and len(list(self.unanswered_questions["what"].keys())) > 0):
				#Ask 'what is/are' question
				if (random.randint(1, 3) == 1):
					random.shuffle(self.popular_words[self.current_mood["mood"]])
					response_made = False
					for word in self.popular_words[self.current_mood["mood"]]:
						try:
							self.unanswered_questions["what"][f"what is/are {word}?"]
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked what is/are question for '{word}' in popular '{self.current_mood["mood"]}' words, waiting for valid answer.")
							self.CHELSEA_previous_response = self.botReply(f"what is/are {word}?")
							self.unanswered["what"] = True
							response_made = True
							break
						except(KeyError):
							continue
					if response_made:
						return
					for word in self.popular_words[self.current_mood["mood"]]:
						for associated_word in self.dictionary[word]["associated"].keys():
							try:
								self.unanswered_questions["what"][f"what is/are {associated_word}?"]
								self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked what is/are question for '{associated_word}' associated to '{word}' in popular '{self.current_mood["mood"]}' words, waiting for valid answer.")
								self.CHELSEA_previous_response = self.botReply(f"what is/are {associated_word}?")
								self.unanswered["what"] = True
								response_made = True
								break
							except(KeyError):
								continue
						if response_made:
							return
						
				else:
					random.shuffle(self.message_words)
					response_made = False
					for word in self.message_words:
						try:
							self.unanswered_questions["what"][f"what is/are {word}?"]
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked what is/are question for '{word}' in previous user reply, waiting for valid answer.")
							self.CHELSEA_previous_response = self.botReply(f"what is/are {word}?")
							self.unanswered["what"] = True
							response_made = True
							break
						except(KeyError):
							continue
					if response_made:
						return
				#No unanswered question match found from previous user reply words or popular words, use random question instead
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked random what is/are question, waiting for valid answer.")
				self.CHELSEA_previous_response = self.botReply(random.choice(list(self.unanswered_questions["what"].keys())))
				self.unanswered["what"] = True
			else:
				#Ask 'why is/are' question
				if (random.randint(1, 2) == 1):
					#why is
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked random why is question, waiting for valid answer.")
					self.CHELSEA_previous_response = self.botReply(random.choice(list(self.unanswered_questions["why is"].keys())))
					self.unanswered["why is"] = True
				else:
					#why are
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked random why are question, waiting for valid answer.")
					self.CHELSEA_previous_response = self.botReply(random.choice(list(self.unanswered_questions["why are"].keys())))
					self.unanswered["why are"] = True

		else:
			#Give random response from current mood
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Gave random response.")	
			self.CHELSEA_previous_response = self.botReply(random.choice(random.choice(list(self.message_dict2[self.current_mood["mood"]].values()))))

	def chat(self):
		if self.get_user_reply():
			return
		if self.math_comprehension():
			return

		#Identity parts
		if self.ask_if_is():
			return
		if self.ask_if_user_is():
			return
		if self.tell_what_is():
			return
		if self.tell_what_user_is():
			return

		#Initial counts and markings
		self.filter_user_reply()
		self.get_exclaim_count()
		self.split_user_reply()
		self.reset_temp_vars()
		self.detect_emotion_words()
		self.getReplyMood()
		self.addToMood()
		self.detect_unkown_words()
		self.add_to_word_counts()
		self.mark_associated_words()
		self.get_topic_counts()
		self.determine_current_topics()
		self.add_to_previous_pairs()
		self.get_depth_words()
		self.get_popular_words()
		self.check_for_answer_what()
		if self.check_for_answer_why():
			return

		#Reponses
		if self.answer_whq_question():
			return
		if self.give_clarification():
			return
		if self.ask_what_feel():
			return
		if self.ask_if_like():
			return
		if self.ask_which_better():
			return
		if self.ask_why_is():
			return
		if self.ask_most_question():
			return
		if self.check_exact_message_match():
			return
		if self.check_partial_message_match():
			return
		if self.check_topic_or_depth_match():
			return
		if self.check_single_term_match():
			return
		self.learn_new_response()
		self.give_random_or_question_response()

		return

