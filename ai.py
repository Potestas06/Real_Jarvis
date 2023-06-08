from llama_cpp import Llama
import json

print("Initializing...")
llm = Llama(model_path="./model/ggml-vicuna-13b-4bit-rev1.bin")
print("loaded models")

def questionAI(question):
    print("asking...")
    asked = llm("Question: " + question + "  Answer:",
                max_tokens = 100,
                stop = ["\n", "Question:", "Answer:", "Q:", "A:"])
    anser = json.dumps(asked, indent=4, sort_keys=True)
    print(asked['choices'][0]['text'])