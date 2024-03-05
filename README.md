This is Chatbot CHELSEA (CHat Emotion Logic SEnse Automator)


CHELSEA is directly based off of my other chatbot, OPHELIA.
Note that the Math Logic is still not fully tested, but everything else seems to be working the way it should.
If choosing to start with almost blank memory, copy the 3 files from 'starter_memory_files' to the directory of the python scripts.
If choosing to use my own chatbot's memory (Inherited from OPHELIA), copy the 3 files from 'my_memory_files' to the directory of the python scripts.


This is a video demonstration of talking to CHELSEA: https://youtu.be/p6TWgLfKwvE


Here is the algortihm for how CHELSEA deals with the user's message:




 Chatbot CHELSEA message handling algorithm 

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
 with them (Barely useful for now, will do something with this later)

 11. Add to running counts of all words in conversation
 Get topic(s) of conversation by the maximum value

 12. Check for an exact match of message, give linked response if so

 13. Check if user is asking What Question, give possible answer response if so

 14. Check if user asking for clarification on previous response,
 try to find matching message containing 2 or more words from
 previous response

 15. Check if asking what CHELSEA feels about ___,
 respond according to the tied emotions with the words in ___

 16. Check if asking 'do you like/dislike ___' question
 respond according to tied emotions to words in ___,
 agreement or disagreement depends on emotion and like/dislike
 word used

 17. Check if asking 'which is better, _1_ or _2_'
 Used emotions tied to the words to decide which CHELSEA likes better,
 or indifferent if neither is tied to happy overall

 18. Check if message matches as part of a message in memory,
 give linked reponse if so

 19. If certain  or greater messages and words in dictionary, PRNG to
 determine if attempting topic match. 

 20. If certain  or greater messages and words in dictionary, PRNG to
 determine if doing single term match. If so, coin flip to determine whether
 trying to match single word from message as part of message in memory,
 or single word associated with word from message. Repond with linked 
 response if so

 21. No match, overwrite old message in memory or learn brand new message/response pair

 22. Respond with random response from memory to keep conversation going
   

 
