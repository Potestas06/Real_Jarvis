from llama_cpp import Llama
import pyttsx3

engin = pyttsx3.init()
print("Initializing...")
llm = Llama(model_path="model\ggml-model-q4_1.bin")
print("loaded models")

def questionAI(question):
    print("asking...")
    asked = llm("Question: " + question + "  Answer:", stop=["Question:", "\n"], max_tokens=400)
    anser = asked['choices'][0]['text']
    print(anser)
    engin.say(anser)
    engin.runAndWait()
    return
