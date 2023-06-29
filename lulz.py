import speech_recognition as sr
from speech_recognition.exceptions import WaitTimeoutError
import os
from threading import Thread
from queue import Queue

PHRASE_MIN_SIZE = 20
VOICE_BOT_NAME = "Daphne"

r = sr.Recognizer()
audio_queue = Queue()

def process_phrase(phrase):
    print('I heard you say:')
    print(phrase)
    phrase = phrase.lower()
    if len(phrase) > PHRASE_MIN_SIZE and 'hey' in phrase and VOICE_BOT_NAME.lower() in phrase:
        chatgpt_phrase = phrase.partition(VOICE_BOT_NAME.lower())[2]
        # chatgpt wants its own process since it's a headless browser so just bash the thing
        os.system('.env/bin/python3 ask_chat.py "' + chatgpt_phrase +'"' )

def recognize_worker():
    # this runs in a background thread
    while True:
        audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
        if audio is None: break  # stop processing if the main thread is done
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # parse the current phrase
            current_phrase = r.recognize_whisper(audio, language="english")
            process_phrase(current_phrase) 
        except sr.UnknownValueError:
            print("Whisper could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Whisper")

        audio_queue.task_done()  # mark the audio processing job as completed in the queue

print('Loading...')
# start a new thread to recognize audio, while this thread focuses on listening
recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()
with sr.Microphone() as source:
    try:
        while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            # listen in 5 second chunks and if it times out simply pass through
            try:
                audio_queue.put(r.listen(source, 5, 5))
            except WaitTimeoutError as e:
                pass
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass
