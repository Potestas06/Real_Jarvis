import speech_recognition
import pyttsx3

reconizer = speech_recognition.Recognizer()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            reconizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = reconizer.listen(mic)
            text = reconizer.recognize_google(audio)
            text = text.lower()
            print(f"Recognized {text}")
    except speech_recognition.UnknownValueError:
        reconizer = speech_recognition.Recognizer()
        continue