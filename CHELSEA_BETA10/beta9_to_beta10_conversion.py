import json
import re

dictionary = {}
message_dict2 = {}
nEmotions = ["happy", "angry", "sad", "afraid"]
unanswered_questions = {}
isare = ['is', 'are']

with open("dictionary.json", 'r') as dictionary_file:
	dictionary = json.load(dictionary_file)
	
with open("messageDictionary2.json", 'r') as message_dictionary_file:
	message_dict2 = json.load(message_dictionary_file)
	
words = list(dictionary.keys())
for word in words:
	if (dictionary[word]['emotion'] == 'permanent neutral'):
		continue
	match_found = False
	for emotion in nEmotions:
		temp_message_keys = list(message_dict2[emotion].keys())
		temp_message_values = list(message_dict2[emotion].values())
		
		#Check values
		for values in temp_message_values:
			for message in values:
				for isare_word in isare:
					partial_message = word + ' ' + isare_word
					if message.find(partial_message) == -1:
						unanswered_questions["what is/are " + word + '?'] = ''
						match_found = True
						break
				if match_found:
					break
			if match_found:
				break
		if match_found:
			break
			
		#Check keys
		for values in temp_message_keys:
			for message in values:
				for isare_word in isare:
					partial_message = word + ' ' + isare_word
					if message.find(partial_message) == -1:
						unanswered_questions["what is/are " + word + '?'] = ''
						match_found = True
						break
				if match_found:
					break
			if match_found:
				break
			
#Output unanswered questions dictionary
with open("unanswered_questions.json", 'w') as unanswered_questions_file:
	json.dump(unanswered_questions, unanswered_questions_file)
	
print(len(unanswered_questions.keys()))
