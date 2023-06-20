import threading
import tkinter as tk
import speech_recognition
import ai
import pyaudio
import argparse
import os
import struct
import wave
import pvporcupine
import pvrecorder

recognizer = speech_recognition.Recognizer()


class Assistant():
    # init
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.recognizer = speech_recognition.Recognizer()
        self.ai = ai
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
        def get_next_audio_frame():
            pass
        print("listening...")
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic)
                    audio = self.recognizer.listen(mic)
                    engine = pvporcupine.create(access_key='os.getenv("APIKEY")', keywords=['picovoice', 'bumblebee'])
                    audio_frame = get_next_audio_frame()
                    keyword_index = engine.process(audio_frame)
                    if keyword_index == 0:
                        print("Hotword Detected")
                        self.answer_label.config(fg="red")
                        try:
                            audio = self.recognizer.listen(mic)
                            text = self.recognizer.recognize_whisper(audio, language="german")
                            self.text_label.config(text="asked: " +text)
                            if text == "stop":
                                self.root.destroy()
                                break
                            elif text is not None:
                                self.answer_label.config(fg="black")
                                self.answer_label.config(text="⌛")
                                anser = ai.questionAI(text)
                                self.answer_label.config(text="anser: " + anser)
                                self.answer_label.config(text="🤖")
                        except speech_recognition.UnknownValueError:
                            print("UnknownValueError at whisper")
                            self.recognizer = speech_recognition.Recognizer()
                            continue
                    elif engine is not None:
                        engine.delete()
            except speech_recognition.UnknownValueError:
                print("UnknownValueError at wakeword")
                self.recognizer = speech_recognition.Recognizer()
                continue
            except Exception as e:
                print("Error at wakeword: " + str(e))
                continue

Assistant()
