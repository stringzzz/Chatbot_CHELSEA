#If you have been using the previous 'BETA12' version, use this script with your memory files to produce
# The new 'bigramDictionary.json' memory file for the 'BETA13' version

import json
import re

message_dict2 = {}
with open("messageDictionary2.json", 'r') as message_dictionary_file:
    message_dict2 = json.load(message_dictionary_file)

dictionary = {}
with open("dictionary.json", 'r') as dictionary_file:
	dictionary = json.load(dictionary_file)

nEmotions = ["happy", "angry", "sad", "afraid"]

bigram_dictionary = {}

for emotion in nEmotions:
    messages = [message for message in message_dict2[emotion].keys()]
    for response in message_dict2[emotion].values():
        messages.extend(response)
    for message in messages:
         message_words = (re.sub(r"([^a-z0-9 '\-])", '', message)).split(" ")
         for n in range(len(message_words)):
              if n != len(message_words) - 1:
                    try:
                        bigram_dictionary[f"{message_words[n]} {message_words[n+1]}"]["seen"] += 1
                    except(KeyError):
                        try:
                            bigram_dictionary[f"{message_words[n]} {message_words[n+1]}"] = {"seen": 1, "emotions": [dictionary[message_words[n]]["emotion"], dictionary[message_words[n+1]]["emotion"]]}
                        except(KeyError):
                             continue

with open("bigramDictionary.json", 'w') as bigram_dictionary_file:
     json.dump(bigram_dictionary, bigram_dictionary_file, indent=4)