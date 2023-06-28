from llama_cpp import Llama
import pyttsx3

# initilaize the ai model
engin = pyttsx3.init()
print("Initializing...")
# replace model path with the path to your model
llm = Llama(model_path="model/Model_V6.bin")
print("loaded models")

# ask the ai a question
def questionAI(question):
    print("asking...")
    asked = llm("Question: " + question + "  Answer:", stop=["Question:", "\n"], max_tokens=400)
    anser = asked['choices'][0]['text'] # type: ignore
    print(anser)
    if anser != "":
        engin.say(anser)
        engin.runAndWait()
    else:
        engin.say("sorry, ich kann dir nicht helfen")
    return(anser)
