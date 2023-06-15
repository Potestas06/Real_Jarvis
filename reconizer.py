import threading
import tkinter as tk
import speech_recognition
import ai

recognizer = speech_recognition.Recognizer()


class Assistant():
    # init
    def __init__(self):
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
        print("listening...")
        while True:
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = self.recognizer.listen(mic)
                text = self.recognizer.recognize_google(audio, language="de-DE")
                text = text.lower()
                print(text)
                self.text_label.config(text="asked: " + text)
                if "günther" in text or "günter" in text:
                    self.answer_label.config(fg="red")
                    try:
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_whisper(audio, language="german")
                        self.text_label.config(text="asked: " +text)
                        if text == "stop":
                            self.root.destroy()
                        elif text is not None:
                            self.answer_label.config(fg="black")
                            self.answer_label.config(text="⌛")
                            anser = ai.questionAI(text)
                            self.answer_label.config(text="anser: " + anser)
                            self.answer_label.config(text="🤖")
                    except speech_recognition.UnknownValueError:
                        print("UnknownValueError")
                        self.recognizer = speech_recognition.Recognizer()
                        continue
Assistant()

