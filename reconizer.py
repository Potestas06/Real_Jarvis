import speech_recognition
import os
import ai

running = True
reconizer = speech_recognition.Recognizer()
print("listening...")

def getAnser(günter_text):
    if "stop" in günter_text:
        running = False
        print("Program stopped.")
    else:
        print("askingAI:")
        ai.questionAI(günter_text)
        print("listening...")

while running:
    try:
        with speech_recognition.Microphone() as mic:
            reconizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = reconizer.listen(mic)
            text = reconizer.recognize_google(audio, language="de-DE")
            text = text.lower()
            if "günter" in text:
                günter_text = text[text.index("günter") + len("günter"):].strip()
                print("günter detected! with text: " + günter_text)
                getAnser(günter_text)
            else:
                print("no günter detected but detected: " + text)
                print("listening...")
    except speech_recognition.UnknownValueError:
        reconizer = speech_recognition.Recognizer()
        continue