from llama_cpp import Llama
import json
import pyttsx3

engin = pyttsx3.init()
print("Initializing...")
llm = Llama(model_path="./model/ggml-vicuna-13b-4bit-rev1.bin")
print("loaded models")

def questionAI(question):
    print("asking...")
    asked = llm("Question: " + question + "  Answer:", stop=["Question:", "\n"], max_tokens=200)
    anser = asked['choices'][0]['text']
    print(anser)
    engin.say(anser)
    engin.runAndWait()
    return


