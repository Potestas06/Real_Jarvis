import speech_recognition
import ai

running = True
reconizer = speech_recognition.Recognizer()

print("===================================")
print("Reconizer.py Output")
print("===================================")

print("listening...")
while running:
    try:
        with speech_recognition.Microphone() as source:
            audio = reconizer.listen(source)
            text = reconizer.recognize_whisper(audio, language="german")
            if "Günther" in text:
                Günther_text = text[text.index("Günther") + len("Günther"):].strip()
                print("Günther detected! with text: " + Günther_text)
                if "stop" in Günther_text:
                    running = False
                    print("Program stopped.")
                else:
                    print("===================================")
                    print("askingAI:")
                    ai.questionAI(Günther_text)
                    print("===================================")
                    print("listening...")
            else:
                print("no Günther detected! with text: " + text)
                print("listening...")
    except speech_recognition.UnknownValueError:
        print("reconizer error!")
        reconizer = speech_recognition.Recognizer()
        print("listening...")
        continue