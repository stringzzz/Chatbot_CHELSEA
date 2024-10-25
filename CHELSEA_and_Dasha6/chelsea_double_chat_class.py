#   chatbotCHELSEA, an AI chatbot with simulated emotions, math logic, and some self identity (chelsea double chat class)
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

#

import json
import os
import re
import random
from datetime import datetime

class chelsea_double_chat:

	Xchatlog = []

	def __init__(self, bot_name, other_bot_name):
		self.bot_name = bot_name
		self.username = other_bot_name
		self.user_self = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'uam': [], 'uamnot': []}
		self.dictionary = {}
		self.message_dict2 = {}
		self.chatlog = []
		self.nEmotions = ["happy", "angry", "sad", "afraid"]
		self.current_mood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
		self.pitches = {"happy": 95, "angry": 80, "sad": 90, "afraid": 99}
		self.speeds = {"happy": 150, "angry": 155, "sad": 135, "afraid": 155}
		self.user_message = " "
		self.chatlog_file = {"regular": f"double_chatlog.txt", "extended": f"double_Xchatlog.txt" }
		self.chelsea_self = {}
		self.agree = ['agreed, ', 'true ', 'yes ', 'i know ', 'true that, ', 'okay ', 'for sure, ', 'oh yeah, ', 'indeed, ', 'yep, ', 'you know it, ', 'correct, ']
		self.disagree = ['no, ', 'disagree, ', 'wrong, ', 'not true, ', 'false, ', 'nope, ', 'incorrect, ', 'i know otherwise, ', 'oh no, ', 'not valid, ', 'negative, ']
		self.topics = {}
		self.previous_pairs = []
		self.CHELSEA_previous_response = ""

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

	def input_memory(self):
		#Input memory
		self.input_dictionary()
		self.input_message_dictionary()

	#Output memory
	def chatlogOutput(self, chatlogFile, chatList):
		chatlog_file = open(f"{chatlogFile}", 'a')
		chatlog_file.write(f"\n\n\n{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}")
		for line in chatList:
			chatlog_file.write(f"\n{line}")
		chatlog_file.close()		
	
	def output_chatlogs(self):
		self.chatlogOutput(self.chatlog_file["regular"], self.chatlog)
		self.chatlogOutput(self.chatlog_file["extended"], chelsea_double_chat.Xchatlog)
		
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
		chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): I feel {self.current_mood["mood"]}")

	def getReplyMood(self):
		#Get the mood of the user reply by looking at the emotion counts gathered on it
		temp_dict = { 'happy': self.reply_mood['happy'], 'angry': self.reply_mood['angry'], 'sad': self.reply_mood['sad'], 'afraid': self.reply_mood['afraid'] }
		self.reply_mood["mood"] = self.getMood2(temp_dict, True)
		chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): {self.username} seems to be {self.reply_mood["mood"]}")

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
		chelsea_double_chat.Xchatlog.append(f"{self.bot_name}: {botResponse}")
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

	def get_user_reply(self, previous_reply):
		#User reply
		self.user_message = previous_reply
		self.chatlog.append(f"{self.username}: {self.user_message}")
		chelsea_double_chat.Xchatlog.append(f"\n{self.username}: {self.user_message}")

	def filter_user_reply(self):
		#Filter certain chars from userMessage
		self.user_message = re.sub(r"([^a-z0-9, \"'\-\?!])", '', self.user_message)

	def get_exclaim_count(self):
		#Detect exclamation points at end of user_message to add emotional emphasis (Multiply counts by (self.exclaim_count + 1))
		self.exclaim_count = 1
		exclaim_match = re.search(r"(!+)$", self.user_message)
		if (exclaim_match):
			chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Exclamation detected, exclaim count: {len(exclaim_match.group(1))}")
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
		chelsea_double_chat.Xchatlog.append(f"Word emotions in previous reply: {self.word_emotions}")

	def detect_unkown_words(self):
		#Mark unknown words in the emotion dictionary according to the overall mood of the user reply
		if len(self.unknown_words) > 0:
			chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Unknown words detected: {self.unknown_words}")
			for word in self.unknown_words:
				self.dictionary[word] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 0, 'associated': {}}
				self.dictionary[word]['emotion'] = self.reply_mood["mood"] 
			chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Learned unknown words as '{self.reply_mood["mood"]}' words.")
			for word in self.unknown_words:
				self.unanswered_questions[f"what is/are {word}?"] = ''
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Learned unknown words as unanswered questions")

	def add_to_word_counts(self):
		#Add to counts for each word
		for word in self.message_words:
			try:
				if (self.dictionary[word]['emotion'] == 'permanent neutral'):
					continue
			except(KeyError):
				continue
			self.dictionary[word][self.reply_mood["mood"]] += 1  * self.exclaim_count
			temp_dict = { 'happy': self.dictionary[word]['happy'], 'angry': self.dictionary[word]['angry'], 'sad': self.dictionary[word]['sad'], 'afraid': self.dictionary[word]['afraid'] }
			word_emotion = self.getMood2(temp_dict, False)
			if (word_emotion != self.dictionary[word]['emotion']):
				self.dictionary[word]['emotion'] = word_emotion
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Switched emotion of word '{word}' to {word_emotion}")

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
					chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Added to count of association of {word} and {word2}")
					continue
				except(KeyError):
					self.dictionary[word]['associated'][word2] = 1
					chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Learned association of {word} and {word2}")
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
			chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Current topic(s) is/are {" & ".join(self.current_topics)}")

	def add_to_previous_pairs(self):
		#Add to previous pairs (For depth words)
		temp_pair = []
		temp_pair.append(self.CHELSEA_previous_response)
		temp_pair.append(self.user_message)
		self.previous_pairs.append(temp_pair)
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
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Found depth words: {" ".join(self.depth_words)}")

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
					chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): WH-Q question match found in values.")
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
					chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): WH-Q question match found in keys.")
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
						chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Previous words meaning match found for: {" & ".join(match_words)}")
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
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Feel nothing.")
				self.CHELSEA_previous_response = self.botReply(f"i feel nothing about {feel_about_match.group(1)}")
				return True
			else:
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Have emotion to answer question.")
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
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Like or dislike match found.")
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
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Neither like or dislike")
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
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Found like both, determining which more.")
				happy_count1 = 0
				happy_count2 = 0
				for word in better_words1:
					happy_count1 += self.dictionary[word]['happy']
				for word in better_words2:
					happy_count2 += self.dictionary[word]['happy']
				if (happy_count1 > happy_count2):
					chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Determined I like first option better.")
					self.CHELSEA_previous_response = self.botReply(f"i like both, but {better_match.group(1)} most")
					return True
				elif (happy_count2 > happy_count1):
					chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Determined I like second option better.")
					self.CHELSEA_previous_response = self.botReply(f"i like both, but {better_match.group(2)} most")
					return True
				else:	
					chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Determined I like both equally.")
					self.CHELSEA_previous_response = self.botReply(f"i like both {better_match.group(1)} & {better_match.group(2)} the same")
					return True
			elif (better_emotion1 == 'happy' and better_emotion2 != 'happy'):
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Found like first.")
				self.CHELSEA_previous_response = self.botReply(f"i like {better_match.group(1)} better ")
				return True
			elif (better_emotion1 != 'happy' and better_emotion2 == 'happy'):
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Found like second.")
				self.CHELSEA_previous_response = self.botReply(f"i like {better_match.group(2)} better ")
				return True
			elif (better_emotion1 != 'happy' and better_emotion2 != 'happy'):
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Like neither.")
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
							chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Possible answer to 'why is' question match found in values for: {" ".join(whyis_words)}")
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
							chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Possible answer to 'why is' question match found in keys for: {" ".join(whyis_words)}")
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
			chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Most {temp_emotion} match found.")
			self.CHELSEA_previous_response = self.botReply(f"{max1[0]} makes me most {temp_emotion}")
			return True
		elif (len(max1) > 1):
			chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Most {temp_emotion} matches found.")
			self.CHELSEA_previous_response = self.botReply(f"{random.choice(max1)} is one of many that makes me most {temp_emotion}")
			return True
		return False
	
	def check_exact_message_match(self):
		#Check for exact match under current mood
		try:
			temp_message = self.message_dict2[self.current_mood["mood"]][self.user_message]
			if len(temp_message) == 1:
				for pair in self.previous_pairs:
					if (temp_message[0] == pair[0] or temp_message[0] == pair[1]):
						chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Duplicate message found, gave random response to avoid loop.")	
						self.CHELSEA_previous_response = self.botReply(random.choice(random.choice(list(self.message_dict2[self.current_mood["mood"]].values()))))
						return True
			chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Exact message match found.")
			self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][self.user_message]))
			return True
		except(KeyError):
			return False
		
	def check_partial_message_match(self):
		#Check for partial match under current mood
		response_made = False
		for message in self.temp_message_keys:
			if message.find(self.user_message) != -1:
				chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Partial message match found.")
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
						chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Depth match found for: {" ".join(matched_words)}")
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
						chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Topic match found.")
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
									chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Single term match found for term: {word}")
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
							chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Single term associated match found for associated term: {highest_associated_chosen}")
							self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][message]))
							response_made = True
							break
					if response_made:
						break
				if response_made:
					return True
		return False

	def give_random_or_question_response(self):
		#Give random response from current mood
		chelsea_double_chat.Xchatlog.append(f"{self.bot_name} (Thinking): Gave random response.")	
		self.CHELSEA_previous_response = self.botReply(random.choice(random.choice(list(self.message_dict2[self.current_mood["mood"]].values()))))

	def chat(self, previous_reply):
		#FLAG
		self.get_user_reply(previous_reply)

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
		self.give_random_or_question_response()

		return

