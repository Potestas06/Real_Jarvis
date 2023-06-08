import speech_recognition
import pyttsx3
import ai

reconizer = speech_recognition.Recognizer()
print("listening...")
while True:
    try:
        with speech_recognition.Microphone() as mic:
            reconizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = reconizer.listen(mic)
            text = reconizer.recognize_google(audio, language="de-DE")
            text = text.lower()
            if "günter" in text:
                günter_text = text[text.index("günter") + len("günter"):].strip()
                print("günter detected! with text: " + günter_text)
                print("askingAI:")
                ai.questionAI(günter_text)
                print("listening...")
            else:
                print("no günter detected but dedected: " + text)
                print("listening...")
    except speech_recognition.UnknownValueError:
        reconizer = speech_recognition.Recognizer()
        continue