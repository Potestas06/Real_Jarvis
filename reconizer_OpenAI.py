import threading
import tkinter as tk
import speech_recognition
import pyaudio
import pyttsx3
import os
import openai
from dotenv import load_dotenv
import functions
import json
import struct
import pvporcupine

previous = []

load_dotenv()
recognizer = speech_recognition.Recognizer()
openai.api_key = os.getenv("OPENAIKEY")

APIKEY = os.getenv("APIKEY")


class Assistant():
    # init
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.handle = pvporcupine.create(access_key=APIKEY, keywords=['computer'])
        self.voice = pyttsx3.init()
        self.audio = pyaudio.PyAudio()
        self.recognizer = speech_recognition.Recognizer()
        self.root = tk.Tk()
        self.root.title("Günther")
        self.text_label = tk.Label(font=("Arial",), fg="black")
        self.answer_label = tk.Label(font=("Arial",), fg="black")
        self.robot_label = tk.Label(text="🤖", font=("Arial", 120, "bold"), fg="black")
        self.robot_label.pack()
        self.text_label.pack()
        self.answer_label.pack()
        threading.Thread(target=self.Wakeword).start()
        self.root.mainloop()



    # lisens for the wakeword and then starts the question ai
    def Wakeword(self):
        def request(text):
            message = {
                "role": "user",
                "content": text
            }
            messages = [message] + [{"role": msg["role"], "content": msg["content"]} for msg in previous]

            function_list = [
                {
                    "name": "check_weather",
                    "description": "Get the current weather from a city.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The city to get the weather from, e.g. London"
                            }
                        },
                        "required": ["city"]
                    }
                },
                {
                    "name": "create_task",
                    "description": "Creates a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The content of the task, e.g. buy milk"
                            }
                        },
                        "required": ["content"]
                    }
                },
                {
                    "name": "check_task_status",
                    "description": "Checks if a task is done",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_name": {
                                "type": "string",
                                "description": "The name of the task, e.g. buy milk"
                            }
                        },
                        "required": ["task_name"]
                    }
                },
                {
                    "name": "close_task_by_name",
                    "description": "Closes a task with a given name",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_name": {
                                "type": "string",
                                "description": "The name of the task, e.g. buy milk"
                            }
                        },
                        "required": ["task_name"]
                    }
                },
                {
                    "name": "get_undone_tasks",
                    "description": "Gets all undone tasks and returns them as a list"
                }
            ]

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                additional_context=function_list
            )

            message = completion.choices[0].message # type: ignore
            previous.append(message)

            if "function_call" in message:
                function_call = message["function_call"]
                arguments = function_call["arguments"]

                response = None
                function_name = function_call["name"]

                if function_name == "check_weather":
                    response = functions.check_weather(arguments["city"])
                elif function_name == "create_task":
                    response = functions.create_task(arguments["content"])
                elif function_name == "check_task_status":
                    response = functions.check_task_status(arguments["task_name"])
                elif function_name == "close_task_by_name":
                    response = functions.close_task_by_name(arguments["task_name"])
                elif function_name == "get_undone_tasks":
                    response = functions.get_undone_tasks()

                if response is not None:
                    request(f'{{"role": "function", "name": "{function_name}", "content": "{response}"}}')



        stream = self.audio.open(
            rate=self.handle.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.handle.frame_length
        )
        print("listening...")
        while True:
            try:
                pcm = stream.read(self.handle.frame_length)
                pcm = struct.unpack_from("h" * self.handle.frame_length, pcm)

                keyword_index = self.handle.process(pcm)

                if keyword_index >= 0:
                    print("Wake word detected!")
                    with speech_recognition.Microphone() as mic:
                        self.recognizer.adjust_for_ambient_noise(mic)
                        audio = self.recognizer.listen(mic)
                        print("listening...")
                        self.robot_label.config(fg="red")
                        try:
                            audio = self.recognizer.listen(mic)
                            text = self.recognizer.recognize_whisper(audio)
                            self.text_label.config(text="asked: " +text)
                            if text == "stop":
                                self.root.destroy()
                                break
                            elif text is not None:
                                self.robot_label.config(fg="black")
                                self.robot_label.config(text="⌛")
                                chat_completion = request(text)
                                anser = chat_completion.choices[0].message.content # type: ignore
                                self.answer_label.config(text="anser: " + anser)
                                self.robot_label.config(text="🤖")
                                self.voice.say(anser)
                                self.voice.runAndWait()
                                break
                        except speech_recognition.UnknownValueError:
                            print("UnknownValueError at whisper")
                            self.recognizer = speech_recognition.Recognizer()
                            continue
            except speech_recognition.UnknownValueError:
                print("UnknownValueError at speech_recognition")
                self.recognizer = speech_recognition.Recognizer()
                continue
            except Exception as e:
                print("Error at wakeword: " + str(e))
                continue

Assistant()
