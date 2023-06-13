import speech_recognition as sr
import json, base64, pyaudio
from threading import Thread
from queue import Queue
from pygame import mixer
import time

r = sr.Recognizer()
audio_queue = Queue()


def process_phrase(phrase):
    print(phrase)
    phrase = phrase.lower()
    if 'amanda' in phrase and 'dream' in phrase:
        mixer.init()
        mixer.music.load("dreams.mp3")
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)

    if 'testing' in phrase and 'hello' in phrase:
        print('ROBOT REPONSE: hello')

def recognize_worker():
    # this runs in a background thread
    while True:
        audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
        if audio is None: break  # stop processing if the main thread is done

        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            current_phrase = r.recognize_whisper(audio, language="english")
            process_phrase(current_phrase) 
        except sr.UnknownValueError:
            print("Whisper could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Whisper")

        audio_queue.task_done()  # mark the audio processing job as completed in the queue


# start a new thread to recognize audio, while this thread focuses on listening
recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()
with sr.Microphone() as source:
    try:
        while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            audio_queue.put(r.listen(source, 10, 10))
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass

audio_queue.join()  # block until all current audio processing jobs are done
audio_queue.put(None)  # tell the recognize_thread to stop
recognize_thread.join()  # wait for the recognize_thread to actually stop
