import sys, os, time, random, string
from gtts import gTTS
from chatgpt_wrapper import ChatGPT

# this is called from a program so just take the first arg string as the phrase
# since this chatgpt binding is dependent on a headless browser session it has to be its own process
ask_phrase = sys.argv[1]
print('asking chatgpt:')
print(ask_phrase)
# acknowlege the command was heard
os.system("say \"Just a moment\"")
bot = ChatGPT()
response = bot.ask(ask_phrase)
print('chatgpt response:')
print(response)
os.system("say \"" + response + "\"")