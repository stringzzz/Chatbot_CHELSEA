#   chatbotCHELSEA, an AI chatbot with simulated emotions, math logic, and some self identity (Double Chat Main)
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

from chelsea_double_chat_class import chelsea_double_chat #type: ignore
import time

#Create chelsea object (CHELSEA is NOT an object! >:/)
chatbot_chelsea =  chelsea_double_chat("CHELSEA", "Dasha") #Input desired name in place of "CHELSEA"
chatbot_dasha =  chelsea_double_chat("Dasha", "CHELSEA")

#Input memory
print("Inputting memory...")
chatbot_chelsea.input_memory()
chatbot_dasha.input_memory()
print("Memory input complete!\n")

chatbot_chelsea.initial_greeting()

#Chat loop
chat_loop_counter = 0
while chat_loop_counter < 120:
	chatbot_dasha.chat(chatbot_chelsea.CHELSEA_previous_response)
	time.sleep(1)
	chatbot_chelsea.chat(chatbot_dasha.CHELSEA_previous_response)
	time.sleep(1)
	chat_loop_counter += 1

print("\nOutputting chatlogs...")
chatbot_chelsea.output_chatlogs()
print("Chatlogs output!")