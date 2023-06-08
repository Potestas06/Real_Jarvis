import deepspeech
import numpy as np
import pyaudio
import wave
import sys
import time

# Load the DeepSpeech model and scorer
model_path = 'model/output_graph_de.pbmm'
scorer_path = 'model/kenlm_de.scorer'
model = deepspeech.Model(model_path)
model.enableExternalScorer(scorer_path)

# Set up the audio stream
sample_rate = 44100  # Change the sample rate to 44100 Hz
chunk_size = 1024  # Change the chunk size to 1024 samples
stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
# Initialize the previous text
prev_text = ''

# Define a function to transcribe speech and describe the text
def transcribe_and_describe():
    global prev_text  # Add this line to modify the global variable
    # Read audio data from the stream
    audio_data = np.frombuffer(stream.read(chunk_size), dtype=np.int16)
    # Transcribe the speech to text
    text = model.stt(audio_data)
    # Check if the text has changed
    if text != prev_text:
        # Print the text and update the previous text
        print('\nNew text:', text)
        prev_text = text
        return

# Continuously transcribe speech from the audio stream every 10 seconds
while True:
    # Call the transcribe_and_describe function every 10 seconds
    transcribe_and_describe()
    time.sleep(10)