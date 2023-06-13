import sys, os, time, random, string
from gtts import gTTS
from chatgpt_wrapper import ChatGPT

# this is called from a program so just take the first arg string as the phrase
ask_phrase = sys.argv[1]
print('asking chatgpt:')
print(ask_phrase)
# acknowlege the command was heard
os.system("afplay response.mp3")
bot = ChatGPT()
response = bot.ask(ask_phrase)
print('chatgpt response:')
print(response)
# random files get randomly made and delted
filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".mp3"
commandname = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".sh"
mp3_file = gTTS(text=response, lang='en', slow=False, tld='ie')
# someone wanna look up how to stream play this file in python?
mp3_file.save(filename)
# write the play command followed by delete to bash then finally delete itself
# os commands written for OSX, subsitute appropriate bash
f = open(commandname, "w")
f.write("#!/bin/bash \n")
f.write("afplay " + filename +"\n")
f.write("rm " + filename +"\n")
f.write("rm " + commandname+"\n")
f.close()
os.system("bash " + commandname)