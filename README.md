This is Chatbot CHELSEA (CHat Emotion Logic SEnse Automator)

###################################################

10-03-2024
After spending quite some time away from this project I've decided to start working on CHELSEA again. I'm going much deeper into learning the Python language, so my plan is to first clean up CHELSEA a bit, then
begin finding ways to add more features to make CHELSEA more intelligent and capable. I've dropped the animated avatar code for now, only because I would have to learn Blender to make a better one, and I
don't really want to learn that just for that one purpose. 

This is a video demonstration of talking to CHELSEA: https://www.youtube.com/watch?v=eCNmKNLkOZ8

And here is a demonstration of CHELSEA talking to a copy of herself: https://www.youtube.com/watch?v=XYLXGI4dyTo

###################################################

CHELSEA is directly based off of my other chatbot, OPHELIA.
Note that the Math Logic is still not fully tested, but everything else seems to be working the way it should.
If choosing to start with almost blank memory, copy the 3 files from 'starter_memory_files' to the directory of the python scripts.
If choosing to use my own chatbot's memory (Inherited from OPHELIA), copy the 3 files from 'my_memory_files' to the directory of the python scripts.

IMPORTANT: If you are viewing this repo for the first time and want to jump into working with this chatbot, it would be best to just download the highest 'BETA#' version directory, it has everything you need and is current. Some things in the highest version may still be experimental, so there may be some uncaught bugs, just to warn you.

IMPORTANTER!!!: To save what CHELSEA just learned from chat, enter '//exit' without the single quotes to exit the chat and retain her memory.

Here is the algortihm for how CHELSEA deals with the user's message:


#############################################

#Chatbot CHELSEA message handling algorithm 

#############################################

 1. User enters message

 2. Detect if math question, use external script to handle
 and give solution to question (Highly experimental)

 3. Detect if asking what she is or is not

 4. Detect if asking what user is or is not

 5. Detect if telling what she is or is not, learn accordingly
 Also detect if contradiction to what she already knows

 6. Detect if current user describing what they are or are not
 Learn accordingly, detect if contradiction to what she already knows

 7. Split message into words, remove punctuation
 Determine mood of reply, add counts to CHELSEA mood as well

 8. Mark unkown words in message

 9. Add to counts for each word, adjust the tied emotion to them accordingly

 10. Take each word and associate all other (non-neutral) words in message 
 with them (Either start or add to count)
 Comes into play in matching single associated word with highest count, or select
 one randomly from list of highest

 11. Identify bigrams in the user message and mark as new or add to counts if
 already seen

 12. Add to running counts of all words in conversation
 Get topic(s) of conversation by the maximum value

 13. Keep track of matching words from 3 previous message/response pairs
 Get list of these 'depth words'

 14. Mark unknown words in dictionary for 'what is/are __' unanswered questions

 15. Check for answer to previous 'what is/are' question

 16. Check for answer to previous 'why is/are' question

 17. Check if user is asking What Question, give possible answer response if so

 18. Check if user asking for clarification on previous response,
 try to find matching message containing 2 or more words from
 previous response

 19. Check if asking what CHELSEA feels about ___,
 respond according to the tied emotions with the words in ___

 20. Check if asking 'do you like/dislike ___' question
 respond according to tied emotions to words in ___,
 agreement or disagreement depends on emotion and like/dislike
 word used

 21. Check if asking 'which is better, _1_ or _2_'
 Used emotions tied to the words to decide which CHELSEA likes better,
 or indifferent if neither is tied to happy overall

 22. Check if asking 'why is' question, try to find match involving
 'because' words a possible answer
 
 23. Check for 'most __emotion__' question, respond with biggest word(s) tied to emotion

 24. Check for an exact match of message, give linked response if so

 25. Check if message matches as part of a message in memory,
 give linked reponse if so

 26. If current topics > 0 and prng 1/6, search for chain of bigrams starting with randomly 
 Chosen topic or depth word (Coin flip), chain either forward or reverse (Coin flip)

 27. If certain  or greater messages and words in dictionary, PRNG to
 determine if attempting topic match, or 'depth match' (Coin flip between two) 

 28. If certain  or greater messages and words in dictionary, PRNG to
 determine if doing single term match. If so, coin flip to determine whether
 trying to match single word from message as part of message in memory,
 or single word associated with word from message. Repond with linked 
 response if so

 29. No match, add response to list in message memory or learn brand new message/response pair

 30. 1/6 chance asking unanswered question, else respond with random response from memory to keep conversation going
  
    
######################################## 
  
