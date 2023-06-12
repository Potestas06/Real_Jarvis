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
            text = reconizer.recognize_whisper(audio, language="english")
            if "günter" in text:
                günter_text = text[text.index("günter") + len("günter"):].strip()
                print("günter detected! with text: " + günter_text)
                if "stop" in günter_text:
                    running = False
                    print("Program stopped.")
                else:
                    print("===================================")
                    print("askingAI:")
                    ai.questionAI(günter_text)
                    print("===================================")
                    print("listening...")
            else:
                print("no günter detected! with text: " + text)
                print("listening...")
    except speech_recognition.UnknownValueError:
        reconizer = speech_recognition.Recognizer()
        continue