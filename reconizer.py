import sys
import threading
import tkinter as tk

import speech_recognition
import ai

reconizer = speech_recognition.Recognizer()


class Assistant():

    def __init__(self):
        self.reconizer = speech_recognition.Recognizer()
        self.ai = ai
        self.root = tk.Tk()
        self.root.title("Günther")
        self.text = tk.Label( font=("Arial",), fg="black")
        self.anser = tk.Label( font=("Arial",), fg="black")
        self.label = tk.Label(text="🤖", font=("Arial", 120, "bold"), fg="black")
        self.label.pack()
        self.text.pack()
        self.anser.pack()
        threading.Thread(target=self.Wakeword).start()
        self.root.mainloop()


    def Wakeword(self):
        print("listening...")
        while True:
            with speech_recognition.Microphone() as mic:
                self.reconizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = self.reconizer.listen(mic)
                text = self.reconizer.recognize_google(audio, language="de-DE")
                text = text.lower()
                print(text)
                self.text.config(text="asked: " + text)
                if "günther" in text or "günter" in text:
                    self.label.config(fg="red")
                    try:
                        audio = self.reconizer.listen(mic)
                        text = self.reconizer.recognize_whisper(audio, language="german")
                        self.text.config(text="asked: " +text)
                        if text == "stop":
                            self.root.destroy()
                        elif text is not None:
                            self.label.config(fg="black")
                            self.label.config(text="⌛")
                            anser = ai.questionAI(text)
                            self.anser.config(text="anser: " + anser)
                            self.label.config(text="🤖")
                    except speech_recognition.UnknownValueError:
                        print("UnknownValueError")
                        self.reconizer = speech_recognition.Recognizer()
                        continue
Assistant()

