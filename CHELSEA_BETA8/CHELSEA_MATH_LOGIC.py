import re
import math

def CHELSEA_Math_Logic(m1):

	word_to_symbol = { 'plus': '+', 'added to': '+', 'increased by': '+', 'minus': '-', 'subtracted by': '-', 'decreased by': '-', 'reduced by': '-', 'multiplied by': '*', 'times': '*', 'divided by': '/' }
	word_to_number = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30, 'fourty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90}

	message = m1.group(1)
	for word in word_to_symbol.keys():
		message = re.sub(word, word_to_symbol[word], message)
			
	m2 = re.search(r"pow\((.*), (.*)\)", message)
	if (m2):
		message = re.sub(r"(pow)", r"math.\1", message)
		
	m2 = re.search(r"(log|sin|cos|tan)\((.*)\)", message)
	if (m2):
		message = re.sub(r"(log|sin|cos|tan)", r"math.\1", message)

	m3 = 1
	while(m3):
		m3 = re.search(r"((([a-zA-Z]+\-?[a-zA-Z]*) thousand) (([a-zA-Z]+\-?[a-zA-Z]*) hundred) ([a-zA-Z]+\-?[a-zA-Z]*))", message)
		if (m3):
			if (m3.group(3).find('-') == -1):
				for word in word_to_number.keys():
					if (word == m3.group(3)):
						message = message.replace(m3.group(3) + ' thousand', '(' + str(word_to_number[word]) + '000 +', 1)
						break
			else:
				for word in word_to_number.keys():
					for word2 in word_to_number.keys():
						if (word + '-' + word2 == m3.group(3)):
							message = message.replace(m3.group(3) + ' thousand', '(' + str(word_to_number[word] + word_to_number[word2]) + '000 +', 1)
							break
			if (m3.group(5).find('-') == -1):
				for word in word_to_number.keys():
					if (word == m3.group(5)):
						message = message.replace(m3.group(5) + ' hundred', str(word_to_number[word]) + '00 +', 1)
						break
			else:
				for word in word_to_number.keys():
					for word2 in word_to_number.keys():
						if (word + '-' + word2 == m3.group(5)):
							message = message.replace(m3.group(5) + ' hundred', str(word_to_number[word] + word_to_number[word2]) + '00 +', 1)
							break
			if (m3.group(6).find('-') == -1):
				for word in word_to_number.keys():
					if (word == m3.group(6)):
						message = message.replace(m3.group(6), str(word_to_number[word]) + ')', 1)
						break
			else:
				for word in word_to_number.keys():
					for word2 in word_to_number.keys():
						if (word + '-' + word2 == m3.group(6)):
							message = message.replace(m3.group(6), str(word_to_number[word] + word_to_number[word2]) + ')', 1)
							break
	m3 = 1
	while(m3):
		m3 = re.search(r"((([a-zA-Z]+\-?[a-zA-Z]*) thousand) ([a-zA-Z]+\-?[a-zA-Z]*))", message)
		if (m3):
			if (m3.group(3).find('-') == -1):
				for word in word_to_number.keys():
					if (word == m3.group(3)):
						message = message.replace(m3.group(3) + ' thousand', '(' + str(word_to_number[word]) + '000 +', 1)
						break
			else:
				for word in word_to_number.keys():
					for word2 in word_to_number.keys():
						if (word + '-' + word2 == m3.group(3)):
							message = message.replace(m3.group(3) + ' thousand', '(' + str(word_to_number[word] + word_to_number[word2]) + '000 +', 1)
							break
			if (m3.group(4).find('-') == -1):
				for word in word_to_number.keys():
					if (word == m3.group(4)):
						message = message.replace(m3.group(4), str(word_to_number[word]) + ')', 1)
						break
			else:
				for word in word_to_number.keys():
					for word2 in word_to_number.keys():
						if (word + '-' + word2 == m3.group(4)):
							message = message.replace(m3.group(4), str(word_to_number[word] + word_to_number[word2]) + ')', 1)
							break
	m3 = 1
	while(m3):
		m3 = re.search(r"((([a-zA-Z]+\-?[a-zA-Z]*) thousand) (([a-zA-Z]+\-?[a-zA-Z]*) hundred))", message)
		if (m3):
			if (m3.group(3).find('-') == -1):
				for word in word_to_number.keys():
					if (word == m3.group(3)):
						message = message.replace(m3.group(3) + ' thousand', '(' + str(word_to_number[word]) + '000 +', 1)
						break
			else:
				for word in word_to_number.keys():
					for word2 in word_to_number.keys():
						if (word + '-' + word2 == m3.group(3)):
							message = message.replace(m3.group(3) + ' thousand', '(' + str(word_to_number[word] + word_to_number[word2]) + '000 +', 1)
							break
			if (m3.group(5).find('-') == -1):
				for word in word_to_number.keys():
					if (word == m3.group(5)):
						message = message.replace(m3.group(5) + ' hundred', str(word_to_number[word]) + '00)', 1)
						break
			else:
				for word in word_to_number.keys():
					for word2 in word_to_number.keys():
						if (word + '-' + word2 == m3.group(5)):
							message = message.replace(m3.group(5) + ' hundred', str(word_to_number[word] + word_to_number[word2]) + '00)', 1)
							break
	m3 = 1
	while(m3):
		m3 = re.search(r"((([a-zA-Z]+\-?[a-zA-Z]*) thousand))", message)
		if (m3):
			if (m3.group(3).find('-') == -1):
				for word in word_to_number.keys():
					if (word == m3.group(3)):
						message = message.replace(m3.group(3) + ' thousand', '(' + str(word_to_number[word]) + '000)', 1)
						break
			else:
				for word in word_to_number.keys():
					for word2 in word_to_number.keys():
						if (word + '-' + word2 == m3.group(3)):
							message = message.replace(m3.group(3) + ' thousand', '(' + str(word_to_number[word] + word_to_number[word2]) + '000)', 1)
							break
	m3 = 1
	while(m3):						
		m3 = re.search(r"((([a-zA-Z]+\-?[a-zA-Z]*) hundred) ([a-zA-Z]+\-?[a-zA-Z]*))", message)
		if (m3):
			if (m3.group(3).find('-') == -1):
				for word in word_to_number.keys():
					if (word == m3.group(3)):
						message = message.replace(m3.group(3) + ' hundred', '(' + str(word_to_number[word]) + '00 +', 1)
						break
			else:
				for word in word_to_number.keys():
					for word2 in word_to_number.keys():
						if (word + '-' + word2 == m3.group(3)):
							message = message.replace(m3.group(3) + ' hundred', '(' + str(word_to_number[word] + word_to_number[word2]) + '00 +', 1)
							break
			if (m3.group(4).find('-') == -1):
				for word in word_to_number.keys():
					if (word == m3.group(4)):
						message = message.replace(m3.group(4), str(word_to_number[word]) + ')', 1)
						break
			else:
				for word in word_to_number.keys():
					for word2 in word_to_number.keys():
						if (word + '-' + word2 == m3.group(4)):
							message = message.replace(m3.group(4), str(word_to_number[word] + word_to_number[word2]) + ')', 1)
							break
	m3 = 1
	while(m3):
		m3 = re.search(r"((([a-zA-Z]+\-?[a-zA-Z]*) hundred))", message)
		if (m3):
			if (m3.group(3).find('-') == -1):
				for word in word_to_number.keys():
					if (word == m3.group(3)):
						message = message.replace(m3.group(3) + ' hundred', '(' + str(word_to_number[word]) + '00)', 1)
						break
			else:
				for word in word_to_number.keys():
					for word2 in word_to_number.keys():
						if (word + '-' + word2 == m3.group(3)):
							message = message.replace(m3.group(3) + ' hundred', '(' + str(word_to_number[word] + word_to_number[word2]) + '00)', 1)
							break
	found = True
	while(found):
		found = False
		if (message.find('-') == -1):
			for word in word_to_number.keys():
				if (message.find(word) != -1):
					message = message.replace(word, '(' + str(word_to_number[word]) + ')', 1)
					found = True
					break
		else:
			for word in word_to_number.keys():
				for word2 in word_to_number.keys():
					if (message.find(word + '-' + word2) != -1):
						message = message.replace(word + '-' + word2, '(' + str(word_to_number[word] + word_to_number[word2]) + ')', 1)
						found = True
						break
	
	m2 = re.search(r"(pi|e)", message)
	if (m2):
		message = re.sub(r"(pi|e)", r"math.\1", message)
		
	m2 = re.search(r"(\(-?\d+\.?\d*\)) *(math\.pi|math\.e)", message)
	if (m2):
		message = re.sub(r"(\(-?\d+\.?\d*\)) *(math\.pi|math\.e)", r"\1 * \2", message)
		
	####### Keep in case of problems					
	#print("Debug1: " + message)
		
	try:
		test = eval(message)
		return (m1.group(1) + " equals " + str(test))
	except:
		return "Invalid expression!"
