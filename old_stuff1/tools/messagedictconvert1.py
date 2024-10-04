#Convert messageDictionary from Version 0.12 to 0.13+

import json

message_dict = {}
with open("messageDictionary.json", 'r') as message_dictionary_file:
	message_dict = json.load(message_dictionary_file)
	
message_dict2 = {}
nEmotions = ["happy", "angry", "sad", "afraid"]
for emotion in nEmotions:
	message_dict2[emotion] = {}
	for key in message_dict[emotion].keys():
		message_dict2[emotion][key] = []
		message_dict2[emotion][key].append(message_dict[emotion][key])	

#Output message/response dictionary
with open("messageDictionary2.json", 'w') as message_dictionary_file:
	json.dump(message_dict2, message_dictionary_file)

