import threading
import tkinter as tk
import speech_recognition
import pyaudio
import pyttsx3
import os
from dotenv import load_dotenv
import struct
import pvporcupine
import openQuest

previous = []

load_dotenv()
recognizer = speech_recognition.Recognizer()
url = "https://api.openai.com/v1/chat/completions"
APIKEY = os.getenv("APIKEY")
OPENAIKEY = os.getenv("OPENAIKEY")


class Assistant():
    # init
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.handle = pvporcupine.create(access_key=APIKEY, keywords=['computer'])
        self.voice = pyttsx3.init()
        self.audio = pyaudio.PyAudio()
        self.recognizer = speech_recognition.Recognizer()
        self.root = tk.Tk()
        self.root.title("Günther")
        self.text_label = tk.Label(font=("Arial",), fg="black")
        self.answer_label = tk.Label(font=("Arial",), fg="black")
        self.robot_label = tk.Label(text="🤖", font=("Arial", 120, "bold"), fg="black")
        self.robot_label.pack()
        self.text_label.pack()
        self.answer_label.pack()
        threading.Thread(target=self.Wakeword).start()
        self.root.mainloop()



    # lisens for the wakeword and then starts the question ai
    def Wakeword(self):

        stream = self.audio.open(
            rate=self.handle.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.handle.frame_length
        )
        print("listening...")
        while True:
            try:
                pcm = stream.read(self.handle.frame_length)
                pcm = struct.unpack_from("h" * self.handle.frame_length, pcm)

                keyword_index = self.handle.process(pcm)

                if keyword_index >= 0:
                    print("Wake word detected!")
                    with speech_recognition.Microphone() as mic:
                        self.recognizer.adjust_for_ambient_noise(mic)
                        audio = self.recognizer.listen(mic)
                        print("listening...")
                        self.robot_label.config(fg="red")
                        try:
                            audio = self.recognizer.listen(mic)
                            text = self.recognizer.recognize_whisper(audio)
                            self.text_label.config(text="asked: " +text)
                            if text == "stop":
                                self.root.destroy()
                                break
                            elif text is not None:
                                self.robot_label.config(fg="black")
                                self.robot_label.config(text="⌛")
                                anser = openQuest.request(text)
                                self.answer_label.config(text=f"anser: {anser}")
                                self.robot_label.config(text="🤖")
                                self.voice.say(anser)
                                self.voice.runAndWait()
                        except speech_recognition.UnknownValueError:
                            print("UnknownValueError at whisper")
                            self.recognizer = speech_recognition.Recognizer()
                            continue
            except speech_recognition.UnknownValueError:
                print("UnknownValueError at speech_recognition")
                self.recognizer = speech_recognition.Recognizer()
                continue
            except Exception as e:
                print("Error at wakeword: " + str(e))
                continue

Assistant()
