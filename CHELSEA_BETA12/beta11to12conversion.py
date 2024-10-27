#Run in same directory as memory files to create the converted 'unanswered_questions2.json' file
#For converting memory from BETA11 to BETA12

import re
import json

print("Creating converted memory file 'unanswered_questions2.json'...")

unanswered_questions1 = {}
with open("unanswered_questions.json", 'r') as unanswered_questions_file:
	unanswered_questions1 = json.load(unanswered_questions_file)

unanswered_questions2 = {"what": unanswered_questions1, "why is": {}, "why are": {}}

with open("messageDictionary2.json", 'r') as message_dictionary_file:
    message_dict2 = json.load(message_dictionary_file)

#horrible inefficiency :/
messages = [message for message in message_dict2["happy"].keys()]
for response in message_dict2["happy"].values():
    messages.extend(response)
for message in messages:
    if not(re.search(r'^why', message)):
        m1 = re.search(r'([a-z ,\'\-]+) (is|are) ([a-z ,\'\-]+)', message)
        is_match1 = ""
        is_are = ""
        is_match2 = ""
        if m1:
            is_match1 = m1.group(1)
            is_are = m1.group(2)
            is_match2 = m1.group(3)
        else:
            continue
        if not(re.search(r'(because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)', is_match2)):
            because_match_found = False
            for message2 in messages:
                if not(re.search(r'^why', message2)):
                    if message2.find(message) != -1:
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

                unanswered_questions2[f"why {is_are}"][f"why {is_are} {is_match1} {is_match2}?".replace("  ", " ")] = ""
        else:
            continue

#print(unanswered_questions2["why is"])
#print(unanswered_questions2["why are"])
with open("unanswered_questions2.json", 'w') as unanswered_questions_file:
    json.dump(unanswered_questions2, unanswered_questions_file, indent=4)

print("Memory conversion complete.")