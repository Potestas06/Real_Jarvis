# Real_Jarvis

## Description

![Günter](https://github.com/Potestas06/Real_Jarvis/assets/94400853/19f19624-ffda-4351-9c14-9cd90f71e8e4)


a small Ai voice assistant

## Getting Started
### Dependencies
- python
- SpeechRecognition
- pyttsx3
- pyaudio
- llama-cpp-python
- customtkinter
- argparse
- python-dotenv
- openai
- pvporcupine
- https://github.com/openai/whisper.git soundfile

### Installing
```
git clone https://github.com/Potestas06/Real_Jarvis

python -m venv {environment name}

{environment name}/Scripts/activate

pip install -r requirements.txt

pip install git+https://github.com/openai/whisper.git soundfile
```
now u need to get ur api keys
- https://console.picovoice.ai/
- https://openai.com/
- https://openweathermap.org/
- https://todoist.com/

now u need to create a .env fille
```
APIKEY = picovoice api key
OPENAIKEY = openai key
WHEATERKEY = openweathermap
TODOAPI = todoist api key
```
replace the names with ur api key

### Executing program
if u wan't to run it localy:
```
python reconizer_local.py
```
if u wan't to use functions:
```
python reconizer_OpenAI.py
```

## testcases

Test Number | Description | requirements | steps | Expected result | test result | date | notice
------------| ------------| -----------  | ----- | --------------- | ------------| ---- | ------
1 | Wake word | Setup correctly | 1. say Computer | Computer image turns red after a few seconds| ✓ | 28.06.23| -
2 | Text to speech | Setup correctly | 1. say computer and wait until computer turned red 2. say something like "hi how are you" | ur text is displayed and the ai will respond with something like "good" | ✓ | 28.06.23 | -
3 | Get water | Setup with every api key and you use the reconizer_OpenAI | 1.say wakeword and wait until computer turned red 2.say something like "how is the weather in berlin"| ur text is displayed and the ai response with something like "the weather in Berlin is cloudy with ..." | ✓ | 28.06.23 | -
4 | get undon tasks | Setup with every api key and you use the reconizer_OpenAI | 1. say wakeword and wait until computer turned red 2. say something like "do i have undo tasks" | ur text is displayed and the ai response with something like "yes u have here is a list ...| ✓ | 28.06.23 | -
5 | create task | Setup with every api key and you use the reconizer_OpenAI |  1. say wakeword and wait until computer turned red 2. say something like "create a task called Test"| ur text is displayed and the ai response with something like " task created successfully" and u can see ur task online| ✓ | 28.06.23| -
6 | delete task | Setup with every api key and you use the reconizer_OpenAI |  1. say wakeword and wait until computer turned red 2. say something like "delete a task called Test"| ur text is displayed and the ai response with something like " task deleted successfully" and u can see ur task is deleted online| ✓ | 28.06.23| -
7 | Questions | Setup correctly | 1. say computer and wait until computer turned red 2. ask ur question for example " why is the sky blue"| ur text is displayed and the ai response with something like "the sky is blue because..." | ✓ | 28.06.23| -
