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
            text = reconizer.recognize_google(audio)
            text = text.lower()
            if "bob" in text:
                bob_text = text[text.index("bob") + len("bob"):].strip()
                print("bob detected!")
                print("askingAI:")
                ai.questionAI(bob_text)
            else:
                print("no bob detected but dedected: " + text)
    except speech_recognition.UnknownValueError:
        reconizer = speech_recognition.Recognizer()
        continue