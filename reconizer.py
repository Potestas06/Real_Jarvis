import speech_recognition
import ai


running = True
reconizer = speech_recognition.Recognizer()

def handling():
    print("askingAI:")
    ai.questionAI(günter_text)
    print("listening...")

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
                if "stop" in günter_text:
                    running = False
                    print("Program stopped.")
                else:
                    handling()
            else:
                print("no günter detected but detected: " + text)
                print("listening...")
    # Do not delete this except block. It is needed to keep the program running.
    except speech_recognition.UnknownValueError:
        reconizer = speech_recognition.Recognizer()
        continue