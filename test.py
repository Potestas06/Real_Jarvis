import pvporcupine
import pyaudio
import os
from dotenv import load_dotenv
import struct

load_dotenv()

APIKEY = os.getenv("APIKEY")

# Load the wake word model
handle = pvporcupine.create(access_key=APIKEY, keywords=['computer'])

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Set the audio stream parameters
stream = audio.open(
    rate=handle.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=handle.frame_length
)

print("Listening for wake word...")

while True:
    pcm = stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)

    keyword_index = handle.process(pcm)

    if keyword_index >= 0:
        print("Wake word detected!")
        # Perform action or trigger further processing based on the wake word detection

# Clean up resources
stream.close()
audio.terminate()